from pysat.solvers import Solver
import csv, itertools, re, sys, time
from typing import List, Tuple, Dict

SUB_MAP = {'₁': '1', '₂': '2', '₃': '3'}


def normalize_leq_subscript(s: str) -> str:
    for k, v in SUB_MAP.items():
        s = s.replace('≤' + k, '≤' + v)
    return s


def split_top_level_groups(line: str) -> List[str]:
    s = line.strip()
    groups = []
    depth = 0
    cur = []
    for ch in s:
        if ch == '(':
            depth += 1
            cur.append(ch)
        elif ch == ')':
            cur.append(ch)
            depth -= 1
            if depth == 0:
                grp = ''.join(cur)
                groups.append(grp[1:-1].strip())
                cur = []
        else:
            if depth > 0:
                cur.append(ch)
    if not groups:
        st = s.strip()
        if st.startswith('(') and st.endswith(')'):
            return [st[1:-1].strip()]
    return groups


def parse_tuple_tokens(text: str) -> Tuple[str, str, str]:
    parts = [p.strip() for p in text.split(',')]
    return (parts[0], parts[1], parts[2])


def classify_triple(tokens: Tuple[str, str, str]):
    a, b, c = tokens
    if a == 'sx' and b == 'sy' and c == 'sz':
        return ('point', None)
    if a.startswith('x') and b.startswith('y') and c.startswith('z'):
        return ('var', a)
    return ('const', (a, b, c))


def parse_atom_text(atom_text: str):
    t = atom_text.strip()
    neg = False
    if t.startswith('¬'):
        neg = True
        t = t[1:].strip()
        if t.startswith('(') and t.endswith(')'):
            t = t[1:-1].strip()
    m_left = re.match(r'^\(\s*([^\)]+?)\s*\)', t)
    left_inner = m_left.group(1)
    rest = t[m_left.end():].strip()
    rest_after = rest[1:].strip()
    if len(rest_after) == 0 or not rest_after[0].isdigit():
        mm = re.match(r'^([1-3])', rest_after)
        player_char = mm.group(1)
        rest_after_digit = rest_after[mm.end():].strip()
    else:
        player_char = rest_after[0]
        rest_after_digit = rest_after[1:].strip()
    player = int(player_char)
    m_right = re.match(r'^\(\s*([^\)]+?)\s*\)', rest_after_digit)
    right_inner = m_right.group(1)
    left_tokens = parse_tuple_tokens(left_inner)
    right_tokens = parse_tuple_tokens(right_inner)
    left_class = classify_triple(left_tokens)
    right_class = classify_triple(right_tokens)
    return {'player': player, 'left': left_class, 'right': right_class, 'neg': neg}


def parse_implication_group(group_text: str):
    prem_text, rest = group_text.split('⊃', 1)
    prem_text = prem_text.strip()
    rest = rest.strip()
    c1_text, c2_text = rest.split('∧', 1)
    prem_atom = parse_atom_text(normalize_leq_subscript(prem_text))
    c1_atom = parse_atom_text(normalize_leq_subscript(c1_text.strip()))
    c2_atom = parse_atom_text(normalize_leq_subscript(c2_text.strip()))
    return (prem_atom, c1_atom, c2_atom)


def parse_omega_line(line: str):
    s = normalize_leq_subscript(line.strip())
    groups = split_top_level_groups(s)
    parsed = []
    for g in groups:
        parsed.append(parse_implication_group(g))
    return parsed


def make_strategies(X_domain, Y_domain, Z_domain):
    return [(x, y, z) for x in X_domain for y in Y_domain for z in Z_domain]


def build_index_map(strategies):
    return {t: i for i, t in enumerate(strategies)}


class CNFEncoder:
    def __init__(self, strategies: List[Tuple[str, str, str]]):
        self.strategies = list(strategies)
        self.idx = build_index_map(self.strategies)
        self.var = {}
        self.next_var = 1
        for player in (1, 2, 3):
            for a in self.strategies:
                for b in self.strategies:
                    self.var[(player, self.idx[a], self.idx[b])] = self.next_var
                    self.next_var += 1

    def get_var(self, player: int, left: Tuple[str, str, str], right: Tuple[str, str, str]) -> int:
        return self.var[(player, self.idx[left], self.idx[right])]

    def new_var(self) -> int:
        v = self.next_var
        self.next_var += 1
        return v


