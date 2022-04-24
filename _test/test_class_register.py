# coding: utf-8

"""
testing of YAML.register_class and @yaml_object
"""

from typing import Any
from ruamel.yaml.comments import TaggedScalar, CommentedMap

from roundtrip import YAML


class User0:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age


class User1:
    yaml_tag = '!user'

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    @classmethod
    def to_yaml(cls, representer: Any, node: Any) -> Any:
        return representer.represent_scalar(cls.yaml_tag, '{.name}-{.age}'.format(node, node))

    @classmethod
    def from_yaml(cls, constructor: Any, node: Any) -> Any:
        return cls(*node.value.split('-'))


class TestRegisterClass:
    def test_register_0_rt(self) -> None:
        yaml = YAML()
        yaml.register_class(User0)
        ys = """
        - !User0
          name: Anthon
          age: 18
        """
        d = yaml.load(ys)
        assert isinstance(d[0], User0)  # and is not a TaggedScalar
        yaml.dump(d, compare=ys, unordered_lines=True)

    def test_register_0_safe(self) -> None:
        # default_flow_style = None
        yaml = YAML(typ='safe')
        yaml.register_class(User0)
        ys = """
        - !User0 {age: 18, name: Anthon}
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_register_0_unsafe(self) -> None:
        # default_flow_style = None
        yaml = YAML(typ='unsafe')
        yaml.register_class(User0)
        ys = """
        - !User0 {age: 18, name: Anthon}
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_register_1_rt(self) -> None:
        yaml = YAML()
        yaml.register_class(User1)
        ys = """
        - !user Anthon-18
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_register_1_safe(self) -> None:
        yaml = YAML(typ='safe')
        yaml.register_class(User1)
        ys = """
        [!user Anthon-18]
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_register_1_unsafe(self) -> None:
        yaml = YAML(typ='unsafe')
        yaml.register_class(User1)
        ys = """
        [!user Anthon-18]
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_check_register_0_on_instance(self) -> None:
        yaml = YAML()
        ys = """
        - !User0
          name: Anthon
          age: 18
        - !user my name is Giovanni Giorgio
        """
        d = yaml.load(ys)
        assert isinstance(d[0], CommentedMap)
        assert isinstance(d[1], TaggedScalar)
        yaml.dump(d, compare=ys, unordered_lines=True)

    def test_check_register_1_on_instance(self) -> None:
        yaml = YAML()
        yaml.register_class(User1)
        ys = """
        - !User0
          name: Anthon
          age: 18
        - !user anthon-18
        """
        d = yaml.load(ys)
        assert isinstance(d[0], CommentedMap)
        assert not isinstance(d[1], TaggedScalar)
        yaml.dump(d, compare=ys, unordered_lines=True)

    def test_check_register_2_on_instance(self) -> None:
        yaml = YAML()
        yaml.register_class(User1)
        ys = """
        - !User0
          name: Anthon
          age: 18
        - !user anthon-18
        """
        yaml = YAML()
        d = yaml.load(ys)
        assert isinstance(d[0], CommentedMap)
        assert isinstance(d[1], TaggedScalar)
        yaml.dump(d, compare=ys, unordered_lines=True)


class TestDecorator:
    def test_decorator_implicit(self) -> None:
        from ruamel.yaml import yaml_object

        yml = YAML()

        @yaml_object(yml)
        class User2:
            def __init__(self, name: str, age: int) -> None:
                self.name = name
                self.age = age

        ys = """
        - !User2
          name: Anthon
          age: 18
        """
        d = yml.load(ys)
        yml.dump(d, compare=ys, unordered_lines=True)

    def test_decorator_explicit(self) -> None:
        from ruamel.yaml import yaml_object

        yml = YAML()

        @yaml_object(yml)
        class User3:
            yaml_tag = '!USER'

            def __init__(self, name: str, age: int) -> None:
                self.name = name
                self.age = age

            @classmethod
            def to_yaml(cls, representer: Any, node: Any) -> Any:
                return representer.represent_scalar(
                    cls.yaml_tag, '{.name}-{.age}'.format(node, node)
                )

            @classmethod
            def from_yaml(cls, constructor: Any, node: Any) -> Any:
                return cls(*node.value.split('-'))

        ys = """
        - !USER Anthon-18
        """
        d = yml.load(ys)
        yml.dump(d, compare=ys)
