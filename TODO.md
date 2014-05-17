To Do
=====

* Gracefully handle >16 channels exceptions
  * I think it's reasonable to handle this situation by treating it as a syntax error. Certainly 16-deep function nesting *should* be considered an error.
* other "scopes" should have some behaviour.
* Figure out binding multiple tracks together, and then implement this as midifying multiple files.
* Think about, maybe, storing the source text in the midi file -- that makes the process reversible but its also not very important
* At some point it might be cool to allow various things to be configured — choice of instruments, keys, etc —
  but only if anyone actually uses this dumb thing, which they wont.
* Doesn't currently handle one-statement if/else/etc blocks (i.e. without `{}`). I think it is reasonable to consider this a syntax error.
* Come up with some awful dissonant shit to play when a syntax error is encountered. Play it when a syntax error is encountered.

To Not Do
=========

* Parse regexes. It's just too fucking hard.
