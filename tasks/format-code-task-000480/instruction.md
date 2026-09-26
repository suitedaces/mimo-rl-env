### Version


v4.38.2

### Deployment Method


Docker

### Reverse Proxy


Traefik

### Reverse Proxy Version


2.11.0

### Description


In upgrading to 4.38 I changed my Traefik middleware to use the (default provided) `/api/authz/forward-auth` route. Then, I noticed requests to Home Assistant's `/api` were getting a 401 response, despite having valid (for Home Assistant) `Authorization` headers. The error comes from Authelia, even though the request should be bypassed.

### Reproduction


This can be reproduced using something simple like `traefik/whoami`

An example docker-compose.yml:

```yml
services:
  whoami:
    image: traefik/whoami
    labels:
      - traefik.enable=true
      - traefik.http.routers.${COMPOSE_PROJECT_NAME}-whoami.rule=Host(`whoami.${HOMELAB_BASE_DOMAIN}`)
      - traefik.http.routers.${COMPOSE_PROJECT_NAME}-whoami.entrypoints=web,websecure
      - traefik.http.routers.${COMPOSE_PROJECT_NAME}-whoami.middlewares=auth@file
```

where `auth@file` is this Traefik middleware:

```yml
http:
  middlewares:
    auth:
      forwardAuth:
        # Using the internal container + port
        address: http://authelia:9091/api/authz/forward-auth
        trustForwardHeader: true
        authResponseHeaders:
          - Authorization
          - Proxy-Authorization
          - Remote-User
          - Remote-Groups
          - Remote-Email
          - Remote-Name
```

and the `access_control` which should bypass Authelia:

```yml
access_control:
  default_policy: one_factor

  rules:
    - domain: whoami.${HOMELAB_BASE_DOMAIN}
      policy: bypass
```

With Authelia + Traefik + whoami running, now you can try curl:

```sh
# This works:
curl -L https://whoami.${HOMELAB_BASE_DOMAIN}/

# This gets a 401 from Authelia:
curl -L -H 'Authorization: Bearer test' https://whoami.${HOMELAB_BASE_DOMAIN}/
```

### Expectations


Ideally Authelia wouldn't be doing much when the requested route is bypassed.

### Configuration (Authelia)


```yaml
theme: auto

totp:
  issuer: auth.${HOMELAB_BASE_DOMAIN}

authentication_backend:
  password_reset:
    disable: true

  file:
    path: /config/users.yml

access_control:
  default_policy: one_factor
  #default_policy: two_factor

  rules:
    - domain: whoami.${HOMELAB_BASE_DOMAIN}
      policy: bypass

session:
  inactivity: '5m'
  expiration: '1h'
  remember_me: '1M'

  redis:
    host: redis

  cookies:
    - domain: ${HOMELAB_BASE_DOMAIN}
      authelia_url: https://auth.${HOMELAB_BASE_DOMAIN}
      default_redirection_url: https://dashboard.${HOMELAB_BASE_DOMAIN}

storage:
  local:
    path: /output/db.sqlite3

notifier:
  filesystem:
    filename: /output/notifications
```


### Build Information


