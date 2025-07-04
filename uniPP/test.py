import random
import clingo


def generate_random_combination():
    options = {
        'l1': [
            "leq(1, x1, y1, z1, X1, Y1, Z1)",
            "not_leq(1, x1, y1, z1, X1, Y1, Z1)",
            "leq(1, X1, Y1, Z1, x1, y1, z1)",
            "not_leq(1, X1, Y1, Z1, x1, y1, z1)"
        ],
        'l2': [
            "leq(2, x1, y1, z1, X2, Y2, Z2)",
            "leq(2, X2, Y2, Z2, x1, y1, z1)"
        ],
        'l3': [
            "leq(3, x1, y1, z1, X3, Y3, Z3)",
            "leq(3, X3, Y3, Z3, x1, y1, z1)"
        ],
        'l4': [
            "leq(2, x1, y1, z1, X4, Y4, Z4)",
            "not_leq(2, x1, y1, z1, X4, Y4, Z4)",
            "leq(2, X4, Y4, Z4, x1, y1, z1)",
            "not_leq(2, X4, Y4, Z4, x1, y1, z1)"
        ],
        'l5': [
            "leq(1, x1, y1, z1, X5, Y5, Z5)",
            "leq(1, X5, Y5, Z5, x1, y1, z1)"
        ],
        'l6': [
            "leq(3, x1, y1, z1, X6, Y6, Z6)",
            "leq(3, X6, Y6, Z6, x1, y1, z1)"
        ],
        'l7': [
            "leq(3, x1, y1, z1, X7, Y7, Z7)",
            "not_leq(3, x1, y1, z1, X7, Y7, Z7)",
            "leq(3, X7, Y7, Z7, x1, y1, z1)",
            "not_leq(3, X7, Y7, Z7, x1, y1, z1)"
        ],
        'l8': [
            "leq(1, x1, y1, z1, X8, Y8, Z8)",
            "leq(1, X8, Y8, Z8, x1, y1, z1)"
        ],
        'l9': [
            "leq(2, x1, y1, z1, X9, Y9, Z9)",
            "leq(2, X9, Y9, Z9, x1, y1, z1)"
        ]
    }

    selected = {key: random.choice(values) for key, values in options.items()}

    l1, l2, l3, l4, l5, l6, l7, l8, l9 = (
        selected['l1'], selected['l2'], selected['l3'],
        selected['l4'], selected['l5'], selected['l6'],
        selected['l7'], selected['l8'], selected['l9']
    )

    clause1 = f"{l2} :- {l1}, s1(X1), s2(Y1), s3(Z1), s1(X2), s2(Y2), s3(Z2)."
    clause2 = f"{l3} :- {l1}, s1(X1), s2(Y1), s3(Z1), s1(X3), s2(Y3), s3(Z3)."
    clause3 = f"{l5} :- {l4}, s1(X4), s2(Y4), s3(Z4), s1(X5), s2(Y5), s3(Z5)."
    clause4 = f"{l6} :- {l4}, s1(X4), s2(Y4), s3(Z4), s1(X6), s2(Y6), s3(Z6)."
    clause5 = f"{l8} :- {l7}, s1(X7), s2(Y7), s3(Z7), s1(X8), s2(Y8), s3(Z8)."
    clause6 = f"{l9} :- {l7}, s1(X7), s2(Y7), s3(Z7), s1(X9), s2(Y9), s3(Z9)."

    rule1 = clause1 + clause2 + clause3 + clause4 + clause5 + clause6
    rule2 = rule1.replace('x1, y1, z1', 'x2, y2, z2')

    def format_rule(atom):
        return atom.replace('x1, y1, z1', 'x, y, z').replace('x1,y1,z1', 'x,y,z')

    formatted_rule = (
        f"{format_rule(l1)} -> {format_rule(l2)}, {format_rule(l3)}.\n"
        f"{format_rule(l4)} -> {format_rule(l5)}, {format_rule(l6)}.\n"
        f"{format_rule(l7)} -> {format_rule(l8)}, {format_rule(l9)}."
    )

    return {
        'selected_options': selected,
        'rule1': rule1,
        'rule2': rule1 + rule2,
        'formatted_rule': formatted_rule
    }


