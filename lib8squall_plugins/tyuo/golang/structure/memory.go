package structure
import (
    "database/sql"
    "filepath"
    "flags"
    "os"
    "os/user"

    _ "github.com/mattn/go-sqlite3"
)

var dbDir = flag.String("db-dir",
                        filepath.Join(user.Current().HomeDir, "/.tyuo/databases"),
                        "the path in which tyuo's databases are stored",
                       )


type memory struct {
    db *sql.DB
    
    Dictionary *dictionary
    BannedDictionary *bannedDictionary
    ModelForward *model
    ModelReverse *model
}
func (m *memory) Close() {
    m.db.Close()
}

func initialiseMemory(dbPath string) (*sql.DB, error) {
    database, err := sql.Open("sqlite3", dbPath)
    if err != nil {
        return nil, err
    }
    
    if _, err := database.Exec(`CREATE TABLE dictionary (
        id INTEGER NOT NULL PRIMARY KEY,
        caseInsensitiveOccurrences INTEGER NOT NULL,
        caseInsensitiveRepresentation TEXT NOT NULL UNIQUE,
        capitalisedFormsJSON BLOB
    )`); err != nil {
        database.Close()
        return nil, err
    }
    
    if _, err := database.Exec(`CREATE TABLE statistics_forward (
        parentDictionaryId INTEGER NOT NULL,
        childDictionaryId INTEGER NOT NULL,
        count INTEGER NOT NULL,
        
        FOREIGN KEY(parentDictionaryId) REFERENCES dictionary(id) ON DELETE CASCADE,
        FOREIGN KEY(childDictionaryId) REFERENCES dictionary(id) ON DELETE CASCADE,
        PRIMARY KEY(parentDictionaryId, childDictionaryId)
    )`); err != nil {
        database.Close()
        return nil, err
    }
    
    if _, err := database.Exec(`CREATE TABLE statistics_reverse (
        parentDictionaryId INTEGER NOT NULL,
        childDictionaryId INTEGER NOT NULL,
        count INTEGER NOT NULL,
        
        FOREIGN KEY(parentDictionaryId) REFERENCES dictionary(id) ON DELETE CASCADE,
        FOREIGN KEY(childDictionaryId) REFERENCES dictionary(id) ON DELETE CASCADE,
        PRIMARY KEY(parentDictionaryId, childDictionaryId)
    )`); err != nil {
        database.Close()
        return nil, err
    }
    
    return database, nil
}
func prepareMemory(contextId string) (*memory, error) {
    dbPath := filepath.Join(*dbDir, contextId + '.sqlite3')
    
    var database *sql.DB
    if _, err := os.Stat(dbPath); os.IsNotExist(err) {
        //TODO: don't automatically create a new memory
        //instead, have an action be required to create new memory
        //and this will just return an error
        
        if database, err = initialiseMemory(dbPath); err != nil {
            return nil, err
        }
    } else {
        if database, err = sql.Open("sqlite3", dbPath); err != nil {
            return nil, err
        }
    }
    
    dict, err := prepareDictionary(database)
    if err != nil {
        database.Close()
        return nil, err
    }
    bannedDict, err := prepareBannedDictionary(database, dict)
    if err != nil {
        database.Close()
        return nil, err
    }
    
    modForward, err := prepareModel(database, bannedDict, "forward")
    if err != nil {
        database.Close()
        return nil, err
    }
    modReverse, err := prepareModel(database, bannedDict, "reverse")
    if err != nil {
        database.Close()
        return nil, err
    }
    
    return &memory{
        db: database
        
        Dictionary: dict,
        BannedDictionary: bannedDict,
        ModelForward: modForward,
        ModelReverse: modReverse,
    }, nil
}
