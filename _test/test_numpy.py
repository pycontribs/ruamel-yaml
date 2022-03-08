# coding: utf-8

try:
    import numpy  # type: ignore
except:  # NOQA
    numpy = None


def Xtest_numpy() -> None:
    import ruamel.yaml

    if numpy is None:
        return
    data = numpy.arange(10)
    print('data', type(data), data)

    yaml_str = ruamel.yaml.dump(data)  # type: ignore  # needs updating to use buffer
    datb = ruamel.yaml.load(yaml_str)
    print('datb', type(datb), datb)

    print('\nYAML', yaml_str)
    assert data == datb
