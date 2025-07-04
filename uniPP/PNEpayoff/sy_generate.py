import csv


def process_line(line):
    new_part = line.replace('x1, y1, z1', 'x2, y2, z2')
    return line + new_part


def process_csv(input_file, output_file):
    with open(input_file, 'r', newline='') as infile, \
            open(output_file, 'w', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            if row:
                processed_line = process_line(row[0])
                writer.writerow([processed_line])


# 使用示例
input_csv = 'havePNE.csv'
output_csv = 'sy_generate_combination.csv'
process_csv(input_csv, output_csv)