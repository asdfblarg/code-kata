import json

with open("spec.json") as file:
    spec = json.load(file)


col_names = spec["ColumnNames"]
offsets = spec["Offsets"]
fw_enc = spec["FixedWidthEncoding"]
header = spec["IncludeHeader"]
delimit_enc = spec["DelimitedEncoding"]

cols_spec = {}
for i in range(len(col_names)):
    cols_spec[i] = (col_names[i], int(offsets[i]))


def read_fwf_file(input_fn, input_enc):
    lines = []
    with open(input_fn, "r", encoding=input_enc) as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


def parse_fwf_row(row_data, cols_spec):
    cur = 0
    data = []
    for i in range(len(cols_spec)):
        col_name, col_width = cols_spec[i]

        col_data = row_data[cur : cur + col_width]
        data.append(col_data.strip())

        cur += col_width
    return data


def parse_data(rows_data, cols_spec):
    parsed_data = []
    for row in rows_data:
        if row:
            parsed_row = parse_fwf_row(row, cols_spec)
            parsed_data.append(parsed_row)
    return parsed_data


def write_csv(filename, data, output_enc, header, delimiter=","):
    with open(filename, "w", encoding=output_enc) as file:
        if header:
            header_row = ",".join(col_names)
            file.write(f"{header_row}\n")

        for row in data:
            row_data = ",".join(row)
            file.write(f"{row_data}\n")

    print(f"Data parsed into: {filename}")


fwf_fn = "text.fwf"
fwf_rows = read_fwf_file(fwf_fn, fw_enc)

if header:
    header_row = fwf_rows[0]
    fwf_rows = fwf_rows[1:]

parsed_data = parse_data(fwf_rows, cols_spec)
write_csv("fwf_data.csv", parsed_data, delimit_enc, header)
