import argparse
from collections import deque


def word_generator(productions, init_symbol_1, init_symbol_2, input_symbol):
    q = deque([init_symbol_1])
    st = set()
    while len(q):
        word = q.popleft()
        if word not in st:
            st.add(word)
            if all(c == input_symbol for c in word):
                yield word
            else:
                for left, right in productions:
                    if left in word:
                        new_word = word.replace(left, right)
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
    gen = word_generator(productions, 'First', 'Second', 'I')

    for i in range(args.n):
        print(len(gen.__next__()))


if __name__ == '__main__':
    main()