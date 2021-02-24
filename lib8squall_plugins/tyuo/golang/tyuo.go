/* tyuo is a Markov-chain-based chatbot, loosely based on MegaHAL by Jason
 * Hutchens.
 * 
 * More specifically, tyuo is a rewrite of yuo, written by Neil Tallim in 2002,
 * based on a limited understanding of how MegaHAL worked, significantly
 * butchered, but that was undeniably the initial inspiration for whatever this
 * is now.
 */
package main
import (
    "github.com/juju/loggo"
        
    "structures"
)

//run a TCP server to handle interactions

//store memory in SQLite

//use JSON to handle interactions
/*
 {
    "action": "setContext",
    "context": <ID as string>,
 }
 {
    "action": "query",
    "input": [<string>],
    "learn": <bool>,
 }
 {
    "action": "learn",
    "input": [<string>],
 }
 {
    "action": "forget",
    "tokens": [<token>],
 }
*/


var logger = loggo.GetLogger("main")

func runForever() {
    
}

func main() {
    shutdownChannel := runForever(shutdownChannel)
    
    
    
    shutdownChannel<- true
}

//each context needs to be threadsafe, retrieved with structures.GetContext(id),
//which might build a new one if the given ID doesn't already exist

//when a context is set, let the caller have exclusive access to it until that
//TCP session ends
//note: set a very brief TCP timeout