```shell
Last Tag: v4.38.2
State: tagged clean
Branch: v4.38.2
Commit: 573e79c8d34e118195731424df15d3e2c989495e
Build Number: 27687
Build OS: linux
Build Arch: amd64
Build Compiler: gc
Build Date: Sat, 16 Mar 2024 02:33:12 +1100
Extra:

Go:
    Version: go1.22.1
    Module Path: github.com/authelia/authelia/v4
    Executable Path: github.com/authelia/authelia/v4/cmd/authelia
    Settings:
        -buildmode: pie
        -compiler: gc
        -trimpath: true
        DefaultGODEBUG: httplaxcontentlength=1,httpmuxgo121=1,tls10server=1,tlsrsakex=1,tlsunsafeekm=1
        CGO_ENABLED: 1
        GOARCH: amd64
        GOOS: linux
        GOAMD64: v1
        vcs: git
        vcs.revision: 573e79c8d34e118195731424df15d3e2c989495e
        vcs.time: 2024-03-15T15:24:32Z
        vcs.modified: true
    Dependencies:
        authelia.com/provider/oauth2@v0.1.1 (h1:JHMWB8aieYW++7a+t3RIB0fkxcLMHyT7NUKPEAl6cls=)
        filippo.io/edwards25519@v1.1.0 (h1:FNf4tywRC1HmFuKW5xopWpigGjJKiJSV0Cqo0cJWDaA=)
        github.com/Azure/go-ntlmssp@v0.0.0-20221128193559-754e69321358 (h1:mFRzDkZVAjdal+s7s0MwaRv9igoPqLRdzOLzw/8Xvq8=)
        github.com/Gurpartap/logrus-stack@v0.0.0-20170710170904-89c00d8a28f4 (h1:vdT7QwBhJJEVNFMBNhRSFDRCB6O16T28VhvqRgqFyn8=)
        github.com/andybalholm/brotli@v1.1.0 (h1:eLKJA0d02Lf0mVpIDgYnqXcUn0GqVmEFny3VuID1U3M=)
        github.com/asaskevich/govalidator@v0.0.0-20230301143203-a9d515a09cc2 (h1:DklsrG3dyBCFEj5IhUbnKptjxatkF07cF2ak3yi77so=)
        github.com/authelia/jsonschema@v0.1.7 (h1:RbtTeTG7GiWIrx2A+3O+b33jr/mLlSmqGYyk1w5gLNA=)
        github.com/authelia/otp@v1.0.0 (h1:X6YeBMb16CkW8fFpLBQc0ams+Ed0zw1R/5pfih/1vLU=)
        github.com/beorn7/perks@v1.0.1 (h1:VlbKKnNfV8bJzeqoa4cOKqO6bYr3WgKZxO8Z16+hsOM=)
        github.com/boombuler/barcode@v1.0.1 (h1:NDBbPmhS+EqABEs5Kg3n/5ZNjy73Pz7SIV+KCeqyXcs=)
        github.com/cespare/xxhash/v2@v2.2.0 (h1:DC2CZ1Ep5Y4k3ZQ899DldepgrayRUGE6BBZ/cd9Cj44=)
        github.com/davecgh/go-spew@v1.1.1 (h1:vj9j/u1bqnvCEfJOwUhtlOARqs3+rkHYY13jYWTU97c=)
        github.com/dgraph-io/ristretto@v0.1.1 (h1:6CWw5tJNgpegArSHpNHJKldNeq03FQCwYvfMVWajOK8=)
        github.com/dgryski/go-rendezvous@v0.0.0-20200823014737-9f7001d12a5f (h1:lO4WD4F/rVNCu3HqELle0jiPLLBs70cWOduZpkS1E78=)
        github.com/dlclark/regexp2@v1.4.0 (h1:F1rxgk7p4uKjwIQxBs9oAXe5CqrXlCduYEJvrF4u93E=)
        github.com/duosecurity/duo_api_golang@v0.0.0-20240205144049-bb361ad4ae1c (h1:xFrCg835Y/ig7iWQqyVmGFG5cd1OztnlN3rF64ltEpY=)
        github.com/dustin/go-humanize@v1.0.1 (h1:GzkhY7T5VNhEkwH0PVJgjz+fX1rhBrR7pRT3mDkpeCY=)
        github.com/facebookgo/stack@v0.0.0-20160209184415-751773369052 (h1:JWuenKqqX8nojtoVVWjGfOF9635RETekkoH6Cc9SX0A=)
        github.com/fasthttp/router@v1.5.0 (h1:3Qbbo27HAPzwbpRzgiV5V9+2faPkPt3eNuRaDV6LYDA=)
        github.com/fasthttp/session/v2@v2.5.4 (h1:SeblRaKHYQoVBjJIF1KlZD0F8QX1poA80h/KaLhNo8I=)
        github.com/fsnotify/fsnotify@v1.7.0 (h1:8JEhPFa5W2WU7YfeZzPNqzMP6Lwt7L2715Ggo0nosvA=)
        github.com/fxamacker/cbor/v2@v2.6.0 (h1:sU6J2usfADwWlYDAFhZBQ6TnLFBHxgesMrQfQgk1tWA=)
        github.com/go-asn1-ber/asn1-ber@v1.5.5 (h1:MNHlNMBDgEKD4TcKr36vQN68BA00aDfjIt3/bD50WnA=)
        github.com/go-crypt/crypt@v0.2.19 (h1:9VFKbVCuWH4cQDbjUA6fGiaHx+w0CXI19rHQGTZqESE=)
        github.com/go-crypt/x@v0.2.13 (h1:YUgKO62hIcPz11ViwHZx89g/OJhOis9+kK13ZunWpS0=)
        github.com/go-jose/go-jose/v4@v4.0.1 (h1:QVEPDE3OluqXBQZDcnNvQrInro2h0e4eqNbnZSWqS6U=)
        github.com/go-ldap/ldap/v3@v3.4.6 (h1:ert95MdbiG7aWo/oPYp9btL3KJlMPKnP58r09rI8T+A=)
        github.com/go-sql-driver/mysql@v1.8.0 (h1:UtktXaU2Nb64z/pLiGIxY4431SJ4/dR5cjMmlVHgnT4=)
        github.com/go-viper/mapstructure/v2@v2.0.0-alpha.1 (h1:TQcrn6Wq+sKGkpyPvppOz99zsMBaUOKXq6HSv655U1c=)
        github.com/go-webauthn/webauthn@v0.10.2 (h1:OG7B+DyuTytrEPFmTX503K77fqs3HDK/0Iv+z8UYbq4=)
        github.com/go-webauthn/x@v0.1.9 (h1:v1oeLmoaa+gPOaZqUdDentu6Rl7HkSSsmOT6gxEQHhE=)
        github.com/golang-jwt/jwt/v5@v5.2.1 (h1:OuVbFODueb089Lh128TAcimifWaLhJwVflnrgM17wHk=)
        github.com/golang/glog@v1.2.0 (h1:uCdmnmatrKCgMBlM4rMuJZWOkPDqdbZPnrMXDY4gI68=)
        github.com/golang/protobuf@v1.5.3 (h1:KhyjKVUg7Usr/dYsdSqoFveMYd5ko72D+zANwlG1mmg=)
        github.com/google/go-tpm@v0.9.0 (h1:sQF6YqWMi+SCXpsmS3fd21oPy/vSddwZry4JnmltHVk=)
        github.com/google/uuid@v1.6.0 (h1:NIvaJDMOsjHA8n1jAhLSgzrAzy1Hgr+hNrb57e+94F0=)
        github.com/hashicorp/go-cleanhttp@v0.5.2 (h1:035FKYIWjmULyFRBKPs8TBQoi0x6d9G4xc9neXJWAZQ=)
        github.com/hashicorp/go-retryablehttp@v0.7.5 (h1:bJj+Pj19UZMIweq/iie+1u5YCdGrnxCT9yvm0e+Nd5M=)
        github.com/iancoleman/orderedmap@v0.3.0 (h1:5cbR2grmZR/DiVt+VJopEhtVs9YGInGIxAoMJn+Ichc=)
        github.com/jackc/pgpassfile@v1.0.0 (h1:/6Hmqy13Ss2zCq62VdNG8tM1wchn8zjSGOBJ6icpsIM=)
        github.com/jackc/pgservicefile@v0.0.0-20221227161230-091c0ba34f0a (h1:bbPeKD0xmW/Y25WS6cokEszi5g+S0QxI/d45PkRi7Nk=)
        github.com/jackc/pgx/v5@v5.5.5 (h1:amBjrZVmksIdNjxGW/IiIMzxMKZFelXbUoPNb+8sjQw=)
        github.com/jackc/puddle/v2@v2.2.1 (h1:RhxXJtFG022u4ibrCSMSiu5aOq1i77R3OHKNJj77OAk=)
        github.com/jmoiron/sqlx@v1.3.5 (h1:vFFPA71p1o5gAeqtEAwLU4dnX2napprKtHr7PYIcN3g=)
        github.com/klauspost/compress@v1.17.6 (h1:60eq2E/jlfwQXtvZEeBUYADs+BwKBWURIY+Gj2eRGjI=)
        github.com/knadh/koanf/maps@v0.1.1 (h1:G5TjmUh2D7G2YWf5SQQqSiHRJEjaicvU0KpypqB3NIs=)
        github.com/knadh/koanf/parsers/yaml@v0.1.0 (h1:ZZ8/iGfRLvKSaMEECEBPM1HQslrZADk8fP1XFUxVI5w=)
        github.com/knadh/koanf/providers/confmap@v0.1.0 (h1:gOkxhHkemwG4LezxxN8DMOFopOPghxRVp7JbIvdvqzU=)
        github.com/knadh/koanf/providers/env@v0.1.0 (h1:LqKteXqfOWyx5Ab9VfGHmjY9BvRXi+clwyZozgVRiKg=)
        github.com/knadh/koanf/providers/posflag@v0.1.0 (h1:mKJlLrKPcAP7Ootf4pBZWJ6J+4wHYujwipe7Ie3qW6U=)
        github.com/knadh/koanf/v2@v2.1.0 (h1:eh4QmHHBuU8BybfIJ8mB8K8gsGCD/AUQTdwGq/GzId8=)
        github.com/mattn/go-sqlite3@v1.14.22 (h1:2gZY6PC6kBnID23Tichd1K+Z0oS6nE/XwU+Vz/5o4kU=)
        github.com/mitchellh/copystructure@v1.2.0 (h1:vpKXTN4ewci03Vljg/q9QvCGUDttBOGBIa15WveJJGw=)
        github.com/mitchellh/mapstructure@v1.5.0 (h1:jeMsZIYE/09sWLaz43PL7Gy6RuMjD2eJVyuac5Z2hdY=)
        github.com/mitchellh/reflectwalk@v1.0.2 (h1:G2LzWKi524PWgd3mLHV8Y5k7s6XUvT0Gef6zxSIeXaQ=)
        github.com/mohae/deepcopy@v0.0.0-20170929034955-c48cc78d4826 (h1:RWengNIwukTxcDr9M+97sNutRR1RKhG96O6jWumTTnw=)
        github.com/ory/herodot@v0.10.3-0.20230807143059-27cd6936499b (h1:AEUyF55UrqTuhJh72I9azACdJrRrDBBjK/XWgVxuQvY=)
        github.com/ory/x@v0.0.616 (h1:iaojp7MvFW1cdirSZFK/XeuJvyhUEVXQdY61bmIOkzk=)
        github.com/philhofer/fwd@v1.1.2 (h1:bnDivRJ1EWPjUIRXV5KfORO897HTbpFAQddBdE8t7Gw=)
        github.com/pkg/errors@v0.9.1 (h1:FEBLx1zS214owpjy7qsBeixbURkuhQAwrK5UwLGTwt4=)
        github.com/pmezard/go-difflib@v1.0.0 (h1:4DBwDE0NGyQoBHbLQYPwSUPoCMWR5BEzIk/f1lZbAQM=)
        github.com/prometheus/client_golang@v1.19.0 (h1:ygXvpU1AoN1MhdzckN+PyD9QJOSD4x7kmXYlnfbA6JU=)
        github.com/prometheus/client_model@v0.5.0 (h1:VQw1hfvPvk3Uv6Qf29VrPF32JB6rtbgI6cYPYQjL0Qw=)
        github.com/prometheus/common@v0.48.0 (h1:QO8U2CdOzSn1BBsmXJXduaaW+dY/5QLjfB8svtSzKKE=)
        github.com/prometheus/procfs@v0.12.0 (h1:jluTpSng7V9hY0O2R9DzzJHYb2xULk9VTR1V1R/k6Bo=)
        github.com/redis/go-redis/v9@v9.5.1 (h1:H1X4D3yHPaYrkL5X06Wh6xNVM/pX0Ft4RV0vMGvLBh8=)
        github.com/savsgio/gotils@v0.0.0-20240303185622-093b76447511 (h1:KanIMPX0QdEdB4R3CiimCAbxFrhB3j7h0/OvpYGVQa8=)
        github.com/sirupsen/logrus@v1.9.3 (h1:dueUQJ1C2q9oE3F7wvmSGAaVtTmUizReu6fjN8uqzbQ=)
        github.com/spf13/cobra@v1.8.0 (h1:7aJaZx1B85qltLMc546zn58BxxfZdR/W22ej9CFoEf0=)
        github.com/spf13/pflag@v1.0.5 (h1:iy+VFUOCP1a+8yFto/drg2CJ5u0yRoB7fZw3DKv/JXA=)
        github.com/stretchr/testify@v1.9.0 (h1:HtqpIVDClZ4nwg75+f6Lvsy/wHu+3BoSGCbBAcpTsTg=)
        github.com/tinylib/msgp@v1.1.9 (h1:SHf3yoO2sGA0veCJeCBYLHuttAVFHGm2RHgNodW7wQU=)
        github.com/trustelem/zxcvbn@v1.0.1 (h1:mp4JFtzdDYGj9WYSD3KQSkwwUumWNFzXaAjckaTYpsc=)
        github.com/valyala/bytebufferpool@v1.0.0 (h1:GqA5TC/0021Y/b9FG4Oi9Mr3q7XYx6KllzawFIhcdPw=)
        github.com/valyala/fasthttp@v1.52.0 (h1:wqBQpxH71XW0e2g+Og4dzQM8pk34aFYlA1Ga8db7gU0=)
        github.com/wneessen/go-mail@v0.4.1 (h1:m2rSg/sc8FZQCdtrV5M8ymHYOFrC6KJAQAIcgrXvqoo=)
        github.com/x448/float16@v0.8.4 (h1:qLwI1I70+NjRFUR3zs1JPUCgaCXSh3SW62uAKT1mSBM=)
        golang.org/x/crypto@v0.21.0 (h1:X31++rzVUdKhX5sWmSOFZxx8UW/ldWx55cbf08iNAMA=)
        golang.org/x/net@v0.22.0 (h1:9sGLhx7iRIHEiX0oAJ3MRZMUCElJgy7Br1nO+AMN3Tc=)
        golang.org/x/oauth2@v0.18.0 (h1:09qnuIAgzdx1XplqJvW6CQqMCtGZykZWcXzPMPUusvI=)
        golang.org/x/sync@v0.6.0 (h1:5BMeUDZ7vkXGfEr1x9B4bRcTH4lpkTkpdh0T/J+qjbQ=)
        golang.org/x/sys@v0.18.0 (h1:DBdB3niSjOA/O0blCZBqDefyWNYveAYMNF1Wum0DYQ4=)
        golang.org/x/term@v0.18.0 (h1:FcHjZXDMxI8mM3nwhX9HlKop4C0YQvCVCdwYl2wOtE8=)
        golang.org/x/text@v0.14.0 (h1:ScX5w1eTa3QqT8oi6+ziP7dTV1S2+ALU0bI+0zXKWiQ=)
        google.golang.org/genproto/googleapis/rpc@v0.0.0-20231106174013-bbf56f31fb17 (h1:Jyp0Hsi0bmHXG6k9eATXoYtjd6e2UzZ1SCn/wIupY14=)
        google.golang.org/grpc@v1.59.0 (h1:Z5Iec2pjwb+LEOqzpB2MR12/eKFhDPhuqW91O+4bwUk=)
        google.golang.org/protobuf@v1.33.0 (h1:uNO2rsAINq/JlFpSdYEKIZ0uKD/R9cpdv0T+yoGwGmI=)
        gopkg.in/yaml.v3@v3.0.1 (h1:fxVm/GzAzEWqLHuvctI91KS9hhNmmWOoWu0XTYJS7CA=)
```


