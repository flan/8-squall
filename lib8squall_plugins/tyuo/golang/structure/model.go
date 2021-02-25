package structure
import (
    "context"
    "database/sql"
    "errors"
    "fmt"
    "math"
)


type modelNode struct {
    DictionaryId int
    Children map[int]int
    
    childrenSum int64
    childrenSumInitialised bool
}
func (mn *modelNode) ChildrenSum() (int64) {
    if mn.childrenSumInitialised {
        return mn.childrenSum
    }
    
    var sum int64 = 0
    for _, count := range mn.Children {
        sum += count
    }
    
    mn.childrenSum = sum
    mn.childrenSumInitialised = true
    return sum
}
func (mn *modelNode) ChooseUniformRandom() (int, error) {
    //select
    
    //this is a weighted random selection of all possible transition nodes
    target := rng.Int63n(mn.childrenSum())
    for childDictionaryId, count := range mn.Children {
        if target <= 0 {
            return childDictionaryId, nil
        }
        target -= count
    }
    return 0, errors.New(fmt.Sprintf("no children available for selection from %d", mn.DictionaryId))
}
func (mn *modelNode) Frequency(childDictionaryId int) (float64, error) {
    if count, defined := mn.Children[childDictionaryId]; defined {
        if count == 0 {
            return 0.0, errors.New(fmt.Sprintf("no transitions observed from %d to %d", mn.DictionaryId, childDictionaryId))
        }
        
        return float64(count) / float64(mn.ChildrenSum()), nil
    } else {
        return 0.0, errors.New(fmt.Sprintf("child %d is not defined in %d", mn.DictionaryId, childDictionaryId))
    }
}
func (mn *modelNode) Surprise(childDictionaryId int) (float64, error) {
    if frequency, err := mn.Frequency(childDictionaryId); err == nil {
        return -math.Log2(float64(count) / float64(mn.ChildrenSum())), nil
    } else {
        return 0.0, err
    }
}


type model struct {
    db *sql.DB
    tableName string
}
func prepareModel(database *sql.DB, tableName string) (*model, error) {
    return &model{
        db: database,
        tableName: string,
    }, nil
}
func (m *model) GetModelNodes(parentDictionaryIds []int) ([]modelNode, error) {
    //find_context
    
    output := make([]modelNode, len(parentDictionaryIds))
    
    var queryStmt := m.db.Prepare(fmt.Sprintf("SELECT childDictionaryId, count FROM statistics_%s WHERE parentDictionaryId = ?", m.tableName))
    defer queryStmt.Close()
    
    for i, parentDictionaryId := range parentDictionaryIds {
        if rows, err := queryStmt.Query(parentDictionaryId); err == nil {
            children := make(map[int]int)
            
            var childDictionaryId, count int
            for rows.Next() {
                rows.Scan(&childDictionaryId, &count)
                children[childDictionaryId] = count
            }
            
            output[i] = modelNode{
                DictionaryId: parentDictionaryId,
                Children: children,
                
                childrenSum: 0,
                childrenSumInitialised: false,
            }
        } else {
            return nil, err
        }
    }
    return output, nil
}
func (m *model) UptickNodes(parentDictionaryIds []int, childDictionaryIds []int) (error) {
    //observe
    //This is a simple parallel arrays model.
    
    var ctx context.Context
    if tx, err := m.db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable}); err == nil {
        var queryStmt := tx.Prepare(fmt.Sprintf("SELECT count FROM statistics_%s WHERE parentDictionaryId = ? AND childDictionaryId = ?", m.tableName))
        defer queryStmt.Close()
        
        var updateStmt := tx.Prepare(fmt.Sprintf("UPDATE statistics_%s SET count = ? WHERE parentDictionaryId = ? AND childDictionaryId = ?", m.tableName))
        defer updateStmt.Close()
        
        var insertStmt := tx.Prepare(fmt.Sprintf("INSERT INTO statistics_%s (parentDictionaryId, childDictionaryId, count) values (?, ?, 1)", m.tableName))
        defer insertStmt.Close()
        
        var deleteStmt := tx.Prepare(fmt.Sprintf("DELETE FROM statistics_%s WHERE parentDictionaryId = ? AND childDictionaryId = ?", m.tableName))
        defer deleteStmt.Close()
        
        rescaleNeeded := make(map[int]bool)
        for i, parentDictionaryId := range parentDictionaryIds {
            childDictionaryId := childDictionaryIds[i]
            
            if rows, err := queryStmt.Query(parentDictionaryId, childDictionaryId); err == nil {
                var count sql.NullInt32
                for rows.Next() {
                    rows.Scan(&count)
                }
                if count.Valid {
                    newCount := count.Int32 + 1
                    if newCount > rescaleThreshold {
                        rescaleNeeded[parentDictionaryId] = true
                    }
                    if _, err = updateStmt.Exec(newCount, parentDictionaryId, childDictionaryId); err != nil {
                        return err
                    }
                } else {
                    if _, err = insertStmt.Exec(parentDictionaryId, childDictionaryId); err != nil {
                        return err
                    }
                }
            } else {
                return err
            }
        }
        
        if len(rescaleNeeded) > 0 {
            var rescaleQueryStmt := tx.Prepare(fmt.Sprintf("SELECT childDictionaryId, count FROM statistics_%s WHERE parentDictionaryId = ?", m.tableName))
            defer rescaleQueryStmt.Close()
            
            for parentDictionaryId, _ := range rescaleNeeded {
                if rows, err := rescaleQueryStmt.Query(parentDictionaryId); err == nil {
                    var childDictionaryId, count int
                    for rows.Next() {
                        rows.Scan(&childDictionaryId, &count)
                        count /= rescaleDecimator
                        if count > 0 {
                            if _, err = updateStmt.Exec(count, parentDictionaryId, childDictionaryId); err != nil {
                                return err
                            }
                        } else {
                            if _, err = deleteStmt.Exec(parentDictionaryId, childDictionaryId); err != nil {
                                return err
                            }
                        }
                    }
                } else {
                    return err
                }
            }
        }
    } else {
        return err
    }
}

//TODO: consider changing the "child" structure, in-database, to be a JSON block, like
//the dictionary, though this one will need to be an array of tuples, since it's a pair of ints
//NOTE: this seems like a pretty good idea, and all lookups start by querying the parent object
//by its ID
//The only thing that complicates it is in how forgetting will work: every single row in the
//database will need to be unpacked and analysed.
//...Unless this gets implemented as a banlist in the database, as a tuple of case-insensitive
//string and, if defined, dictionary ID, maybe loaded in its entireity when the memory is prepared,
//and if any of the transitions from this token are in that list, they just get deleted when it's
//written back to disk.

//when banning words, use a "startswith" check
