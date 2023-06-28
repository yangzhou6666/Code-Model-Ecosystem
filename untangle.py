import os
import csv

if __name__ == '__main__':
    file_path = 'data/all.csv'
    output_file_path = 'data/all_untangled.csv'

    with open(file_path, 'r', newline='') as input_file, open(output_file_path, 'w', newline='') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)

        for row in reader:
            if row[4] != '2':
                continue
            model = row[0]
            dataset = row[1]
            dependent_model = row[2]

            if len(dataset) > 0:
                writer.writerow([model, dataset])
            if len(dependent_model) > 0:
                writer.writerow([model, dependent_model])
