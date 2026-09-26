## Reverse token filter mangles strings that contain combining characters

I'm using the `reverse` token filter as part of an analyzer chain to index text in a few languages that make heavy use of diacritics (think Vietnamese, or French/Spanish text that ends up in NFD form after some upstream normalization). The idea is to reverse the token so I can do suffix-style matching.

The problem: tokens that contain combining characters come out of the reverse filter looking corrupted. Characters that the user sees as a single accented letter get broken apart, and the pieces end up in the wrong order relative to each other. So a word that should still be a readable (reversed) string of accented letters comes out as garbage where the accent marks are attached to the wrong base letters.

For plain ASCII tokens everything looks fine. The breakage only shows up once the input contains characters that are encoded as a base character followed by one or more combining marks.

What I'd expect is that reversing a token treats each user-perceived character as a single unit — so an accented letter stays an accented letter after reversal, just in a new position in the string. Right now reversing visibly destroys those characters, which makes the filter unusable for anything beyond pure ASCII / pre-composed input.

Could the reverse filter be made to handle these combining-character sequences correctly?
