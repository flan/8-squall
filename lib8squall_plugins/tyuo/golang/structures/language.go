package structures
import (
    "strings"
)

//language handles traits and patterns specific to English, the only language tyuo is intended to
//support


//when learning a word not in the established English dictionary, keep track of how often it
//gets capitalised versus not when in the middle of a sentence
//if one of the capitalisedForms occurs more than 10% of the time, use that when displaying it.

type voidWord struct{}
const referenceVoidWord voidWord
var dictionary = make(map[string]voidWord)

type nonNativeWord struct {
    caseInsensitiveOccurrences uint
    capitalisedForms map[string]uint
}
var nonNativeDictionary = make(map[string]*nonNativeWord)

func init() {
    //load native dictionary from a file that's just a list of words
    
    //load non-native dictionary from memory
    //it's okay for all the contexts to share the same non-native structures
}

//only called when the given word isn't the first in the input sequence or after
//punctuation that implies it should be capitalised
func updateDictionary(token string) {
    lcaseToken := strings.ToLower(token)
    if _, defined := dictionary[lcaseToken]; !defined { //it's a non-native word
        nnWord, defined := nonNativeDictionary[lcaseToken]
        if !defined {
            nnWord = &nonNativeWord{
                caseInsensitiveOccurrences: 0,
                capitalisedForms: make(map[string]uint),
            }
            nonNativeDictionary[lcaseToken] = nnWord
        }
        
        if lcaseToken == token {
            nnWord.caseInsensitiveOccurrences += 1
        } else {
            instances, defined := nnWord.capitalisedForms[token]
            if !defined {
                instances = 1
            } else {
                instances += 1
            }
            nnWord.capitalisedForms[token] = instances
        }
        
        //prevent these counts from ever becoming large enough to overflow
        rescaleNeeded := nnWord.caseInsensitiveOccurrences >= 65535
        if not rescaleNeeded {
            for _, occurrences := range nnWord.capitalisedForms {
                if occurrences >= 65535 {
                    rescaleNeeded = true
                    break
                }
            }
        }
        if rescaleNeeded {
            nnWord.caseInsensitiveOccurrences /= 10
            for t, occurrences := range nnWord.capitalisedForms {
                nnWord.capitalisedForms[t] /= 10
            }
        }
        
        //update memory for persistence
        //this operation needs to be threadsafe, but it doesn't matter if it
        //races, since it'll still be close enough, ratio-wise
        //TODO: go memoryUpdateNonNativeDictionary(lcaseToken, nnWord)
    }
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

