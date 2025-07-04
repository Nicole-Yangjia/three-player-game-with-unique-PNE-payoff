import csv
import re


def extract_head_and_body(clause):
    match = re.match(r'^([^(]+\([^)]*\))\s*:-\s*([^,]+\([^)]*\))(?:,|$)', clause)
    if match:
        head = match.group(1).strip()
        first_body_atom = match.group(2).strip()
        return head, first_body_atom
    return None, None


def process_rule(rule_str):
    parts = rule_str.split('.')
    if len(parts) > 6:
        processed_str = '.'.join(parts[:6])
    else:
        processed_str = rule_str

    clauses = [clause.strip() for clause in processed_str.split('.') if clause.strip()]

    if len(clauses) != 6:
        return rule_str

    parsed_clauses = []
    for clause in clauses:
        head, first_body_atom = extract_head_and_body(clause)
        if head and first_body_atom:
            parsed_clauses.append((head, first_body_atom))
        else:
            parsed_clauses.append(('', clause))

    groups = []
    for i in range(0, 6, 2):
        if i + 1 < len(parsed_clauses):
            head1, body1 = parsed_clauses[i]
            head2, body2 = parsed_clauses[i + 1]

            if body1 == body2 and body1:
                groups.append((body1, head1, head2))

    new_rules = []
    for body, head1, head2 in groups:
        body = re.sub(r'\bx1\b', 'x', body)
        body = re.sub(r'\by1\b', 'y', body)
        body = re.sub(r'\bz1\b', 'z', body)

        head1 = re.sub(r'\bx1\b', 'x', head1)
        head1 = re.sub(r'\by1\b', 'y', head1)
        head1 = re.sub(r'\bz1\b', 'z', head1)

        head2 = re.sub(r'\bx1\b', 'x', head2)
        head2 = re.sub(r'\by1\b', 'y', head2)
        head2 = re.sub(r'\bz1\b', 'z', head2)

        new_rules.append(f"{body}->{head1},{head2}")

    return ' '.join([f"{r}." for r in new_rules])


input_file = 'unique_PNE_payoff.csv'
output_file = 'conditions_unique_PNE_payoff.csv'

with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    headers = next(reader)
    writer.writerow(headers)

    for row_idx, row in enumerate(reader):
        if row:
            try:
                original_rule = row[0]
                processed_rule = process_rule(original_rule)
                row[0] = processed_rule
                writer.writerow(row)
            except Exception as e:
                print(f"Error processing row {row_idx + 2}: {e}")
                writer.writerow(row)

print("Processing complete! Results saved to", output_file)