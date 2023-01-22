from fakeClass import FakeClass


class SomeClass:
    def __init__(self):
        ...

    def someFunction(self, someArg, anotherArg):
        someVariable = someArg + anotherArg
        return someVariable

    def anotherFunction(self, someMoreArg, evenMoreArg):
        modifiedArg = someMoreArg * evenMoreArg
        returnedObj = self.someFunction(modifiedArg, someMoreArg)
        return returnedObj


if __name__ == "__main__":
    someClassInstance = SomeClass()
    someClassInstance.someFunction("stringLiteral", "anotherStringLiteral")
    variable: str
    someClassInstance.anotherFunction(variable, variable)
    variable = "someFunction"
