package structure
import (
    "database/sql"
    "strings"
)

const caseSensitiveRepresentationThreshold = 0.9

type dictionaryWord struct {
    id int
    caseInsensitiveOccurrences int
    caseInsensitiveRepresentation string
    capitalisedForms map[string]int64
}
func (dw *dictionaryWord) updateRepresentation(token string) {
    if token == dw.caseInsensitiveRepresentation {
        dw.caseInsensitiveOccurrences += 1
    } else {
        occurrences, defined := dw.capitalisedForms[token]
        if !defined {
            occurrences = 1
        } else {
            occurrences += 1
        }
        dw.capitalisedForms[token] = occurrences
    }
    
    //prevent these counts from ever becoming large enough to overflow
    rescaleNeeded := dw.caseInsensitiveOccurrences >= rescaleThreshold
    if not rescaleNeeded {
        for _, occurrences := range dw.capitalisedForms {
            if occurrences >= rescaleThreshold {
                rescaleNeeded = true
                break
            }
        }
    }
    if rescaleNeeded {
        dw.caseInsensitiveOccurrences /= rescaleDecimator
        for t, occurrences := range dw.capitalisedForms {
            occurrences /= rescaleDecimator
            if occurrences == 0 {
                delete(dw.capitalisedForms, t)
            } else {
                dw.capitalisedForms[t] = occurrences
            }
        }
    }
}
func (dw *dictionaryWord) occurrenceSum() (float64) {
    sum := float64(dw.caseInsensitiveOccurrences)
    for _, count := range dw.capitalisedForms {
        sum += count
    }
    return sum
}
func (dw *dictionaryWord) represent() (string, bool) {
    if dw.caseInsensitiveOccurrences / dw.occurrenceSum() > caseSensitiveRepresentationThreshold {
        return dw.caseInsensitiveRepresentation, true
    } else {
        var mostRepresented string
        var mostRepresentedCount int64 = 0
        for representation, count := range dw.capitalisedForms {
            if count > mostRepresentedCount {
                mostRepresentedCount = count
                mostRepresented = representation
            }
        }
        return mostRepresented, false
    }
}

type dictionary struct {
    memory *memory
    
    lastMarkovIdentifier int
}
func prepareDictionary(memory *memory) (*dictionary, error) {
    var lastMarkovIdentifier int
    if rows, err := database.Query("SELECT MAX(id) FROM dictionary"); err == nil {
        var maxId sql.NullInt32
        for rows.Next() {
            rows.Scan(&maxId)
        }
        if maxId.Valid {
            lastMarkovIdentifier = maxId
        } else {
            lastMarkovIdentifier = sentenceBoundary + 1 //the first valid identifier
        }
    } else {
        return nil, err
    }
    
    return &dictionary{
        memory: memory,
        
        lastMarkovIdentifier: lastMarkovIdentifier,
    }, nil
}
func (d *dictionary) getWordsByToken(tokens []string) ([]dictionaryWord, error) {
    lcaseToken := strings.ToLower(token)
    
    //if lcaseToken isn't in memory, prepare a new dictionaryWord and call upsertWord()
    //before returning it
    
    
    //needs to deserialise capitalisedForms from JSON as map[string]int64
}
func (d *dictionary) getWordsById(ids []int) ([]dictionaryWord, error) {
    //if id isn't in memory, raise an error
    
    //needs to deserialise capitalisedForms from JSON as map[string]int64
}
func (d *dictionary) upsertWords(dws []dictionaryWord) (error) {
    
    //needs to serialise capitalisedForms as JSON if len() > 0; null otherwise
    //Golang's Marshal() uses compact representations by default
    //data stored in the database is further compressed using zlib
}
