Environment variables set to empty cause silent failing of auth
Hello,

recently, we stumbled upon an interesting 'bug' that took us some time to resolve - we had set `AWS_ACCESS_KEY_ID` env variable set to empty, which resulted of having it in `os.environ` as empty string. If it's there as an empty string, it causes config resolver to use EnvProvider - even if it's clearly invalid. While i realize that this issue is caused by us, I would like to propose a small improvement to EnvProvider - which will not only check if env variables are set - but also if they're valid and log/error out when that's not the case, allowing users for quicker debugging. 

If I can help with the implementation, please let me know, I would gladly take a stab at it.

Regards,
Piotr
