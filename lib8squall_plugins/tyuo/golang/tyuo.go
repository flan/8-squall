/* tyuo is a Markov-chain-based chatbot, loosely based on MegaHAL from 1999 by 
 * Jason Hutchens.
 * 
 * More specifically, tyuo is a rewrite of yuo, written by Neil Tallim in 2002,
 * based on a limited understanding of how MegaHAL worked, significantly
 * butchered, but that was undeniably the initial inspiration for whatever this
 * is now.
 */

//run a TCP server to handle interactions

//store memory in SQLite

//use JSON to handle interactions
/*
 {
    "action": "query",
    "input": [<string>],
    "context": <butter ID as string>,
    "learn": <bool>,
 }
 {
    "action": "learn",
    "input": [<string>],
    "context": <ID as string>,
 }
 {
    "action": "forget",
    "tokens": [<token>],
    "context": <ID as string>,
 }
*/

package main

import (
    "github.com/juju/loggo"
        
    "structures"
)

var logger = loggo.GetLogger("main")

func runForever() {
    
}

func main() {
    shutdownChannel := runForever(shutdownChannel)
    
    
    
    shutdownChannel<- true
}

//each context needs to be threadsafe, retrieved with structures.GetContext(id),
//which might build a new one if the given ID doesn't already exist
