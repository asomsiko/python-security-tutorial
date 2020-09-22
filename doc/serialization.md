# Safe de-serializaion

Insecure object deserialization a vulnerability allows to an attacker to abuse
application logic, deny service, or execute arbitrary code when an object being
deserialized

- Don't compile and run untrusted pull request
- Don't load pickle files you found on a street

## Pickle

The `pickle` is a default module for python object serialization and
de-serialization. It convertsthe whole python objects hierarhy into a byte
stream and back.

Tip: Point your attention to security disclamers in Python docs:\
_"Warning The pickle module is not intended to be secure against erroneous or
maliciously constructed data. Never unpickle data received from an untrusted or
unauthenticated source."_

If you brave enough and need to use pickle here some techniques can reduce
security risks:

1. When loading from disk ensure strict permissions

2. When loading from network use cryptographic signature

Pickle can handle the module imports and execute functions:

``` python
import pickle
pickle.loads(b"cos\nsystem\n(S'echo hello world'\ntR.")
```

The solution to protect here is to use restrict globals can be called.

``` python
import builtins
import io
import pickle

safe_builtins = {
    'range',
    'complex',
    'set',
    'frozenset',
    'slice',
}

class RestrictedUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        # Only allow safe classes from builtins.
        if module == "builtins" and name in safe_builtins:
            return getattr(builtins, name)
        # Forbid everything else.
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
                                     (module, name))

def restricted_loads(s):
    """Helper function analogous to pickle.loads()."""
    return RestrictedUnpickler(io.BytesIO(s)).load()
```

At the end whis will not ptotect you. Dedicated hacker can always find a way.
Avoid using pickle. Consider JSON or protobuf as secure alternatives.

[python-can-i-safely-unpickle-untrusted-data](https://stackoverflow.com/questions/25353753/python-can-i-safely-unpickle-untrusted-data)

[reverse enginnering pickle](https://hackmd.io/@2KUYNtTcQ7WRyTsBT7oePg/BycZwjKNX?print-pdf#/)

## Numpy

Saving and loading numpy with `allow_pickle=False`

```python
import numpy as np
with np.load(path, allow_pickle=False) as data:
    print(data)
```

TODO: Loading array of objects

## Yaml

yaml.load is as powerfull as pickle. Use yaml.safe_load when loading yaml files.
yaml can construct arbitray python objects and yaml.safe_load limits this to
simple Python objects like lists and integers.

``` python
import yaml
yaml.safe_load(...)
```

You can check yourself with `yaml.safe_dump()` which only creates safe yaml
files.

TODO: extending safe objects: A python object can be marked as safe and thus be
recognized by yaml.safe_load. To do this, derive it from yaml.YAMLObject (as
explained in section Constructors, representers, resolvers) and explicitly set
its class property yaml_loader to yaml.SafeLoader.
