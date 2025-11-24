import csv
import networkx as nx

SIGMA_RULES = [
    "s1(x1).",
    "s2(y1).",
    "s3(z1).",
    "player(1..3).",
    "%Sigma G",
    "leq(I, X, Y, Z, X, Y, Z) :- s1(X), s2(Y), s3(Z), player(I).",
    ":- not leq(I, X1, Y1, Z1, X2, Y2, Z2), not leq(I, X2, Y2, Z2, X1, Y1, Z1), s1(X1), s2(Y1), s3(Z1), s1(X2), s2(Y2), s3(Z2), player(I).",
    "leq(I, X1, Y1, Z1, X3, Y3, Z3) :- leq(I, X1, Y1, Z1, X2, Y2, Z2), leq(I, X2, Y2, Z2, X3, Y3, Z3), s1(X1), s2(Y1), s3(Z1), s1(X2), s2(Y2), s3(Z2), s1(X3), s2(Y3), s3(Z3), player(I).",
    "%classical not and not is failure",
    "not_leq(I, X, Y, Z, X1, Y1, Z1):- not leq(I, X, Y, Z, X1, Y1, Z1), s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).",
    ":- not_leq(I, X, Y, Z, X1, Y1, Z1), leq(I, X, Y, Z, X1, Y1, Z1), s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).",
    ":- not not_leq(I, X, Y, Z, X1, Y1, Z1), not leq(I, X, Y, Z, X1, Y1, Z1), s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I)."
]

def parse_rule(rule_line):
    rule_line = rule_line.strip()
    if not rule_line or rule_line.startswith("%"):
        return None, [], []

    if ":-" in rule_line:
        head_part, body_part = rule_line.split(":-", 1)
    else:
        head_part, body_part = rule_line, ""

    head_part = head_part.strip()
    if "|" in head_part:
        head = head_part.split("|")[0].strip()
    else:
        head = head_part

    pos_literals = []
    neg_literals = []

    body_literals = [x.strip() for x in body_part.split(",") if x.strip()]
    for lit in body_literals:
        if lit.startswith("not "):
            neg_literals.append(lit[4:].strip())
        else:
            pos_literals.append(lit.strip())

    return head, pos_literals, neg_literals


def is_stratified_with_sigma(delta_line, sigma_rules):
    G = nx.DiGraph()
    delta_rules = [r.strip() for r in delta_line.split(".") if r.strip()]
    all_rules = sig#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import networkx as nx


SIGMA_RULES = [
    "s1(a1).",
    "s2(b1).",
    "s3(c1).",
    "player(1..3).",
    "leq(I, X, Y, Z, X, Y, Z) :- s1(X), s2(Y), s3(Z), player(I).",
    """{ leq(I, X1, Y1, Z1, X2, Y2, Z2) } :-
       s1(X1), s2(Y1), s3(Z1), 
       s1(X2), s2(Y2), s3(Z2), 
       player(I),
       X1 != X2; Y1 != Y2; Z1 != Z2.""",
    ":- not leq(I, X1, Y1, Z1, X2, Y2, Z2), not leq(I, X2, Y2, Z2, X1, Y1, Z1), s1(X1), s2(Y1), s3(Z1), s1(X2), s2(Y2), s3(Z2), player(I).",
    "leq(I, X1, Y1, Z1, X3, Y3, Z3) :- leq(I, X1, Y1, Z1, X2, Y2, Z2), leq(I, X2, Y2, Z2, X3, Y3, Z3), s1(X1), s2(Y1), s3(Z1), s1(X2), s2(Y2), s3(Z2), s1(X3), s2(Y3), s3(Z3), player(I)."
]


NOT_LEQ_RULES = [
    "not_leq(I, X, Y, Z, X1, Y1, Z1):- not leq(I, X, Y, Z, X1, Y1, Z1), s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).",
    ":- not_leq(I, X, Y, Z, X1, Y1, Z1), leq(I, X, Y, Z, X1, Y1, Z1), s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).",
    ":- not not_leq(I, X, Y, Z, X1, Y1, Z1), not leq(I, X, Y, Z, X1, Y1, Z1), s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I)."
]


NE_RULES = [
    "ne(X,Y,Z) :- leq(1, XE, Y, Z, X, Y, Z), leq(2, X, YE, Z, X, Y, Z), leq(3, X, Y, ZE, X, Y, Z), s1(XE), s2(YE), s3(ZE), s1(X), s2(Y), s3(Z).",
    "ne(a1,b1,c1)."
]


SIM_RULES = [
    "sim(I, X1, Y1, Z1, X2, Y2, Z2) :- leq(I, X1, Y1, Z1, X2, Y2, Z2), leq(I, X2, Y2, Z2, X1, Y1, Z1).",
    ":- sim(1,a1,b1,c1,a2,b2,c2), sim(2,a1,b1,c1,a2,b2,c2), sim(3,a1,b1,c1,a2,b2,c2)."
]

def parse_rule(rule_line):
    rule_line = rule_line.strip()
    if not rule_line or rule_line.startswith("%"):
        return None, [], []

    if ":-" in rule_line:
        head_part, body_part = rule_line.split(":-", 1)
    else:
        head_part, body_part = rule_line, ""

    head_part = head_part.strip()
    if not head_part:
        head = "__constraint__"
    elif "|" in head_part:
        head = head_part.split("|")[0].strip()
    else:
        head = head_part

    pos_literals = []
    neg_literals = []
    body_literals = [x.strip() for x in body_part.split(",") if x.strip()]
    for lit in body_literals:
        if lit.startswith("not "):
            neg_literals.append(lit[4:].strip())
        else:
            pos_literals.append(lit.strip())

    return head, pos_literals, neg_literals

def is_stratified_program(rules_list):
    G = nx.DiGraph()
    for rule in rules_list:
        head, pos, neg = parse_rule(rule)
        if not head:
            continue
        for p in pos:
            G.add_edge(head, p, neg=False)
        for n in neg:
            G.add_edge(head, n, neg=True)

    for cycle in nx.simple_cycles(G):
        cycle_edges = list(zip(cycle, cycle[1:] + [cycle[0]]))
        for u, v in cycle_edges:
            if G[u][v].get("neg", False):
                return False
    return True

def read_b_rules(csv_path):
    b_rules = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].strip():
                b_rules.append(row[0].strip())
    return b_rules
def main():
    # P1
    b_rules_p1 = read_b_rules("generate_combination.csv")
    full_rules_p1 = SIGMA_RULES + b_rules_p1 + NOT_LEQ_RULES + NE_RULES
    stratified_p1 = is_stratified_program(full_rules_p1)
    print(f"P1 is stratified: {stratified_p1}")

    # P2
    b_rules_p2 = read_b_rules("sy_generate_combination.csv")
    full_rules_p2 = SIGMA_RULES + b_rules_p2 + NOT_LEQ_RULES + NE_RULES + SIM_RULES
    stratified_p2 = is_stratified_program(full_rules_p2)
    print(f"P2 is stratified: {stratified_p2}")

if __name__ == "__main__":
    main()