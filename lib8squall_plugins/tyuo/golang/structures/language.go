package structures
import (
    "strings"
    "sync"
)

//language handles traits and patterns specific to English, the only language tyuo is intended to
//support


//when learning a word, keep track of how often it
//gets capitalised versus not when in the middle of a sentence
//if the caseInsensitive form makes up less than 90% of occurrences,
//display whichever capitalised form has the highest rate

type word struct {
    markovIdentifier int
    caseInsensitiveOccurrences int
    caseInsensitiveRepresentation string
    capitalisedForms map[string]int
}
var dictionary = make(map[string]*word)
var markovDictionary = make(map[int]*word)
const sentenceBoundary int = -2147483648
var lastMarkovIdentifier int = -2147483647
const dictionaryLock sync.Mutex

func loadWord(w *word) {
    dictionary[w.caseInsensitiveRepresentation] = w
    markovDictionary[w.markovIdentifier] = w
    if w.markovIdentifier > lastMarkovIdentifier {
        lastMarkovIdentifier = w.markovIdentifier
    }
}

func init() {
    //load dictionary from memory: for word in range <memory.getWords()> {loadWord(word)}
    //it's okay for all the contexts to share the same dictionary structures
}

func getWord(token string) (*word) {
    lcaseToken := strings.ToLower(token)
    
    dictionaryLock.Lock()
    
    w, defined := dictionary[lcaseToken]
    if !defined {
        lastMarkovIdentifier += 1
        w = &word{
            markovIdentifier: lastMarkovIdentifier,
            caseInsensitiveOccurrences: 0,
            caseInsensitiveRepresentation: lcaseToken,
            capitalisedForms: make(map[string]int),
        }
        dictionary[lcaseToken] = w
    }
    
    if lcaseToken == token {
        w.caseInsensitiveOccurrences += 1
    } else {
        instances, defined := w.capitalisedForms[token]
        if !defined {
            instances = 1
        } else {
            instances += 1
        }
        w.capitalisedForms[token] = instances
    }
    
    //prevent these counts from ever becoming large enough to overflow
    rescaleNeeded := w.caseInsensitiveOccurrences >= 32760
    if not rescaleNeeded {
        for _, occurrences := range w.capitalisedForms {
            if occurrences >= 32760 {
                rescaleNeeded = true
                break
            }
        }
    }
    if rescaleNeeded {
        w.caseInsensitiveOccurrences /= 10
        for t, occurrences := range w.capitalisedForms {
            occurrences /= 10
            if occurrences == 0 {
                delete(w.capitalisedForms, t)
            } else {
                w.capitalisedForms[t] = occurrences
            }
        }
    }
    
    lastMarkovIdentifier.Unlock()
    
    //update memory for persistence
    //this operation needs to be threadsafe, but it doesn't matter if it
    //races, since it'll still be close enough, ratio-wise
    //TODO: go memoryUpdateNonNativeDictionary(lcaseToken, nnWord)
    
    return w
}



const minimumLearnableLength = 4 //the minimum number of consecutive
                                 //non-punctuation tokens required to consider
                                 //a sentence learnable
//a lexer, producing output including punctuation symbols and a boolean
//indicating whether the input is suitable for learning
func ParseInput(input string) ([]string, bool) {
    
    //check each token against the list of banned words
    
    //go's strings.IsLetter will probbaly be enough to distinguish between a
    //part-of-word and punctuation case.
    
    //When dealing with any unrecognised punctuation, in re-assembly,
    //process it like a comma.
    
    //disallow learning when two punctuation tokens follow each other
    //however, unbroken strings of "?" and "!", or a triplet of "."s
    //become a single token and are valid.
    //In these cases, it's only valid to continue with a trigram+ match
    //in lesser cases, terminate the flow as though the sentence ended after them
    
    //quotation marks, brackets, and any other non-standalone punctuation
    //are also unacceptable for learning
}

