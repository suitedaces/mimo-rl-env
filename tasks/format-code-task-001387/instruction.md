UserStorage: Allow all signed-in users to access storage
At the moment, only users with an Editor role (or more privileged) can use their user storage. For other roles (`Viewer`, `None`), it fails:

![Image](https://github.com/user-attachments/assets/a40b4797-040c-477d-ae11-7b14d0c39f23)

It should:
 - Allow any signed-in user to write its user-storage
 - If user-storage is not available, it should not render an Alert and fallback to `localStorage` instead.
