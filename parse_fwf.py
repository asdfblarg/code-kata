from spec import Spec
import argparse


def read_fwf_file(input_fn: str, spec: type[Spec]):
    lines = []
    with open(input_fn, "r", encoding=spec.fixed_width_encoding) as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


def parse_fwf_row(row_data: list[str], spec: type[Spec]):
    cur = 0
    data = []
    for i in range(spec.num_columns):
        col_name, col_width = spec.columns[i]

        col_data = row_data[cur : cur + col_width]
        data.append(col_data.strip())

        cur += col_width
    return data


def parse_data(rows_data: list[str], spec: type[Spec]):
    parsed_data = []
    for row in rows_data:
        if row:
            parsed_row = parse_fwf_row(row, spec)
            parsed_data.append(parsed_row)
    return parsed_data


def write_csv(filename: str, data: list[list[str]], spec: type[Spec], delimiter=","):
    with open(filename, "w", encoding=spec.delimited_encoding) as file:
        if spec.include_header:
            header_row = ",".join(spec.column_names)
            file.write(f"{header_row}\n")

        for row in data:
            row_data = ",".join(row)
            file.write(f"{row_data}\n")

    print(f"Data parsed into: {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This script parses a fixed width file and writes a delimited csv file."
    )
    parser.add_argument(
        "-f", "--file", help="Input fixed width file name", required=True
    )
    parser.add_argument(
        "-o", "--output", help="Output delimited csv file name", required=True
    )
    parser.add_argument("-s", "--spec", help="Spec json file name", default="spec.json")
    parser.add_argument("-d", "--delimiter", help="Spec json file name", default=",")
    args = parser.parse_args()

    fwf_filename = args.file
    csv_filename = args.output
    spec_file = args.spec
    delimiter = args.delimiter

    spec = Spec(spec_file)

    fwf_rows = read_fwf_file(fwf_filename, spec)

    if spec.include_header:
        fwf_rows = fwf_rows[1:]

    parsed_data = parse_data(fwf_rows, spec)
    write_csv(csv_filename, parsed_data, spec, delimiter=delimiter)
