Change default login method to POST
Hello everyone,

I really liked the application, however, I saw that the method for logging in with email and password uses the GET method.

I know that being in secure SSL connection this data is encrypted, however, according to the current Data Protection Laws, the login data is in the request log on the server, this is not at all interesting.

Imagine Parse's paid consumer services, the network administrator will have access to all users and user passwords. This is not cool.

Therefore, I hereby suggest changing the Login class with email and password to use the POST method.

The following image link of what I am explaining.

[https://ibb.co/Y0Q1j3P](https://ibb.co/Y0Q1j3P)
