from io import StringIO
from tempfile import NamedTemporaryFile
from unittest import TestCase

from testfixtures import compare, ShouldRaise

from configurator import Config


class InstantiationTests(TestCase):

    def test_empty(self):
        config = Config()
        # make sure empty dict is default:
        config.merge(Config({'x': 1}))
        compare(config.x, 1)

    def test_path(self):
        with NamedTemporaryFile() as source:
            source.write('{"x": 1}')
            source.flush()
            config = Config.from_file(source.name)
        compare(config.x, expected=1)

    def test_stream(self):
        with StringIO(u'{"x": 1}') as source:
            config = Config.from_stream(source)
        compare(config.x, expected=1)

    def test_dict(self):
        config = Config(dict(x=1))
        compare(config.x, expected=1)

    def test_list(self):
        config = Config([1, 2])
        compare(config[0], expected=1)
        compare(config[1], expected=2)
        compare(list(config), expected=[1, 2])

    def test_int(self):
        # not very useful...
        config = Config(1)


class MergeTests(TestCase):

    def test_empty(self):
        config = Config()
        config.merge(Config())
        # make sure empty dict is default:
        config.merge(Config({'x': 1}))
        compare(config.x, 1)

    def test_non_config(self):
        config = Config()
        with ShouldRaise(TypeError("'foo' is not a Config instance")):
            config.merge('foo')

    def test_dict_to_dict(self):
        config = Config()
        config.merge(Config(dict(x=1)))
        compare(config.x, expected=1)

    def test_list_to_list(self):
        config = Config([1, 2])
        config.merge(Config([3, 4]))
        compare(config[0], expected=1)
        compare(config[2], expected=3)
        compare(list(config), expected=[1, 2, 3, 4])