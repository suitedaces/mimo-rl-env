Add option to open doc preview window in a vertical right split
# Issue Prelude

**Please complete these steps and check these boxes (by putting an `x` inside
the brackets) _before_ filing your issue:**

- [x] I have read and understood YCM's [CONTRIBUTING][cont] document.
- [x] I have read and understood YCM's [CODE_OF_CONDUCT][code] document.
- [x] I have read and understood YCM's [README][readme], **especially the
  [Frequently Asked Questions][faq] section.**
- [x] I have searched YCM's issue tracker to find issues similar to the one I'm
  about to report and couldn't find an answer to my problem. ([Example Google
  search.][search])
- [x] If filing a bug report, I have included the output of `vim --version`.
- [x] If filing a bug report, I have included the output of `:YcmDebugInfo`.
- [x] If filing a bug report, I have attached the contents of the logfiles using
  the `:YcmToggleLogs` command.
- [x] If filing a bug report, I have included which OS (including specific OS
  version) I am using.
- [x] If filing a bug report, I have included a minimal test case that reproduces
  my issue, using `vim -Nu /path/to/YCM/vimrc_ycm_minimal`, including what I
  expected to happen and what actually happened.
- [x] If filing a installation failure report, I have included the entire output
  of `install.py` (or `cmake`/`make`/`ninja`) including its invocation
- [x] **I understand this is an open-source project staffed by volunteers and
  that any help I receive is a selfless, heartfelt _gift_ of their free time. I
  know I am not entitled to anything and will be polite and courteous.**
- [x] **I understand my issue may be closed if it becomes obvious I didn't
  actually perform all of these steps.**

Thank you for adhering to this process! It ensures your issue is resolved
quickly and that neither your nor our time is needlessly wasted.

# Issue Details

* What did you do?

Executed `:rightbelow vertical YcmCompleter GetDoc`.

* What did you expect to happen?

I expected the documentation to appear in a vertical split on the right side, similar to how `:rightbelow vertical YcmCompleter GoTo` opens a split in a vertical split on the right side.

* What actually happened?

The documentation / preview window appeared on the top. I was able to move the preview window to the bottom by setting `set splitbelow` (as recommended in https://github.com/ycm-core/YouCompleteMe/issues/2355). I tried setting `set splitright`, however, that did not seem to have any effect.
