# Handing secrets

"*Don't rool your own crypto*"

To work with secret tokens or password use cryptography functions, otherwise
your secrets can leak. Managing secrets inlude generating, storing, verifying
and retaining it.

## Random numbers

You might need random sequences if, for example, you are implementing
authentication or password reset.

```python
import random
random.seed(1)
print(random.random())
print(random.random())
```

Not all random numbers are cryptographycally secure. For cryptography purposes
use [secrets](https://docs.python.org/3/library/secrets.html) module.

``` python
import secrets
secrets.token_bytes()
```

Note: a random token size is not part of API contract - it can change any time
evem with path update.

TODO: How big shoudl be the secret to protect from
[brute-force](https://en.wikipedia.org/wiki/Brute-force_attack)?

How to deal with URLs?

``` python
import secrets
secrets.token_hex()
```

but urlsafe method gives your shorter string.

``` import secrets secrets.token_urlsafe() ```

## Comparing secret tokens

Checking if a token you've just received matches one you have generated before
looks stright forward, but only on first sight. The operations with a secrets
need to be resistant to [timing
attacks](https://codahale.com/a-lesson-in-timing-attacks/).

TODO: Lab on timing attack with partial code [Web
example](https://sqreen.github.io/DevelopersSecurityBestPractices/timing-attack/python)

Use `secrets.compare_digest(a, b)` to check if secret strings are equal. This
function do comparison in a way to reduce a risk of timig attacks.

## Storing passwords

Never store passwords or other secrets in a recoverable format whether it plain
or encrypted.

When storing a passwords think about protecting your storage from brute force
attacks. The first consideration is that since brute force attacks require many
iterations of guessing a password the password check shoudl be slow enough. And
the second consideraion is that similar passwords shoud not look the same.

Python offers `hashlib.pbkdf2_hmac(hash_name, password, salt, iterations,
dklen=None)` function for stroring a password.
