import argparse
from itertools import product


def parse_LBA(path):
    lba = open(path)

    init_state = lba.readline().replace("init: ", "").strip()
    accept_state = lba.readline().replace("accept: ", "").strip()

    sigma = lba.readline().replace("sigma: {", "").replace("}", "").strip().split(", ")
    gamma = lba.readline().replace("gamma: {", "").replace("}", "").strip().split(", ")

    lines = list(filter(lambda s: s != '\n', lba.readlines()))
    lines = list(map(lambda s: s.strip().split(","), lines))

    transition_function = {}
    left = map(tuple, lines[::2])
    right = map(tuple, lines[1::2])
    for l, r in zip(left, right):
        if l in transition_function.keys():
            transition_function[l] += [r]
        else:
            transition_function.update({l: [r]})

    lba.close()

    return sigma, gamma, transition_function, init_state, accept_state


def init_config_single(sigma, init_state, init_symbol):
    return [(init_symbol, f'[{init_state},$,{a},{a},#]') for a in sigma]


def movement_config_single(sigma, gamma, transition_function, accept_state):
    productions = []
    for a in sigma:
        for left, rights in transition_function.items():
            q, x = left
            if q != accept_state:
                for right in rights:
                    p, y, d = right
                    if y == '$' and x == '$' and d == '>':
                        for g in gamma:
                            l_rule = f'[{q},$,{x},{a},#]'
                            r_rule = f'[$,{p},{x},{a},#]'
                            productions.append((l_rule, r_rule))
                    elif y == '#' and x == '#' and d == '<':
                        for g in gamma:
                            l_rule = f'[$,{g},{a},{q},#]'
                            r_rule = f'[$,{p},{g},{a},#]'
                            productions.append((l_rule, r_rule))
                    elif d == '<':
                        l_rule = f'[$,{q},{x},{a},#]'
                        r_rule = f'[{p},$,{y},{a},#]'
                        productions.append((l_rule, r_rule))
                    elif d == '>':
                        l_rule = f'[$,{q},{x},{a},#]'
                        r_rule = f'[$,{y},{a},{p},#]'
                        productions.append((l_rule, r_rule))

    return productions


def restore_word_accept(sigma, gamma, accept_state):
    productions = []
    for a in sigma:
        for g in gamma:
            productions.append((f'[{accept_state},$,{g},{a},#]', a))
            productions.append((f'[$,{accept_state},{g},{a},#]', a))
            productions.append((f'[$,{g},{a},{accept_state},#]', a))
    return productions


def init_config_general(sigma, init_state, init_symbol_1, init_symbol_2):
    productions = []
    for a in sigma:
        productions.append((init_symbol_1, f'[{init_state},$,{a},{a}]{init_symbol_2}'))
        productions.append((init_symbol_2, f'[{a},{a}]{init_symbol_2}'))
        productions.append((init_symbol_2, f'[{a},{a},#]'))
    return productions


def movement_config_left(sigma, gamma, transition_function, accept_state):
    productions = []
    for a in sigma:
        for left, rights in transition_function.items():
            q, x = left
            if q != accept_state:
                for right in rights:
                    p, y, d = right
                    if y == '$' and x == '$' and d == '>':
                        for g in gamma:
                            productions.append(
                                (f'[{q},$,{g},{a}]', f'[$,{p},{g},{a}]'))
                    elif d == '<':
                        productions.append((f'[$,{q},{x},{a}]', f'[{p},$,{y},{a}]'))
                    elif d == '>':
                        for z, b in product(gamma, sigma):
                            l_rule = f'[$,{q},{x},{a}][{z},{b}]'
                            r_rule = f'[$,{y},{a}][{p},{z},{b}]'
                            productions.append((l_rule, r_rule))

                            l_rule = f'[$,{q},{x},{a}][{z},{b},#]'
                            r_rule = f'[$,{y},{a}][{p},{z},{b},#]'
                            productions.append((l_rule, r_rule))
    return productions


