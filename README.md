# py-ucsd-api-lib
This is my attempt to make something usable off UCSD API in python

## Problem statement
To be honest, in its present state, Cisco UCSD API is a mess. 
- The docs sometimes list API calls that don't work in a real deployment
- Sometimes the return is in XML, when you expect JSON; sometimes it's the other way around
- call attributes are very un-systematic, looks like every function re-invents the wheel - there's no consistency about the meaning of the param values
- error messages are not very useful - could be better when the Developper mode is active

## Why? What? Who?
This is just an experiment. Also, the rep is in a limbo called "a work in progress". 
Expect bugs and dirty code.

I'm trying to make a wrapper that will work with my UCSD lab setup.
- if it works, that's great!
- if it doesn't, that'll be a bummer

# Goals
- Clear GET / DO separation is one of my primary goals; i.e. each function MUST either GET a state or DO something (change state); other options are possible - I'll be flexible with that
- all functions MUST return either a directly usable (parsed) data structures, or None in case of failures
- failures MUST be logged

# Usage
Just 'from pyucsd import *' should be enouth.

I try to annotate the functions as much as possible.

Maybe I'll get to write some usage examples someday.

## Tests
I know it's wrong, but no tests right now. Primarily because I'm yet to learn how to write them ;-)
This makes this libe unsuitable for production.

## Dependencies (non-standard lib)
- defusedxml.ElementTree

# Related work & due credit
This repository was greatly influenced by work done by hpreston ( https://github.com/hpreston/cisco_cloud ).
I outright copy some of his code, with credit given directly inline where it is due.
