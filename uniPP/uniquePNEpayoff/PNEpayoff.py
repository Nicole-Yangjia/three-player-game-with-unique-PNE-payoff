import csv
from itertools import product
import clingo
import re


# =============================================================================
# Step 1: Generate all rule combinations
# =============================================================================
def generate_combinations():
    l1_options = [
        "leq(1, x1, y1, z1, X1, Y1, Z1)",
        "not_leq(1, x1, y1, z1, X1, Y1, Z1)",
        "leq(1, X1, Y1, Z1, x1, y1, z1)",
        "not_leq(1, X1, Y1, Z1, x1, y1, z1)"
    ]

    l2_options = [
        "leq(2, x1, y1, z1, X2, Y2, Z2)",
        "leq(2, X2, Y2, Z2, x1, y1, z1)"
    ]

    l3_options = [
        "leq(3, x1, y1, z1, X3, Y3, Z3)",
        "leq(3, X3, Y3, Z3, x1, y1, z1)"
    ]

    l4_options = [
        "leq(2, x1, y1, z1, X4, Y4, Z4)",
        "not_leq(2, x1, y1, z1, X4, Y4, Z4)",
        "leq(2, X4, Y4, Z4, x1, y1, z1)",
        "not_leq(2, X4, Y4, Z4, x1, y1, z1)"
    ]

    l5_options = [
        "leq(1, x1, y1, z1, X5, Y5, Z5)",
        "leq(1, X5, Y5, Z5, x1, y1, z1)"
    ]

    l6_options = [
        "leq(3, x1, y1, z1, X6, Y6, Z6)",
        "leq(3, X6, Y6, Z6, x1, y1, z1)"
    ]

    l7_options = [
        "leq(3, x1, y1, z1, X7, Y7, Z7)",
        "not_leq(3, x1, y1, z1, X7, Y7, Z7)",
        "leq(3, X7, Y7, Z7, x1, y1, z1)",
        "not_leq(3, X7, Y7, Z7, x1, y1, z1)"
    ]

    l8_options = [
        "leq(1, x1, y1, z1, X8, Y8, Z8)",
        "leq(1, X8, Y8, Z8, x1, y1, z1)"
    ]

    l9_options = [
        "leq(2, x1, y1, z1, X9, Y9, Z9)",
        "leq(2, X9, Y9, Z9, x1, y1, z1)"
    ]

    total_combinations = (
            len(l1_options) * len(l2_options) * len(l3_options) *
            len(l4_options) * len(l5_options) * len(l6_options) *
            len(l7_options) * len(l8_options) * len(l9_options)
    )

    with open('generate_combination.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Rule'])

        for combo in product(
                l1_options, l2_options, l3_options,
                l4_options, l5_options, l6_options,
                l7_options, l8_options, l9_options
        ):
            l1, l2, l3, l4, l5, l6, l7, l8, l9 = combo

            clause1 = f"{l2} :- {l1}, s1(X1), s2(Y1), s3(Z1), s1(X2), s2(Y2), s3(Z2)."
            clause2 = f"{l3} :- {l1}, s1(X1), s2(Y1), s3(Z1), s1(X3), s2(Y3), s3(Z3)."
            clause3 = f"{l5} :- {l4}, s1(X4), s2(Y4), s3(Z4), s1(X5), s2(Y5), s3(Z5)."
            clause4 = f"{l6} :- {l4}, s1(X4), s2(Y4), s3(Z4), s1(X6), s2(Y6), s3(Z6)."
            clause5 = f"{l8} :- {l7}, s1(X7), s2(Y7), s3(Z7), s1(X8), s2(Y8), s3(Z8)."
            clause6 = f"{l9} :- {l7}, s1(X7), s2(Y7), s3(Z7), s1(X9), s2(Y9), s3(Z9)."
            full_rule = clause1 + clause2 + clause3 + clause4 + clause5 + clause6
            writer.writerow([full_rule])

    print(f"Generated {total_combinations} combinations")
    return total_combinations


