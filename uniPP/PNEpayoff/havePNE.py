import clingo
import csv


def generate_asp_program(b_rules):
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


def solve_asp_with_b_rule(b_rule):
    formatted_b_rule = b_rule.replace('.', '.\n') + '\n' if b_rule else ''

    asp_program = generate_asp_program(formatted_b_rule)

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


def process_csv(input_csv, output_csv, satisfiable_output_csv):
    with open(input_csv, 'r') as file:
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
            if solve_asp_with_b_rule(b_rule):
                passed_rules.append(b_rule)
                success_count += 1
                print(" -> Satisfiable")
            else:
                failed_rules.append(b_rule)
                print(" -> Unsatisfiable")
            print(f"Progress: {i + 1}/{total_count}, Satisfiable: {success_count}, Unsatisfiable: {len(failed_rules)}")

    with open(output_csv, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header)
        for rule in failed_rules:
            writer.writerow([rule])

    with open(satisfiable_output_csv, 'w', newline='') as passed_file:
        writer = csv.writer(passed_file)
        writer.writerow(header)
        for rule in passed_rules:
            writer.writerow([rule])

    print(f"Processing completed: {total_count} rules")
    print(f"Unsatisfiable: {len(failed_rules)}")
    print(f"Satisfiable: {len(passed_rules)}")


if __name__ == "__main__":
    process_csv("generate_combination.csv", "noPNE.csv", "havePNE.csv")