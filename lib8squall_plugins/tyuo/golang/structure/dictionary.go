package structure
import (
    "database/sql"
    "flags"
    "strings"
)

const caseSensitiveRepresentationThreshold = 0.9

type dictionaryWord struct {
    id int
    caseInsensitiveOccurrences int
    caseInsensitiveRepresentation string
    capitalisedForms map[string]int64
}
func (dw *dictionaryWord) UpdateRepresentation(token string) {
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
func (dw *dictionaryWord) Represent() (string, bool) {
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
    db *sql.DB
    
    lastMarkovIdentifier int
}
func prepareDictionary(database *sql.DB) (*dictionary, error) {
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
        db: database,
        
        lastMarkovIdentifier: lastMarkovIdentifier,
    }, nil
}
func (d *dictionary) EnumerateWordsByToken(tokens []string) (map[string]int, error) {
    lcaseToken := strings.ToLower(token)
    
    //return every token and ID that contains the given token
}
func (d *dictionary) GetWordsByToken(tokens []string) ([]dictionaryWord, error) {
    lcaseToken := strings.ToLower(token)
    
    //if lcaseToken isn't in memory, prepare a new dictionaryWord and call upsertWord()
    //before returning it
    
    
    //needs to deserialise capitalisedForms from JSON as map[string]int64
}
func (d *dictionary) GetWordsById(ids []int) ([]dictionaryWord, error) {
    //if id isn't in memory, raise an error
    
    //needs to deserialise capitalisedForms from JSON as map[string]int64
}
func (d *dictionary) UpsertWords(dws []dictionaryWord) (error) {
    
    //needs to serialise capitalisedForms as JSON if len() > 0; null otherwise
    //Golang's Marshal() uses compact representations by default
    //data stored in the database is further compressed using zlib
}



var bannedTokensList = flag.String("banned-tokens-list",
                        filepath.Join(user.Current().HomeDir, "/.tyuo/banned-tokens"),
                        "the path to a file containing banned tokens",
                       )
var bannedTokens []string = make([]string, 0)
func init() {
    //parse bannedTokensList, adding each one to bannedTokens
}

type bannedToken struct {
    id int
    token string
}
type bannedDictionary struct {
    db *sql.DB
    dict *dictionary,
    
    tokens []bannedToken
    ids []int
}
func prepareBannedDictionary(database *sql.DB, dict *dictionary) (*bannedDictionary, error) {
    var bannedTokens []bannedToken
    var bannedIds []int
    if rows, err := database.Query("SELECT token FROM banned_dictionary"); err == nil {
        tokens := make([]string, 0)
        var token string
        for rows.Next() {
            rows.Scan(&token)
            tokens = append(tokens, token)
        }
        if words, err := dict.EnumerateWordsByToken(tokens); err == nil {
            bannedTokens = make([]bannedToken, 0)
            bannedIds = make([]int, 0)
            for _, token = range tokens {
                if id, defined := words[token]; defined {
                    bannedTokens = append(bannedTokens, token)
                    bannedIds = append(bannedIds, id)
                    delete(words, token)
                }
            }
            for token, id := range(words) {
                bannedTokens = append(bannedTokens, token)
                bannedIds = append(bannedIds, id)
            }
        } else {
            return nil, err
        }
    } else {
        return nil, err
    }
    
    //TODO: sort bannedIds
    
    return &bannedDictionary{
        db: database,
        dict: dict,
        
        tokens: bannedTokens,
        ids: bannedIds,
    }, nil
}
func (bd *bannedDictionary) areAllowed(tokens []string)) (bool) {
    //iterate through bd.bannedToken; if the given token contains a banned token,
    //return false
    
    //otherwise, do the same thing against the global banned tokens list
    
    //if none of the tokens are offensive, return true
}
func (bd *bannedDictionary) IdentifiyBannedIds(ids []int)) ([]int) {
    //do a binary search on bd.bannedIds; if the ID is banned, append it to the output
    
    //TODO: use this data to filter transitions in model
}
func (bd *bannedDictionary) BanTokens(tokens []string) ([]int, error) {
    //get matches from bd.dict.EnumerateWordsByToken(tokens);
    //append token to bd.bannedTokens if not already present
    //append any IDs to the output and bd.bannedIds
    //re-sort bd.bannedIds
    
    //add to banned tokens on disk, if anything was changed
    
    //TODO: use the output to delete any transition-parents from model
}
func (bd *bannedDictionary) UnbanTokens(tokens []string) (error) {
    //get matches from bd.dict.EnumerateWordsByToken(tokens);
    //remove exact tokens from bd.bannedTokens, if present (not what came from enumeration,
    //rather what was supplied to avoid being too accepting)
    //remove matching IDs from bd.bannedIds, preserving sorted order
    //(should be able to just join two slices after finding a match for both)
    
    //remove from banned tokens on disk, if anything was changed
}
func (bd *bannedDictionary) EnumerateBannedTokens() ([]string) {
    bannedTokensSet := make(map[string]bool)
    for _, token := range bd.bannedTokens {
        bannedTokensSet[token] = false
    }
    for _, token := range bannedTokens {
        bannedTokensSet[token] = false
    }
    
    bannedTokensSlice := make([]string, len(bannedTokensSet))
    i := 0
    for token, _ := range bannedTokensSet {
        bannedTokensSlice[i++] = token
    }
    
    //sort bannedTokensSlice
    
    return bannedTokensSlice
}