# =============================================================================
# Step 2: Check for PNE existence
# =============================================================================
def generate_asp_program_pne(b_rules):
    return f"""
s1(x1).
s2(y1).
s3(z1).
player(1..3).
%Sigma G
leq(I, X, Y, Z, X, Y, Z) :- s1(X), s2(Y), s3(Z), player(I).

leq(I, X1, Y1, Z1, X2, Y2, Z2) | leq(I, X2, Y2, Z2, X1, Y1, Z1) :- 
    s1(X1), s2(Y1), s3(Z1), 
    s1(X2), s2(Y2), s3(Z2), 
    player(I).

leq(I, X1, Y1, Z1, X3, Y3, Z3) :- 
    leq(I, X1, Y1, Z1, X2, Y2, Z2), 
    leq(I, X2, Y2, Z2, X3, Y3, Z3),
    s1(X1), s2(Y1), s3(Z1),
    s1(X2), s2(Y2), s3(Z2),
    s1(X3), s2(Y3), s3(Z3),
    player(I).

%classical not and not is failure
not_leq(I, X, Y, Z, X1, Y1, Z1):- not leq(I, X, Y, Z, X1, Y1, Z1), s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).
:- not_leq(I, X, Y, Z, X1, Y1, Z1), leq(I, X, Y, Z, X1, Y1, Z1), s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).
not_leq(I, X, Y, Z, X1, Y1, Z1) | leq(I, X, Y, Z, X1, Y1, Z1):- s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).

%Omega'(x1,y1,z1)
{b_rules}

ne(X,Y,Z) :- 
    leq(1, XE, Y, Z, X, Y, Z), 
    leq(2, X, YE, Z, X, Y, Z), 
    leq(3, X, Y, ZE, X, Y, Z),
    s1(XE), s2(YE), s3(ZE), s1(X), s2(Y), s3(Z).

%NE(x1,y1,z1)
ne(x1,y1,z1).
"""


def solve_asp_with_b_rule_pne(b_rule):
    formatted_b_rule = b_rule.replace('.', '.\n') + '\n' if b_rule else ''

    asp_program = generate_asp_program_pne(formatted_b_rule)

    with open("debug_asp.lp", "w") as f:
        f.write(asp_program)

    control = clingo.Control()
    control.add("base", [], asp_program)

    try:
        control.ground([("base", [])])
        result = control.solve()
        return result.satisfiable
    except Exception as e:
        print(f"Error solving ASP: {e}")
        print("Problematic ASP program saved to debug_asp.lp")
        return False


