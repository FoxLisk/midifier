* Gracefully handle >16 channels exceptions
* Channels representing high-scope functions (i.e. the first or second function scope encountered) should periodically play new notes.
  Probably something along the lines of: every now and then we go down the scope stack, and at each level we either change the playing
  note or not with probability inversely proportional to how far down the stack we are; i.e. the bottom of the stack changes least often.
  I think this should be logarithmic.
* other "scopes" should have some behaviour.
* Figure out binding multiple tracks together, and then implement this as midifying multiple files.
* Think about, maybe, storing the source text in the midi file -- that makes the process reversible but its also not very important
* Look into seeding the RNG with a hash of the source content or something, in order to make the process deterministic. Probably make this determinism optional.
* At some point it might be cool to allow various things to be configured — choice of instruments, keys, etc —
  but only if anyone actually uses this dumb thing, which they wont.
