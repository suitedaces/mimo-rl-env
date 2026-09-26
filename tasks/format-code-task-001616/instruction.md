**Describe the bug**
When trying to do silent login or prompt=none login /o/authorize redirects to the login screen. 

This is because it oauth2_provider.views.AuthorizationView extends LoginRequiredMixin via BaseAuthorizationView. 


**To Reproduce**
<!-- Steps to reproduce the behavior -->
setup any OIDC silent auth enabled client, I used https://github.com/dopry/svelte-oidc, with the django oauth toolkit and enable the chrome debugger in your browser, login then reload the client. 

You will see a request to http://127.0.0.1:8000/o/authorize/... in an iframe with a 302 Location redirect to  /admin/login?next=/o/authorize/

you will also see in the console `fused to display 'http://127.0.0.1:8000/' in a frame because it set 'X-Frame-Options' to 'deny'.`

**Expected behavior**
<!-- A clear and concise description of what you expected to happen. -->
per https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest


> prompt - OPTIONAL. Space delimited, case sensitive list of ASCII string values that specifies whether the Authorization Server prompts the End-User for reauthentication and consent. The defined values are:
> - none

>   The Authorization Server MUST NOT display any authentication or consent user interface pages. An error is returned if an End-User is not already authenticated or the Client does not have pre-configured consent for the requested Claims or does not fulfill other conditions for processing the request. The error code will typically be login_required, interaction_required, or another code defined in [Section 3.1.2.6](https://openid.net/specs/openid-connect-core-1_0.html#AuthError). This can be used as a method to check for existing authentication and/or consent.

and there should be no xframe deny error. 
 
**Version**
<!-- Version of django-oauth-toolkit -->
25f6de50d4b7287a76c87e1cf511d8f9a61c6faa


<!-- Have you tested with the latest version and/or master branch? -->
<!-- Replace '[ ]' with '[x]' to indicate that. -->
- [X] I have tested with the latest published release and it's still a problem.
- [X] I have tested with the master branch and it's still a problem.

**Additional context**
<!-- Add any other context about the problem here. -->