def check_pne_existence():
    with open('generate_combination.csv', 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        failed_rules = []
        passed_rules = []

        total_count = 0
        success_count = 0

        for i, row in enumerate(reader):
            if not row:
                continue
            b_rule = row[0]
            total_count += 1
            print(f"Processing rule {i + 1}...")
            if solve_asp_with_b_rule_pne(b_rule):
                passed_rules.append(b_rule)
                success_count += 1
                print(" -> Satisfiable")
            else:
                failed_rules.append(b_rule)
                print(" -> Unsatisfiable")
            print(f"Progress: {i + 1}/{total_count}, Satisfiable: {success_count}, Unsatisfiable: {len(failed_rules)}")

    with open('noPNE.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header)
        for rule in failed_rules:
            writer.writerow([rule])

    with open('havePNE.csv', 'w', newline='') as passed_file:
        writer = csv.writer(passed_file)
        writer.writerow(header)
        for rule in passed_rules:
            writer.writerow([rule])

    print(f"Processing completed: {total_count} rules")
    print(f"Unsatisfiable: {len(failed_rules)}")
    print(f"Satisfiable: {len(passed_rules)}")
    return passed_rules


# =============================================================================
# Step 3: Create symmetric rules
# =============================================================================
def create_symmetric_rules():
    def process_line(line):
        new_part = line.replace('x1, y1, z1', 'x2, y2, z2')
        return line + new_part

    with open('havePNE.csv', 'r', newline='') as infile, \
            open('sy_generate_combination.csv', 'w', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            if row:
                processed_line = process_line(row[0])
                writer.writerow([processed_line])

    print("Created symmetric rules")


# =============================================================================
# Step 4: Check for unique PNE
# =============================================================================
def generate_asp_program_unique(b_rules):
    return f"""
% strategies and players
s1(x1).
s1(x2).
s2(y1).
s2(y2).
s3(z1).
s3(z2).
player(1..3).

%Sigma G
leq(I, X, Y, Z, X, Y, Z) :- s1(X), s2(Y), s3(Z), player(I).

leq(I, X1, Y1, Z1, X2, Y2, Z2) | leq(I, X2, Y2, Z2, X1, Y1, Z1) :- 
    s1(X1), s2(Y1), s3(Z1), 
    s1(X2), s2(Y2), s3(Z2), 
    player(I).

leq(I, X1, Y1, Z1, X3, Y3, Z3) :- 
    leq(I, X1, Y1, Z1, X2, Y2, Z2), 
    leq(I, X2, Y2, Z2, X3, Y3, Z3),
    player(I).

%classical not and not is failure
not_leq(I, X, Y, Z, X1, Y1, Z1):- not leq(I, X, Y, Z, X1, Y1, Z1), s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).
:- not_leq(I, X, Y, Z, X1, Y1, Z1), leq(I, X, Y, Z, X1, Y1, Z1), s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).
not_leq(I, X, Y, Z, X1, Y1, Z1) | leq(I, X, Y, Z, X1, Y1, Z1):- s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).

%Omega'(x1,y1,z1) and Omega'(x2,y2,z2)
{b_rules}

% PNE
ne(X,Y,Z) :- 
    leq(1, XE, Y, Z, X, Y, Z), 
    leq(2, X, YE, Z, X, Y, Z), 
    leq(3, X, Y, ZE, X, Y, Z),
    s1(XE), s2(YE), s3(ZE), s1(X), s2(Y), s3(Z).


sim(I, X1, Y1, Z1, X2, Y2, Z2) :- 
    leq(I, X1, Y1, Z1, X2, Y2, Z2), 
    leq(I, X2, Y2, Z2, X1, Y1, Z1).

% SIM
ne(x1,y1,z1).
ne(x2,y2,z2).
:- sim(1,x1,y1,z1,x2,y2,z2), sim(2,x1,y1,z1,x2,y2,z2), sim(3,x1,y1,z1,x2,y2,z2).
"""


def solve_asp_with_b_rule_unique(b_rule):
    formatted_b_rule = b_rule.replace('.', '.\n') + '\n' if b_rule else ''

    asp_program = generate_asp_program_unique(formatted_b_rule)
    with open("debug_asp.lp", "w") as f:
        f.write(asp_program)

    control = clingo.Control()
    control.add("base", [], asp_program)

    try:
        control.ground([("base", [])])
        result = control.solve()
        return result.satisfiable
    except Exception as e:
        print(f"Error solving ASP: {e}")
        print("Problematic ASP program saved to debug_asp.lp")
        return False


def check_unique_pne():
    with open('sy_generate_combination.csv', 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        failed_rules = []
        passed_rules = []

        total_count = 0
        success_count = 0

        for i, row in enumerate(reader):
            if not row:
                continue
            b_rule = row[0]
            total_count += 1
            print(f"Processing rule {i + 1}...")
            if solve_asp_with_b_rule_unique(b_rule):
                passed_rules.append(b_rule)
                success_count += 1
                print(" -> Satisfiable")
            else:
                failed_rules.append(b_rule)
                print(" -> Unsatisfiable")
            print(f"process: {i + 1}/{total_count}, Satisfiable: {success_count}, Unsatisfiable: {len(failed_rules)}")

    with open('unique_PNE_payoff.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header)
        for rule in failed_rules:
            writer.writerow([rule])

    with open('no_unique_PNE_payoff.csv', 'w', newline='') as passed_file:
        writer = csv.writer(passed_file)
        writer.writerow(header)
        for rule in passed_rules:
            writer.writerow([rule])

    print(f"Processing completed: {total_count} rules")
    print(f"Unique PNE: {len(failed_rules)}")
    print(f"Non-unique PNE: {len(passed_rules)}")
    return failed_rules


# =============================================================================
# Step 5: Extract conditions
# =============================================================================
def extract_conditions():
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

    print("Condition extraction complete")


# =============================================================================
# Main Execution Flow
# =============================================================================
if __name__ == "__main__":
    print("=" * 50)
    print("Step 1: Generating rule combinations")
    print("=" * 50)
    generate_combinations()

    print("\n" + "=" * 50)
    print("Step 2: Checking for PNE existence")
    print("=" * 50)
    check_pne_existence()

    print("\n" + "=" * 50)
    print("Step 3: Creating symmetric rules")
    print("=" * 50)
    create_symmetric_rules()

    print("\n" + "=" * 50)
    print("Step 4: Checking for unique PNE")
    print("=" * 50)
    check_unique_pne()

    print("\n" + "=" * 50)
    print("Step 5: Extracting conditions")
    print("=" * 50)
    extract_conditions()

    print("\nProcessing pipeline completed successfully!")