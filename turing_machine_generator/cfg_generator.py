import argparse
from itertools import product


def parse_turing_machine(path):
    file = open(path)
    init_state = file.readline().replace('\n', '')
    final_state = file.readline().replace('\n', '')
    input_symbols = file.readline().replace('\n', '').split(' ')
    type_symbols = file.readline().replace('\n', '').split(' ')
    transition_function = dict()
    for line in file.readlines():
        in_state, in_symbol, _, to_state, type_symbol, direction = line.replace('\n', '').split(' ')
        key = (in_state, in_symbol)
        if transition_function.keys().__contains__(key):
            transition_function[key].append((to_state, type_symbol, direction))
        else:
            transition_function[key] = list()
            transition_function[key].append((to_state, type_symbol, direction))
    file.close()
    return input_symbols, type_symbols, transition_function, init_state, final_state


def generate_productions(input_symbols, type_symbols, transition_function, init_state, accept_state):
    first = 'First'
    second = 'Second'
    productions = []
    productions += [(f'{first}', f'[,_]{init_state}{second}[,_][,_]')]
    productions += [(f'{second}', f'[{a},{a}]{second}') for a in input_symbols]
    productions += [(f'{second}', '')]
    t_input_symbols = input_symbols + ['']
    for a in t_input_symbols:
        for left, rights in transition_function.items():
            q, c = left
            for right in rights:
                p, d, m = right
                if m == 'r':
                    l_rule = f'{q}[{a},{c}]'
                    r_rule = f'[{a},{d}]{p}'
                    productions.append((l_rule, r_rule))
                else:
                    for b, e in product(t_input_symbols, type_symbols):
                        l_rule = f'[{b},{e}]{q}[{a},{c}]'
                        r_rule = f'{p}[{b},{e}][{a},{d}]'
                        productions.append((l_rule, r_rule))

    for a, c in product(input_symbols, type_symbols):
        productions.append((f'[{a},{c}]{accept_state}', f'{accept_state}{a}'))
        productions.append((f'{accept_state}[{a},{c}]', f'{accept_state}{a}{accept_state}'))

    for c in type_symbols:
        productions.append((f'[,{c}]{accept_state}', accept_state))
        productions.append((f'{accept_state}[,{c}]', accept_state))

    productions.append((accept_state, ''))

    return productions


def save_grammar(path, productions):
    grammar = open(path, 'w')
    lines = [f"{left} -> {right}\n" for left, right in productions]
    grammar.writelines(lines)
    grammar.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-tm", "--turing_machine_path", help="Path to turing machine file", required=False, type=str, default="./TM.txt")
    parser.add_argument("-g", "--grammar_path", help="Output grammar path", required=False, type=str, default="./cfg_prime_grammar.txt")
    args = parser.parse_args()

    input_symbols, type_symbols, transition_function, init_state, accept_state = parse_turing_machine(args.turing_machine_path)

    productions = generate_productions(input_symbols, type_symbols, transition_function, init_state, accept_state)

    save_grammar(args.grammar_path, productions)


if __name__ == '__main__':
    main()
