import json
import csv

input_json = 'dataset_rsicd.json'
output_csv = 'rsicd.csv'

with open(input_json, 'r') as f:
    data = json.load(f)

rows = []
for image_data in data['images']:
    filename = image_data['filename']
    for sentence in image_data['sentences']:
        caption = sentence['raw'].strip()
        rows.append({
            'filepath': filename,
            'captions': caption
        })

with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['filepath', 'captions'])
    writer.writeheader()
    writer.writerows(rows)

print(f"CSV file created: {output_csv}")
