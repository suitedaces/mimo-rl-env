Hi, I have tested the newest version of Foolbox and it seems like it can't handle parallel batch attacks with estimated gradients models, any idea on when it will be released?

(In case it helps: I'd also expect a public per-sample entry point like `gradient_one(...)` on the estimated-gradient wrapper alongside the batched `gradient(...)`.)