### Logs (Authelia)


```shell
redis-1     | 1:C 16 Mar 2024 17:48:35.500 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
redis-1     | 1:C 16 Mar 2024 17:48:35.500 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis-1     | 1:C 16 Mar 2024 17:48:35.500 * Redis version=7.2.4, bits=64, commit=00000000, modified=0, pid=1, just started
redis-1     | 1:C 16 Mar 2024 17:48:35.500 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis-1     | 1:M 16 Mar 2024 17:48:35.500 * monotonic clock: POSIX clock_gettime
redis-1     | 1:M 16 Mar 2024 17:48:35.500 * Running mode=standalone, port=6379.
redis-1     | 1:M 16 Mar 2024 17:48:35.501 * Server initialized
redis-1     | 1:M 16 Mar 2024 17:48:35.501 * Loading RDB produced by version 7.2.4
redis-1     | 1:M 16 Mar 2024 17:48:35.501 * RDB age 5 seconds
redis-1     | 1:M 16 Mar 2024 17:48:35.501 * RDB memory usage when created 0.95 Mb
redis-1     | 1:M 16 Mar 2024 17:48:35.501 * Done loading RDB, keys loaded: 12, keys expired: 0.
redis-1     | 1:M 16 Mar 2024 17:48:35.501 * DB loaded from disk: 0.000 seconds
redis-1     | 1:M 16 Mar 2024 17:48:35.501 * Ready to accept connections tcp
whoami-1    | 2024/03/16 17:48:35 Starting up on port 80
authelia-1  | time="2024-03-16T14:48:35-03:00" level=debug msg="Process user information" gid=1000 uid=1000
authelia-1  | time="2024-03-16T14:48:35-03:00" level=warning msg="Configuration: identity_providers: oidc: clients: client 'he9CQnNpTG_i3geR2OnIgjBtuvMOSZI3': option 'scopes' should only have the values 'offline_access' or 'offline' if the client is also configured with a 'response_type' such as 'code', 'code id_token', 'code token', or 'code id_token token' which respond with authorization codes"
authelia-1  | time="2024-03-16T14:48:35-03:00" level=warning msg="Configuration: identity_providers: oidc: clients: client 'TOs7SahclSI1f8IlvV3vliWz5VT8iZvK': option 'scopes' should only have the values 'offline_access' or 'offline' if the client is also configured with a 'response_type' such as 'code', 'code id_token', 'code token', or 'code id_token token' which respond with authorization codes"
authelia-1  | time="2024-03-16T14:48:35-03:00" level=warning msg="Configuration: identity_providers: oidc: clients: warnings for clients above indicate deprecated functionality and it's strongly suggested these issues are checked and fixed if they're legitimate issues or reported if they are not as in a future version these warnings will become errors"
authelia-1  | time="2024-03-16T14:48:35-03:00" level=info msg="Authelia v4.38.2 is starting"
authelia-1  | time="2024-03-16T14:48:35-03:00" level=info msg="Log severity set to info"
authelia-1  | time="2024-03-16T14:48:35-03:00" level=info msg="Storage schema is being checked for updates"
authelia-1  | time="2024-03-16T14:48:35-03:00" level=info msg="Storage schema is already up to date"
authelia-1  | time="2024-03-16T14:48:35-03:00" level=info msg="Startup complete"
authelia-1  | time="2024-03-16T14:48:35-03:00" level=info msg="Listening for non-TLS connections on '[::]:9091' path '/'" server=main service=server
authelia-1  | time="2024-03-16T14:48:41-03:00" level=error msg="Error occurred while attempting to authenticate a request" error="invalid scheme: scheme with name 'bearer' isn't available on this endpoint" method=GET path=/api/authz/forward-auth remote_ip=10.0.1.76 stack="github.com/authelia/authelia/v4/internal/handlers/handler_authz.go:63  (*Authz).Handler\ngithub.com/authelia/authelia/v4/internal/middlewares/bridge.go:54      handleRouter.(*BridgeBuilder).Build.func1.1\ngithub.com/authelia/authelia/v4/internal/middlewares/headers.go:12     SecurityHeaders.func1\ngithub.com/fasthttp/router@v1.5.0/router.go:441                        (*Router).Handler\ngithub.com/authelia/authelia/v4/internal/middlewares/log_request.go:14 handleRouter.LogRequest.func40\ngithub.com/authelia/authelia/v4/internal/middlewares/errors.go:38      RecoverPanic.func1\ngithub.com/valyala/fasthttp@v1.52.0/server.go:2374                     (*Server).serveConn\ngithub.com/valyala/fasthttp@v1.52.0/workerpool.go:224                  (*workerPool).workerFunc\ngithub.com/valyala/fasthttp@v1.52.0/workerpool.go:196                  (*workerPool).getCh.func1\nruntime/asm_amd64.s:1695                                               goexit"
```


### Logs (Proxy / Application)


_No response_

### Documentation


_No response_

### Pre-Submission Checklist


- [X] I agree to follow the [Code of Conduct](http://www.authelia.com/code-of-conduct)

- [X] This is a bug report and not a support request

- [X] I have read the security policy and this bug report is not a security issue or security related issue

- [X] I have either included the complete configuration file or I am sure it's unrelated to the configuration

- [X] I have either included the complete debug / trace logs or the output of the build-info command if the logs are not relevant

- [X] I have provided all of the required information in full with the only alteration being reasonable sanitization in accordance with the [Troubleshooting Sanitization](https://www.authelia.com/r/sanitize) reference guide

- [X] I have checked for related proxy or application logs and included them if available

- [X] I have checked for related issues and checked the documentation
