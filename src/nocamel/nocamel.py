import argparse
import tokenize
from pathlib import Path


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--source_to_convert",
        type=str,
        default=None,
        help=""" Source file or directory to convert.
                        If None, all .py files in current working directory
                        will be converted.""",
    )

    parser.add_argument(
        "-ef",
        "--extra_files",
        type=str,
        nargs="*",
        default=[],
        help=""" Change the names in these non .py files as well. """,
    )

    parser.add_argument(
        "-lmn",
        "--lower_module_names",
        action="store_true",
        help=""" Change module import names to lower case. """,
    )

    parser.add_argument(
        "-cfn",
        "--convert_file_name",
        action="store_true",
        help=""" Convert the file name to snake case and delete the origninal. """,
    )

    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help=""" If -s/--source is None or a directory, convert all .py files
        including those in subdirectories.""",
    )

    args = parser.parse_args()
    if not args.source_to_convert:
        args.source_to_convert = Path.cwd()
    else:
        args.source_to_convert = Path(args.source_to_convert)
    if args.source_to_convert.is_dir():
        args.source_to_convert = list(
            args.source_to_convert.glob("**/*.py" if args.recursive else "*.py")
        )
    else:
        args.source_to_convert = [args.source_to_convert]
    args.extra_files: list[Path] = [Path(file) for file in args.extra_files]

    return args


def convert_string(camel_string: str) -> str:
    """Converts a camel case string to a PEP compliant snake case string."""
    snake_string = ""
    for i, ch in enumerate(camel_string):
        if (
            0 < i < (len(camel_string) - 1)
            and ch.isupper()
            and camel_string[i - 1].islower()
        ):
            if camel_string[i + 1].isupper():
                snake_string += f"_{ch}"
            else:
                snake_string += f"_{ch.lower()}"
        else:
            snake_string += ch
    return snake_string


def convert_fstring_variables(fstring: str, names: list[str]) -> str:
    """Converts names within {} of f-strings to snake case
    while leaving the rest of the string literal as is.

    :param fstring: The string to convert.

    :param names: List of token names.
    If a symbol is inside {}, but not in token names it will be unaltered.
    """
    startdex = 0
    stopdex = 0
    for _ in range(fstring.count("{")):
        startdex = fstring.find("{", stopdex)
        stopdex = fstring.find("}", startdex)
        bracket_contents = fstring[startdex + 1 : stopdex]
        variables = bracket_contents.split()
        for i, variable in enumerate(variables):
            if (
                "'" not in variable
                and '"' not in variable
                and variable in names
                and not variable[0].isupper()
            ):
                variables[i] = convert_string(variable)
        fstring = fstring[: startdex + 1] + " ".join(variables) + fstring[stopdex:]
    return fstring


def main(args: argparse.Namespace = None):
    if not args:
        args = get_args()
    for file in args.source_to_convert:
        content = file.read_text()
        modules = []
        with file.open("r") as f:
            tokens = list(tokenize.generate_tokens(f.readline))
        all_names = [token.string for token in tokens if token.type == 1]
        modified_tokens = []
        for token in tokens:
            if token.type == 1 and not token.string[0].isupper():
                try:
                    if (
                        "import " in token.line
                        and token.line.split()[1].strip("\n").strip(".") == token.string
                    ):
                        modules.append(token.string)
                        modified_tokens.append(token)
                    else:
                        converted_token = convert_string(token.string)
                        modified_tokens.append(token._replace(string=converted_token))
                        for extra in args.extra_files:
                            extra.write_text(
                                extra.read_text().replace(token.string, converted_token)
                            )
                except Exception as e:
                    print(e)
                    print(token)
                    input("Press any key to continue or ctrl+c to quit... ")
            elif token.type == 3 and 'f"' in token.string or "f'" in token.string:
                modified_tokens.append(
                    token._replace(
                        string=convert_fstring_variables(token.string, all_names)
                    )
                )
            else:
                modified_tokens.append(token)
        content = tokenize.untokenize(modified_tokens)
        if args.lower_module_names:
            for module in modules:
                content = content.replace(module, module.lower())
                for extra in args.extra_files:
                    extra.write_text(extra.read_text().replace(module, module.lower()))
        if args.convert_file_name:
            converted_stem = convert_string(file.stem)
            file.with_stem(converted_stem).write_text(content)
            if converted_stem != file.stem:
                file.unlink()
            for extra in args.extra_files:
                extra.write_text(extra.read_text().replace(file.stem, converted_stem))
        else:
            file.write_text(content)


if __name__ == "__main__":
    main(get_args())