def add_sigmaG_clauses(encoder: CNFEncoder, clauses: List[List[int]]):
    S = encoder.strategies
    for p in (1, 2, 3):
        for t in S:
            clauses.append([encoder.get_var(p, t, t)])
    for p in (1, 2, 3):
        for t1 in S:
            for t2 in S:
                if t1 == t2: continue
                clauses.append([encoder.get_var(p, t1, t2), encoder.get_var(p, t2, t1)])
    for p in (1, 2, 3):
        for a in S:
            for b in S:
                for c in S:
                    v_ab = encoder.get_var(p, a, b)
                    v_bc = encoder.get_var(p, b, c)
                    v_ac = encoder.get_var(p, a, c)
                    clauses.append([-v_ab, -v_bc, v_ac])


def resolve_side(side, assignment: Dict[str, Tuple[str, str, str]], point_tuple: Tuple[str, str, str]):
    if side[0] == 'point':
        return point_tuple
    if side[0] == 'const':
        return side[1]
    if side[0] == 'var':
        name = side[1]
        return assignment[name]
    raise KeyError("Unknown side type")


def atom_to_literal(atom: Dict, encoder: CNFEncoder, assignment: Dict[str, Tuple[str, str, str]],
                    point_tuple: Tuple[str, str, str]) -> int:
    left = resolve_side(atom['left'], assignment, point_tuple)
    right = resolve_side(atom['right'], assignment, point_tuple)
    v = encoder.get_var(atom['player'], left, right)
    return -v if atom['neg'] else v


def collect_triple_vars(atom: Dict) -> List[str]:
    vars = []
    if atom['left'][0] == 'var':
        vars.append(atom['left'][1])
    if atom['right'][0] == 'var':
        vars.append(atom['right'][1])
    return vars


def instantiate_implication(prem, c1, c2, encoder: CNFEncoder, clauses: List[List[int]],
                            strategies: List[Tuple[str, str, str]], point_tuple: Tuple[str, str, str]):
    triple_vars = set()
    for atm in (prem, c1, c2):
        triple_vars.update(collect_triple_vars(atm))
    triple_vars = list(triple_vars)
    if not triple_vars:
        assignments = [{}]
    else:
        assignments = []
        for prod in itertools.product(strategies, repeat=len(triple_vars)):
            assign = {triple_vars[i]: prod[i] for i in range(len(triple_vars))}
            assignments.append(assign)
    for assign in assignments:
        lit_prem = atom_to_literal(prem, encoder, assign, point_tuple)
        lit_c1 = atom_to_literal(c1, encoder, assign, point_tuple)
        lit_c2 = atom_to_literal(c2, encoder, assign, point_tuple)
        clauses.append([-lit_prem, lit_c1])
        clauses.append([-lit_prem, lit_c2])


def omega_parsed_to_clauses(parsed_implications: List[Tuple], encoder: CNFEncoder,
                            strategies: List[Tuple[str, str, str]], point_tuple: Tuple[str, str, str]) -> List[
    List[int]]:
    clauses = []
    for prem, c1, c2 in parsed_implications:
        instantiate_implication(prem, c1, c2, encoder, clauses, strategies, point_tuple)
    return clauses


def ne_unit_literals_for_point(encoder: CNFEncoder, point_tuple: Tuple[str, str, str], X_domain, Y_domain, Z_domain) -> \
        List[int]:
    lits = []
    for x in X_domain:
        left = (x, point_tuple[1], point_tuple[2])
        right = point_tuple
        lits.append(encoder.get_var(1, left, right))
    for y in Y_domain:
        left = (point_tuple[0], y, point_tuple[2])
        right = point_tuple
        lits.append(encoder.get_var(2, left, right))
    for z in Z_domain:
        left = (point_tuple[0], point_tuple[1], z)
        right = point_tuple
        lits.append(encoder.get_var(3, left, right))
    return lits


def ne_clauses_for_point(encoder: CNFEncoder, point_tuple: Tuple[str, str, str], X_domain, Y_domain, Z_domain) -> List[
    List[int]]:
    lits = ne_unit_literals_for_point(encoder, point_tuple, X_domain, Y_domain, Z_domain)
    return [[lit] for lit in lits]