def check_step1(rule):
    asp_program = f"""
s1(x1).
s2(y1).
s3(z1).
player(1..3).

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

not_leq(I, X, Y, Z, X1, Y1, Z1):- not leq(I, X, Y, Z, X1, Y1, Z1), 
    s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).

:- not_leq(I, X, Y, Z, X1, Y1, Z1), leq(I, X, Y, Z, X1, Y1, Z1), 
    s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).

not_leq(I, X, Y, Z, X1, Y1, Z1) | leq(I, X, Y, Z, X1, Y1, Z1):- 
    s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).

{rule}

ne(X,Y,Z) :- 
    leq(1, XE, Y, Z, X, Y, Z), 
    leq(2, X, YE, Z, X, Y, Z), 
    leq(3, X, Y, ZE, X, Y, Z),
    s1(XE), s2(YE), s3(ZE), s1(X), s2(Y), s3(Z).

ne(x1,y1,z1).
"""
    control = clingo.Control()
    control.add("base", [], asp_program)
    try:
        control.ground([("base", [])])
        result = control.solve()
        return result.satisfiable
    except Exception as e:
        print(f"Error in step1 ASP: {e}")
        return False


def check_step2(rule):
    asp_program = f"""
s1(x1).
s1(x2).
s2(y1).
s2(y2).
s3(z1).
s3(z2).
player(1..3).

leq(I, X, Y, Z, X, Y, Z) :- s1(X), s2(Y), s3(Z), player(I).

leq(I, X1, Y1, Z1, X2, Y2, Z2) | leq(I, X2, Y2, Z2, X1, Y1, Z1) :- 
    s1(X1), s2(Y1), s3(Z1), 
    s1(X2), s2(Y2), s3(Z2), 
    player(I).

leq(I, X1, Y1, Z1, X3, Y3, Z3) :- 
    leq(I, X1, Y1, Z1, X2, Y2, Z2), 
    leq(I, X2, Y2, Z2, X3, Y3, Z3),
    player(I).

not_leq(I, X, Y, Z, X1, Y1, Z1):- not leq(I, X, Y, Z, X1, Y1, Z1), 
    s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).

:- not_leq(I, X, Y, Z, X1, Y1, Z1), leq(I, X, Y, Z, X1, Y1, Z1), 
    s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).

not_leq(I, X, Y, Z, X1, Y1, Z1) | leq(I, X, Y, Z, X1, Y1, Z1):- 
    s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).

{rule}

ne(X,Y,Z) :- 
    leq(1, XE, Y, Z, X, Y, Z), 
    leq(2, X, YE, Z, X, Y, Z), 
    leq(3, X, Y, ZE, X, Y, Z),
    s1(XE), s2(YE), s3(ZE), s1(X), s2(Y), s3(Z).

sim(I, X1, Y1, Z1, X2, Y2, Z2) :- 
    leq(I, X1, Y1, Z1, X2, Y2, Z2), 
    leq(I, X2, Y2, Z2, X1, Y1, Z1).

ne(x1,y1,z1).
ne(x2,y2,z2).

:- sim(1,x1,y1,z1,x2,y2,z2), 
   sim(2,x1,y1,z1,x2,y2,z2), 
   sim(3,x1,y1,z1,x2,y2,z2).
"""
    control = clingo.Control()
    control.add("base", [], asp_program)
    try:
        control.ground([("base", [])])
        result = control.solve()
        return result.satisfiable
    except Exception as e:
        print(f"Error in step2 ASP: {e}")
        return False


def main():
    combination = generate_random_combination()

    print("Randomly selected options:")
    for key, value in combination['selected_options'].items():
        print(f"{key}: {value}")
    print()

    print("Formatted rules:")
    print(combination['formatted_rule'])
    print()

    print("Checking step1: Checking for pure Nash equilibrium...")
    step1_result = check_step1(combination['rule1'])
    print(f"Step1 result: {'PNE exists' if step1_result else 'No PNE'}")

    if step1_result:
        print("\nChecking step2: Checking for unique PNE payoff...")
        step2_result = check_step2(combination['rule2'])
        print(f"Step2 result: {'Unique PNE payoff' if step2_result else 'No unique PNE payoff'}")

    with open("random_combination_result.txt", "w") as f:
        f.write("Randomly selected options:\n")
        for key, value in combination['selected_options'].items():
            f.write(f"{key}: {value}\n")

        f.write("\nrules:\n")
        f.write(combination['formatted_rule'] + "\n")

        f.write("\nStep1 result: ")
        f.write("PNE exists\n" if step1_result else "No PNE\n")

        if step1_result:
            f.write("\nStep2 result: ")
            f.write("Unique PNE payoff\n" if step2_result else "No unique PNE payoff\n")

    print("\nResults saved to random_combination_result.txt")


if __name__ == "__main__":
    main()