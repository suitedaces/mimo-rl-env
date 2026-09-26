### Environment
* Nautobot version (Docker tag too if applicable): 1.5.9
* Python version: 3.10
* Database platform, version:
* Middleware(s):

<!--
    If user has two or more Nautobot windows opened and is logged out after some time of inactivity or user log out in one window, switch to the second window and search for something he get "No results found" instead of login window (or at least message that user is logged out).
-->
### Steps to Reproduce
1. Open two Nautobot windows
2. Log out in one window
3. Switch to the second window and search for any object (prefix, device, etc.)
4. You will receive "No results found" instead of login window (or at least message that user is logged out).

<!-- What did you expect to happen? -->
To receive login window.

<!-- What happened instead? -->
Received confusing message "No results found".
