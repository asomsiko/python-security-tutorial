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

TODO: demo how pickle is used for good

Tip: Point your attention to security disclamers in Python docs:\
[Pickle documentation]: _"Warning The pickle module is not intended to be secure
against erroneous or maliciously constructed data. Never unpickle data received
from an untrusted or unauthenticated source."_

Pickle can also handle the module imports and execute functions:

``` python
import pickle
pickle.loads(b"cos\nsystem\n(S'echo hello world'\ntR.")
```

If you brave enough and need to use pickle here some techniques can reduce
security risks:

1. When loading from disk ensure strict permissions

2. When loading from network use cryptographic signature


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

TODO: demo how restricted pickler can be used

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

TODO: Explain that loading array of objects is not safe and repeat strict
permission or crypto verification reuirements

## Yaml

TODO: general introduction to yaml

TODO: basic types

TODO: advanced python types

yaml.load is as powerfull as pickle. Use yaml.safe_load when loading yaml files.
yaml can construct arbitray python objects and yaml.safe_load limits this to
simple Python objects like lists and integers.

``` python
import yaml
yaml.safe_load(...)
```

You can check yourself with `yaml.safe_dump()` which only creates safe yaml
files.

PyYAML provide a hooks and helper classes to use full power of PyYAML safely.

To declare you robject can be loaded safely you can inherit it from
yaml.YAMLObject and set `yaml_loader=yaml.SafeLoader`.

``` python
import yaml

class Monster(yaml.YAMLObject):
    yaml_tag = u'!Monster'
    yaml_loader = yaml.SafeLoader
    yaml_dumper = yaml.SafeDumper
    def __init__(self, name, hp, ac, attacks):
        self.name = name
        self.hp = hp
        self.ac = ac
        self.attacks = attacks
print(yaml.safe_dump(Monster(name='Cave lizard', hp=[3,6], ac=16, attacks=['BITE','HURT'])))
print(yaml.safe_load('!Monster {ac: 16, attacks: [BITE, HURT], hp: [3, 6], name: Cave lizard}'))
```

What is you need advanced scalar construction?

``` yaml
tests:
- mark: pytest.mark.xfail
  name: feature_A_exists
- name: feature_B_exists
```

Lets check what pytest mark is:

``` python
import pytest

print(pytest.mark.xfail)
print(pytest.mark.__getattr__('xfail'))
```

Now we can register constructor and representer:

``` python
import re
import yaml
import pytest

def pytest_mark_constructor(loader, node):
    value = loader.construct_scalar(node)
    return pytest.mark.__getattr__(value.rsplit(".", 1)[1])
def pytest_mark_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', u'pytest.mark.%s' % data.name)
yaml.add_constructor(u'!pytest.mark', pytest_mark_constructor, Loader=yaml.SafeLoader)
yaml.add_implicit_resolver(u'!pytest.mark', re.compile(r'^pytest\.mark\.[a-zA-Z]+$'))
yaml.add_representer(type(pytest.mark.xfail), pytest_mark_representer, Dumper=yaml.SafeDumper)

print(yaml.safe_load('mark: pytest.mark.xfail'))
print(yaml.safe_load('mark: "pytest.mark.xfail"'))

print(yaml.safe_dump({'tests':[{'name':'feature_A_exists', 'mark':pytest.mark.xfail}, {'name':'feature_B_exists'}]}))
```

[Pickle documentation]:https://docs.python.org/3/library/pickle.html