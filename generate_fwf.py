import json


def load_spec_json(json_fn):
    with open(json_fn) as file:
        spec = json.load(file)
    return spec


def generate_line(row_data, cols_data):
    line = ""
    for i in range(len(cols_data)):
        col_name, col_width = cols_data[i]

        # truncate and pad data before adding to line
        col_data = row_data[i][:col_width]
        col_data = col_data.ljust(col_width)

        line += col_data

    return line


def write_file(cols_spec, data_rows, output_filename="text.fwf", header=True):
    with open(output_filename, "w", encoding=fw_enc) as outfile:
        if header:
            header_row = generate_line(col_names, cols_spec)
            outfile.write(f"{header_row}\n")

        for row in data_rows:
            data_row = generate_line(row, cols_spec)
            outfile.write(f"{data_row}\n")


spec = load_spec_json("spec.json")

col_names = spec["ColumnNames"]
offsets = spec["Offsets"]
fw_enc = spec["FixedWidthEncoding"]
header = spec["IncludeHeader"]
delimit_enc = spec["DelimitedEncoding"]

cols_spec = {}
for i in range(len(col_names)):
    cols_spec[i] = (col_names[i], int(offsets[i]))

# generate test data
data = [chr(ord("a") + i) for i in range(len(cols_spec) * 3)]
num_cols = len(cols_spec)
num_rows = len(data) // num_cols
data_rows = [data[num_cols * i : num_cols * (i + 1)] for i in range(num_rows)]

write_file(cols_spec, data_rows, header=True)
