from fakeclass import FakeClass


class SomeClass:
    def __init__(self):
        ...

    def some_function(self, some_arg, another_arg):
        some_variable = some_arg + another_arg
        return some_variable

    def another_function(self, some_more_arg, even_more_arg):
        modified_arg = some_more_arg * even_more_arg
        returned_obj = self.some_function(modified_arg, some_more_arg)
        return returned_obj


if __name__ == "__main__":
    some_class_instance = SomeClass()
    some_class_instance.some_function("stringLiteral", "anotherStringLiteral")
    variable: str
    some_class_instance.another_function(variable, variable)
    variable = "someFunction"
