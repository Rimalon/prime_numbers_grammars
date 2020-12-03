import argparse
from collections import deque


def word_generator(productions, init_symbol_1, init_symbol_2, input_symbol, counter):
    q = deque([init_symbol_1])
    st = set()
    c = 1
    productions_list = list()
    result_productions_dict = dict()
    result_rules_dict = dict()
    while len(q):
        word = q.popleft()
        if word not in st:
            st.add(word)
            if all(c == input_symbol for c in word):
                if counter != c:
                    c += 1
                else:
                    prime_number_word = word
                    result_productions_dict[prime_number_word] = ''
                    result_rules_dict[prime_number_word] = 'Word was applied'
                    productions_list.reverse()
                    for lp, rp, left, right in productions_list:
                        if rp in result_productions_dict.keys():
                            result_productions_dict[lp] = rp
                            result_rules_dict[lp] = left + ' -> ' + right
                    result_file = open('./prime_generator_result.txt', 'w')
                    for key, value in result_productions_dict.items().__reversed__():
                        result_file.write('Applied rule: ' + result_rules_dict[key] + '\nResult replacement: ' + key + ' -> ' + value + '\n\n')
                yield word
            else:
                for left, right in productions:
                    if left in word:
                        new_word = word.replace(left, right)
                        productions_list.append((word, new_word, left, right))
                        if any(S in new_word for S in [init_symbol_1, init_symbol_2]):
                            q.append(new_word)
                        else:
                            q.appendleft(new_word)


def read_free_grammar(path):
    grammar = open(path)
    str_productions = [line.strip('\n') for line in grammar.readlines()]
    productions = []
    for line in str_productions:
        line = line.split(' -> ')
        productions += [tuple(line)] if len(line) > 1 else [(line[0], '')]
    grammar.close()
    return productions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--grammar_path", help="Path to file with grammar",
                        type=str, default="./free_prime_grammar.txt")
    parser.add_argument("-n", help="Prime numbers amount", default=10, type=int)
    args = parser.parse_args()

    productions = read_free_grammar(args.grammar_path)
    gen = word_generator(productions, 'First', 'Second', 'I', args.n)

    for i in range(args.n):
        print(len(gen.__next__()))


if __name__ == '__main__':
    main()