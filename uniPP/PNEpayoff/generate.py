import csv
from itertools import product

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
print(f"number: {total_combinations}")