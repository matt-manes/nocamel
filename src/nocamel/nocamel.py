import argparse
import tokenize
from pathlib import Path


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_to_convert", type=str)

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

    args = parser.parse_args()
    args.source_to_convert: Path = Path(args.source_to_convert)
    if args.source_to_convert.is_dir():
        args.file_to_convert = args.source_to_convert.rglob("*.py")
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


def main(args: argparse.Namespace = None):
    if not args:
        args = get_args()
    for file in args.source_to_convert:
        content = file.read_text()
        names = []
        modules = []
        with file.open("r") as f:
            tokens = list(tokenize.generate_tokens(f.readline))
        modified_tokens = []
        for token in tokens:
            if token.type == 1 and not token.string[0].isupper():
                if (
                    "import" in token.line
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
            file.unlink()
            for extra in args.extra_files:
                extra.write_text(extra.read_text().replace(file.stem, converted_stem))
        else:
            file.write_text(content)


if __name__ == "__main__":
    main(get_args())
