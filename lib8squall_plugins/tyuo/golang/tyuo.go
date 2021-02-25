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
    "action": "createContext",
    "context": <ID as string>,
 }
 {
    "action": "dropContext",
    "context": <ID as string>,
 }
 {
    "action": "prompt",
    "context": <ID as string>,
    "input": [<string>],
    "learn": <bool>, //should this be an option? Maybe just explicitly requiring a second call will be clearer
 }
 {
    "action": "learn",
    "context": <ID as string>,
    "input": [<string>],
 }
 {
    "action": "banTokens",
    "context": <ID as string>,
    "tokens": [<token>],
 }
 {
    "action": "unbanTokens",
    "context": <ID as string>,
    "tokens": [<token>],
 }
 {
    "action": "listBannedTokens",
    "context": <ID as string>,
 }
*/


var logger = loggo.GetLogger("main")

func runForever() {
    
}

func main() {
    shutdownChannel := runForever(shutdownChannel)
    
    
    
    shutdownChannel<- true
}

//on-boot, don't connect to any contexts, but when a context is accessed,
//hold on to the connection indefinitely

//each context needs to be threadsafe, which can be accomplished by having
//structures.GetContext(contextId)'s returned object exposes an RWLock, with
//the "query" path being a reader and everything else being a writer

//if a context gets dropped while there are still clients waiting to access it,
//just let the memory-access steps raise errors
