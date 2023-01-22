import argparse
import tokenize
from pathlib import Path


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("files_to_convert", type=str)

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

    parser.add_argument("-cfn", "--convert_file_name", action="store_true")

    args = parser.parse_args()
    args.files_to_convert: Path = Path(args.files_to_convert)
    args.extra_files: list[Path] = [Path(file) for file in args.extra_files]

    return args


def convert_string(camel_string: str) -> str:
    return "".join(f"_{ch.lower()}" if ch.isupper() else ch for ch in camel_string)


def main():
    args = get_args()
    if args.files_to_convert.is_file():
        files_to_convert: list[Path] = [args.files_to_convert]
    else:
        files_to_convert: list[Path] = list(args.files_to_convert.iterdir())
    for file in files_to_convert:
        content = file.read_text()
        names = []
        modules = []
        with file.open("r") as f:
            for token in tokenize.generate_tokens(f.readline):
                if token.type == 1:
                    if (
                        "import" in token.line
                        and token.line.split()[1].strip("\n").strip(".") == token.string
                    ):
                        modules.append(token.string)
                    elif token.string not in modules:
                        names.append(token.string)
            names = list(set(names))

        for name in names:
            if not name[0].isupper():
                converted_name = convert_string(name)
                content = content.replace(name, converted_name)
                for extra in args.extra_files:
                    extra.write_text(extra.read_text().replace(name, converted_name))
        if args.lower_module_names:
            for module in modules:
                content = content.replace(module, module.lower())
                for extra in args.extra_files:
                    extra.write_text(extra.read_text().replace(module, module.lower()))
        if args.convert_file_name:
            file.with_stem(convert_string(file.stem)).write_text(content)
            file.unlink()
        else:
            file.write_text(content)


if __name__ == "__main__":
    main()
