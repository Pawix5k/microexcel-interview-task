import argparse
import csv
import sys
import typing
from pathlib import Path

from _sheet import Sheet


def read_csv(path: Path) -> list[list[str]]:
    try:
        with open(path, "r") as f:
            reader = csv.reader(f)
            return [row for row in reader]
    except FileNotFoundError:
        sys.exit("Input file not found")
    except IsADirectoryError:
        sys.exit("Input path is a directory")
    except PermissionError:
        sys.exit("Permission to input file denied")
    except OSError:
        sys.exit("Problem reading file")


def write_csv(path: Path, csv_data: list[list[str]]) -> None:
    try:
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)
    except FileNotFoundError:
        sys.exit("Input file not found")
    except IsADirectoryError:
        sys.exit("Input path is a directory")
    except PermissionError:
        sys.exit("Permission to input file denied")
    except OSError:
        sys.exit("Problem reading file")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="MicroExcel",
        description="Evaluate .csv file like an Excel sheet.",
        epilog="Text at the bottom of help",
    )
    parser.add_argument("input", help="input file path", type=str)
    parser.add_argument("output", help="output file path", type=str)
    args = parser.parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    csv_data = read_csv(input_path)
    sheet = Sheet(csv_data)
    write_csv(output_path, sheet.evaluate())


if __name__ == "__main__":
    main()