def step1_find_havePNE(omega_csv='generate_combination_sat.csv', havePNE_out='havePNE.csv'):
    rows = list(csv.reader(open(omega_csv, newline='', encoding='utf-8')))
    start = 0
    if rows and rows[0] and 'Rule' in rows[0][0]:
        start = 1

    Xs = ['sx'];
    Ys = ['sy'];
    Zs = ['sz']
    strategies = make_strategies(Xs, Ys, Zs)
    encoder = CNFEncoder(strategies)
    base_clauses = []
    add_sigmaG_clauses(encoder, base_clauses)

    total = 0
    kept = 0

    with open(havePNE_out, 'w', newline='', encoding='utf-8') as outf:
        writer = csv.writer(outf)
        writer.writerow(['Omega'])
        for r in rows[start:]:
            line = r[0].strip()
            total += 1
            parsed = parse_omega_line(line)
            clauses = list(base_clauses)
            point_tuple = ('sx', 'sy', 'sz')
            clauses.extend(omega_parsed_to_clauses(parsed, encoder, strategies, point_tuple))
            clauses.extend(ne_clauses_for_point(encoder, point_tuple, Xs, Ys, Zs))
            sl = Solver(name='glucose3')
            for c in clauses:
                sl.add_clause(c)
            sat = sl.solve()
            sl.delete()
            if sat:
                writer.writerow([line])
                kept += 1

    print(f"STEP1: Read {total} rows from {omega_csv}")
    print(f"STEP1: Output {havePNE_out} with {kept} rows")
    return havePNE_out


def step2_check_lambda(havePNE_csv='havePNE.csv', failUNE_out='failUNE.csv', uniqueUNE_out='uniqueUNE.csv'):
    rows = list(csv.reader(open(havePNE_csv, newline='', encoding='utf-8')))
    start = 0
    if rows and rows[0] and 'Omega' in rows[0][0]:
        start = 1

    Xs = ['a', 'ap'];
    Ys = ['b', 'bp'];
    Zs = ['c', 'cp']
    strategies = make_strategies(Xs, Ys, Zs)
    encoder = CNFEncoder(strategies)
    base_clauses = []
    add_sigmaG_clauses(encoder, base_clauses)

    p1 = ('a', 'b', 'c')
    p2 = ('ap', 'bp', 'cp')

    total = 0
    failing = 0
    unique = 0

    with open(failUNE_out, 'w', newline='', encoding='utf-8') as fail_file, \
            open(uniqueUNE_out, 'w', newline='', encoding='utf-8') as unique_file:

        fail_writer = csv.writer(fail_file)
        unique_writer = csv.writer(unique_file)

        fail_writer.writerow(['Omega', 'reason'])
        unique_writer.writerow(['Omega'])

        for r in rows[start:]:
            line = r[0].strip()
            total += 1
            parsed = parse_omega_line(line)

            clauses = list(base_clauses)
            clauses.extend(omega_parsed_to_clauses(parsed, encoder, strategies, p1))
            clauses.extend(omega_parsed_to_clauses(parsed, encoder, strategies, p2))
            for lit in ne_unit_literals_for_point(encoder, p1, Xs, Ys, Zs):
                clauses.append([lit])
            for lit in ne_unit_literals_for_point(encoder, p2, Xs, Ys, Zs):
                clauses.append([lit])

            lit_list = []
            for player in (1, 2, 3):
                v1 = encoder.get_var(player, p1, p2)
                v2 = encoder.get_var(player, p2, p1)
                lit_list.append(-v1)
                lit_list.append(-v2)

            clauses.append(lit_list)

            sl = Solver(name='glucose3')
            for c in clauses:
                sl.add_clause(c)
            sat = sl.solve()
            sl.delete()

            if sat:
                fail_writer.writerow([line, f"counterexample with NE(p1) and NE(p2); model exists violating λ"])
                failing += 1
            else:
                unique_writer.writerow([line])
                unique += 1

    print(f"STEP2: Read {total} rows from {havePNE_csv}")
    print(f"STEP2: Output {failUNE_out} with {failing} rows")
    print(f"STEP2: Output {uniqueUNE_out} with {unique} rows")
    return failUNE_out, uniqueUNE_out


if __name__ == '__main__':
    t0 = time.time()
    havePNE = step1_find_havePNE('generate_combination_sat.csv', 'havePNE.csv')
    failUNE, uniqueUNE = step2_check_lambda(havePNE, 'failUNE.csv', 'uniqueUNE.csv')
    t1 = time.time()
    print(f"Total runtime: {t1 - t0:.2f} seconds")
    print(f"Final output files: {havePNE}, {failUNE}, {uniqueUNE}")