from __future__ import absolute_import
from __future__ import print_function

import codecs   # NOQA
import io

from ruamel.yaml.compat import PY2
import ruamel.yaml.reader


def _run_reader(data, verbose):
    try:
        stream = ruamel.yaml.py.reader.Reader(data)
        while stream.peek() != u'\0':
            stream.forward()
    except ruamel.yaml.py.reader.ReaderError as exc:
        if verbose:
            print(exc)
    else:
        raise AssertionError("expected an exception")


def test_stream_error(error_filename, verbose=False):
    with open(error_filename, 'rb') as fp0:
        _run_reader(fp0, verbose)
    with open(error_filename, 'rb') as fp0:
        _run_reader(fp0.read(), verbose)
    for encoding in ['utf-8', 'utf-16-le', 'utf-16-be']:
        try:
            if PY2:
                with open(error_filename, 'rb') as fp0:
                    data = unicode(fp0.read(), encoding)  # NOQA
            else:
                with open(error_filename, 'rb') as fp0:
                    data = fp0.read().decode(encoding)
            break
        except UnicodeDecodeError:
            pass
    else:
        return
    _run_reader(data, verbose)
    with io.open(error_filename, encoding=encoding) as fp:
        _run_reader(fp, verbose)


test_stream_error.unittest = ['.stream-error']

if __name__ == '__main__':
    import test_appliance
    test_appliance.run(globals())
