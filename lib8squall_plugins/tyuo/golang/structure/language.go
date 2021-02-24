package structure
import (
    "strings"
)

//language handles traits and patterns specific to English, the only language tyuo is intended to
//support

const sentenceBoundary int = -2147483648 //used to denote the end of a sentence









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


//all the stuff about MegaHAL's "brain" dict can probably be ignored
//it looks like that's entirely to make sure the correct personality context is used,
//which tyuo's memory model entirely sidesteps through isolation at the database level



/* When deriving keywords from input, use a combination of an exclusion-list to delete words
 * frequently associated with questions ("what is it about his brain?" really only has one
 * interesting keyword, which also happens to be the noun) and order what's left over by
 * sorting against dw.occurrenceSum(). Also omit punctuation marks.
 */
