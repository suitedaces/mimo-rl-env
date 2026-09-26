**Is your feature request related to a problem? Please describe.**
Using the websocket server with web browsers causes inconsistent behavior with using tracking cookies because of the attributes (or lack of) for the cookie. 

**Describe the solution you'd like**
I would like the ability to modify the http.Cookie attributes presented by the websocket server when tracking cookies are enabled.  Specifically the ability to set `Secure: true` and `SameSite: http.SameSiteNoneMode`

**Describe alternatives you've considered**
For now, we are cloning the project, hard coding the http.Cookie settings in `func (s *WebsocketServer) ServeHTTP(w http.ResponseWriter, r *http.Request)` and redirecting in go.mod.

**Additional context**
I'd expect the configuration to live as new fields on `WebsocketServer`, named something like `TrackingCookieSecureAttribute` and `TrackingCookieSameSiteAttribute`.
