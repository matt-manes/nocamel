import shutil
from pathlib import Path

import pytest

import nocamel

root = Path(__file__).parent


class MockArgs:
    def __init__(self):
        self.source_to_convert = [root / "someClass.py"]
        self.extra_files = [root / "readme.md"]
        self.lower_module_names = True
        self.convert_file_name = True
        self.recursive = False


def test_nocamel_get_args():
    ...


def test_nocamel_convert_string():
    camel_string = "someStringInCamelCaseHTTP"
    assert nocamel.convert_string(camel_string) == "some_string_in_camel_case_HTTP"


def test_nocamel_main():
    shutil.copy(str(root / "camel_case_dont_modify.py"), str(root / "someClass.py"))
    shutil.copy(
        str(root / "camel_case_fake_readme_dont_modify.md"), str(root / "readme.md")
    )
    nocamel.main(MockArgs())
    case_pairs = [
        ("someFunction", "some_function"),
        ("anotherFunction", "another_function"),
        ("fakeClass", "fakeclass"),
        ("someArg", "some_arg"),
        ("anotherArg", "another_arg"),
        ("someMoreArg", "some_more_arg"),
        ("evenMoreArg", "even_more_arg"),
        ("returnedObj", "returned_obj"),
        ("modifiedArg", "modified_arg"),
        ("someClassInstance", "some_class_instance"),
    ]
    assert (root / "some_class.py").exists()
    content = (root / "some_class.py").read_text()
    assert "SomeClass" in content
    assert case_pairs[0][0] not in content[: content.find("variable")]
    for pair in case_pairs[1:]:
        assert pair[0] not in content and pair[1] in content
    assert 'variable = "someFunction"' in content
    assert (
        """ f"{variable_name} variableName {variable_name + variable_name_two * 'variableName' / 'variableNameThree' % 'someString'}" """.strip()
        in content
    )

    readme = (root / "readme.md").read_text()
    assert "SomeClass" in readme
    for pair in [("someClass", "some_class")] + case_pairs[:2]:
        assert pair[0] not in readme and pair[1] in readme
    assert not (root / "someClass.py").exists()


def test_nocamel_convert_fstring_variables():
    fstring = """f"{variableName} variableName {variableName + variableNameTwo * 'variableName' / 'variableNameThree' % 'someString'}" """.strip()
    names = ["variableName", "variableNameTwo"]
    print()
    print(fstring)
    print(nocamel.convert_fstring_variables(fstring, names))
    print(
        """f"{variable_name} variableName {variable_name + variable_name_two * 'variableName' / 'variableNameThree' % 'someString'}" """.strip()
    )
    assert (
        nocamel.convert_fstring_variables(fstring, names)
        == """f"{variable_name} variableName {variable_name + variable_name_two * 'variableName' / 'variableNameThree' % 'someString'}" """.strip()
    )
