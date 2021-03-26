import argparse
import json

from scidatalib.scidata import SciData


def get_parser():
    parser = argparse.ArgumentParser(
        prog="scidatalib",
        description="SciDataLib - Library for SciData JSON-LD",
        allow_abbrev=False)

    # Positional arguments
    parser.add_argument(
        "output",
        type=str,
        help="Filename for output SciData JSON-LD file")

    # Optional arguments
    parser.add_argument(
        "--uid",
        type=str,
        default="example",
        help="UID of the SciData JSON-LD")

    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="Number of indents for JSON-LD formatting")

    return parser


def cli(input_args=None):
    parser = get_parser()

    if input_args:
        args = parser.parse_args(input_args)
    else:
        args = parser.parse_args()  # pragma: no cover

    sd = SciData(args.uid)
    with open(args.output, 'w') as out:
        json.dump(sd.output, out, indent=args.indent)
        print(f'SciData JSON-LD written to... {args.output}')


if __name__ == "__main__":
    cli()  # pragma: no cover
