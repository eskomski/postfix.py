# postfix.py
An interpreter for PostFix, a stack-based language found in Turbak and Gifford's Design Concepts in Programming Languages.
Written for Python 3.

I hastily put this together over the course of a couple of days after covering the basics of the language in my programming
languages class. I'll have to implement this in Prolog eventually, so I figured doing an implementation in Python would be 
a good warmup. It could definitely use some cleanup and testing, but it's working well enough for simple programs.

### Usage
`python postfix.py '(postfix 1 1 nget mul)' -args 2`
