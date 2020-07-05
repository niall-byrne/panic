# Environment Variables

Each "Environment" has two sets of inputs for it's environment variables.
Only the local environment has it's `base` settings checked in, never it's `secrets`.

**Never check the secrets file into git.**

Reach out to niall-byrne, for assistance with configuring the secrets.

## Base Environment Variables

The first is a `base` environment file:
- local.env

This file should contain the following non-privileged secrets:

#### Local Dev Specific Configuration
```bash
PYTHONPATH=/app/panic/
GIT_HOOKS=1
GIT_HOOKS_PROTECTED_BRANCHES="^(master|stage)"
```

#### Local Django and Postgresql Configuration
```bash
POSTGRES_USER=dbuser
POSTGRES_PASSWORD=supersecret
POSTGRES_DB=panic
POSTGRES_HOSTNAME=db
DJANGO_SECRET_KEY=hf8fsg-7k$16$@v69l)1y=hmrkd#czed9b%h20z)^#^gel-@*8
DJANGO_JWT_SECRET_KEY=LKEtEEk1rXLFkXqzIbFeGpCLBTskOOiUmiAXflLBXKorvqmtOvq05ZyhUPcIwoL6fZHs5bcU6w7UWPRBHOwPAXE1VI98YJY5UBvIM4zdohfJxtnG923JI9Ge
DJANGO_ENVIRONMENT=local
```

## Secret Environment Variables

In addition to the `base` files, each environment has a set of `secret` files that need to be kept out of git:
- local_secret.env

## This files contain the following information
```
EMAIL_ADDRESS=<gmail account for sending emails>
EMAIL_PASSWORD=<gmail account password>
GOOGLE_ID=<google service account for oauth logins>
GOOGLE_SECRET_KEY=<google client key for oauth logins>
FACEBOOK_ID=<facebook app id for oauth logins>
FACEBOOK_SECRET_KEY=<facebook app secret for oauth logins>
BASE_URL="http://localhost:8080"
```

(gmail will of course be switched out with a proper vendor solution, when/if the need arises.)
