import csv
from itertools import product


def generate_combinations():
    l1_options = [
        "(sx, sy, sz)≤₁(x1, y1, z1)",
        "¬((sx, sy, sz)≤₁(x1, y1, z1))",
        "(x1, y1, z1)≤₁(sx, sy, sz)",
        "¬((x1, y1, z1)≤₁(sx, sy, sz))"

    ]

    l2_options = [
        "(sx, sy, sz)≤₂(x2, y2, z2)",
        "(x2, y2, z2)≤₂(sx, sy, sz)"
    ]

    l3_options = [
        "(sx, sy, sz)≤₃(x3, y3, z3)",
        "(x3, y3, z3)≤₃(sx, sy, sz)"
    ]

    l4_options = [
        "(sx, sy, sz)≤₂(x4, y4, z4)",
        "¬((sx, sy, sz)≤₂(x4, y4, z4))",
        "(x4, y4, z4)≤₂(sx, sy, sz)",
        "¬((x4, y4, z4)≤₂(sx, sy, sz))"
    ]

    l5_options = [
        "(sx, sy, sz)≤₁(x5, y5, z5)",
        "(x5, y5, z5)≤₁(sx, sy, sz)"
    ]

    l6_options = [
        "(sx, sy, sz)≤₃(x6, y6, z6)",
        "(x6, y6, z6)≤₃(sx, sy, sz)"
    ]

    l7_options = [
        "(sx, sy, sz)≤₃(x7, y7, z7)",
        "¬((sx, sy, sz)≤₃(x7, y7, z7))",
        "(x7, y7, z7)≤₃(sx, sy, sz)",
        "¬((x7, y7, z7)≤₃(sx, sy, sz))"
    ]

    l8_options = [
        "(sx, sy, sz)≤₁(x8, y8, z8)",
        "(x8, y8, z8)≤₁(sx, sy, sz)"
    ]

    l9_options = [
        "(sx, sy, sz)≤₂(x9, y9, z9)",
        "(x9, y9, z9)≤₂(sx, sy, sz)"
    ]
    total_combinations = (
        len(l1_options) * len(l2_options) * len(l3_options) *
        len(l4_options) * len(l5_options) * len(l6_options) *
        len(l7_options) * len(l8_options) * len(l9_options)
    )

    # 添加编码参数确保文件正确写入
    with open('generate_combination_sat.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Rule'])

        for combo in product(
                l1_options, l2_options, l3_options,
                l4_options, l5_options, l6_options,
                l7_options, l8_options, l9_options
        ):
            l1, l2, l3, l4, l5, l6, l7, l8, l9 = combo

            clause = f"({l1}⊃{l2}∧{l3})∧({l4}⊃{l5}∧{l6})∧({l7}⊃{l8}∧{l9})"
            full_rule = clause
            writer.writerow([full_rule])

    print(f"Generated {total_combinations} combinations")
    return total_combinations

if __name__ == "__main__":
    generate_combinations()