def movement_config_center(sigma, gamma, transition_function, accept_state):
    productions = []
    for a in sigma:
        for left, rights in transition_function.items():
            q, x = left
            if q != accept_state:
                for right in rights:
                    p, y, d = right
                    if x in gamma and y in gamma:
                        for z, b in product(gamma, sigma):
                            if d == '>':
                                l_rule = f'[{q},{x},{a}][{z},{b}]'
                                r_rule = f'[{y},{a}][{p},{z},{b}]'
                                productions.append((l_rule, r_rule))

                                l_rule = f'[{q},{x},{a}][{z},{b},#]'
                                r_rule = f'[{y},{a}][{p},{z},{b},#]'
                                productions.append((l_rule, r_rule))
                            else:
                                l_rule = f'[{z},{b}][{q},{x},{a}]'
                                r_rule = f'[{p},{z},{b}][{y},{a}]'
                                productions.append((l_rule, r_rule))

                                l_rule = f'[$,{z},{b}][{q},{x},{a}]'
                                r_rule = f'[$,{p},{z},{b}][{y},{a}]'
                                productions.append((l_rule, r_rule))

    return productions


def movement_config_right(sigma, gamma, transition_function, accept_state):
    productions = []
    for a in sigma:
        for left, rights in transition_function.items():
            q, x = left
            if q != accept_state:
                for right in rights:
                    p, y, d = right
                    if y == '#' and x == '#' and d == '<':
                        for g in gamma:
                            productions.append(
                                (f'[{g},{a},{q},#]', f'[{p},{g},{a},#]'))
                    elif d == '>':
                        productions.append(
                            (f'[{q},{x},{a},#]', f'[{y},{a},{p},#]'))
                    elif d == '<':
                        for z, b in product(gamma, sigma):
                            l_rule = f'[{z},{b}][{q},{x},{a},#]'
                            r_rule = f'[{p},{z},{b}][{y},{a},#]'
                            productions.append((l_rule, r_rule))

                            l_rule = f'[$,{z},{b}][{q},{x},{a},#]'
                            r_rule = f'[$,{p},{z},{b}][{y},{a},#]'
                            productions.append((l_rule, r_rule))
    return productions


def restore_word_accepted(sigma, gamma, accept_state):
    productions = []
    for x, a in product(gamma, sigma):
        productions.append((f'[{accept_state},$,{x},{a}]', a))
        productions.append((f'[$,{accept_state},{x},{a}]', a))
        productions.append((f'[{accept_state},{x},{a}]', a))
        productions.append((f'[{accept_state},{x},{a},#]', a))
        productions.append((f'[{x},{a},{accept_state},#]', a))
    return productions


def restore_word_general(sigma, gamma):
    productions = []
    for x, a, b in product(gamma, sigma, sigma):
        productions.append((f'{a}[{x},{b}]', f'{a}{b}'))
        productions.append((f'{a}[{x},{b},#]', f'{a}{b}'))
        productions.append((f'[{x},{a}]{b}', f'{a}{b}'))
        productions.append((f'[$,{x},{a}]{b}', f'{a}{b}'))
    return productions


def build_cs_grammar(sigma, gamma, transition_function, init_state, accept_state):
    gamma += sigma
    first = 'First'
    second = 'Second'

    productions = init_config_single(sigma, init_state, first)
    productions += movement_config_single(sigma, gamma, transition_function, accept_state)
    productions += restore_word_accept(sigma, gamma, accept_state)
    productions += init_config_general(sigma, init_state, first, second)
    productions += movement_config_left(sigma, gamma, transition_function, accept_state)
    productions += movement_config_center(sigma, gamma, transition_function, accept_state)
    productions += movement_config_right(sigma, gamma, transition_function, accept_state)
    productions += restore_word_accepted(sigma, gamma, accept_state)
    productions += restore_word_general(sigma, gamma)

    return productions, first


def save_grammar(path, productions, sigma):
    grammar = open(path, 'w')
    grammar.write(str(*sigma) + ' $ #\n')
    grammar.writelines(sorted(left + " -> " + right + '\n' for left, right in productions))
    grammar.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-lba", "--lba_path", help="Path to lba file", required=False, type=str, default="./LBA.txt")
    parser.add_argument("-g", "--grammar_path", help="Output grammar path", required=False,
                        type=str, default="./csg_prime_grammar.txt")
    args = parser.parse_args()

    sigma, gamma, transition_function, init_state, accept_state = parse_LBA(args.lba_path)
    productions, init_symbol = build_cs_grammar(sigma, gamma, transition_function, init_state, accept_state)

    save_grammar(args.grammar_path, productions, sigma)


if __name__ == '__main__':
    main()
