### twisted.conch.ssh.userauth doesn't work on Python 3

I'm trying to use Twisted Conch on Python 3 to run an SSH server with user authentication. As far as I can tell from `twisted.python.dist3`, most of `twisted.conch.ssh` has already been ported, but `userauth` is still listed as not-really-ported, and in practice it falls over as soon as a client tries to authenticate.

If I set up an `SSHUserAuthServer` against a portal and let a normal client try to log in (say with publickey), the server blows up while handling the userauth request — nothing gets through, and the auth attempt never reaches the checker. Switching to `password` doesn't help either: the dispatch from the requested method name to the `auth_*` handler doesn't seem to survive on Python 3, so no method ever runs. On Python 2 the same setup works fine, so this looks specific to the Py3 port.

It would be great to finish porting `twisted.conch.ssh.userauth` (both `SSHUserAuthServer` and `SSHUserAuthClient`) so that the standard auth methods (publickey, password, keyboard-interactive) actually complete on Python 3, and to flip it over in `twisted.python.dist3` so it shows up as a properly supported module on Py3.

Tracking ticket: https://twistedmatrix.com/trac/ticket/8654
