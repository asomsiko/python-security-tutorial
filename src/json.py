import re
import yaml
import pytest


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

print(yaml.dump(pytest.mark.xfail, default_flow_style=True))
print(pytest.mark.xfail)
print(pytest.mark.__getattr__('xfail'))


def pytest_mark_constructor(loader, node):
    value = loader.construct_scalar(node)
    return pytest.mark.__getattr__(value.rsplit(".", 1)[1])


def pytest_mark_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', u'pytest.mark.%s' % data.name)


yaml.add_constructor(u'!pytest.mark', pytest_mark_constructor, Loader=yaml.SafeLoader)
yaml.add_implicit_resolver(u'!pytest.mark', re.compile(r'^pytest\.mark\.[a-zA-Z]+$'))
yaml.add_representer(type(pytest.mark.xfail), pytest_mark_representer, Dumper=yaml.SafeDumper)

print(pytest.mark.__getattr__('xfail'))
print(yaml.safe_load('mark: pytest.mark.xfail'))
print(yaml.safe_load('mark: "pytest.mark.xfail"'))
print(yaml.safe_dump(
    {'tests': [{'name': 'feature_A_exists', 'mark': pytest.mark.xfail}, {'name': 'feature_B_exists'}]}))
print(yaml.safe_load(yaml.safe_dump({'mark': pytest.mark.xfail})))
print(yaml.safe_dump(yaml.safe_load('mark: pytest.mark.xfail')))
