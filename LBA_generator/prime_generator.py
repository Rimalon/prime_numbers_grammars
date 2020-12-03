import collections
import sys


def converter(pair):
    pair4 = []
    for el in pair:
        pair2 = el.split("', ")
        pair3 = []
        for el2 in pair2:
            pair3.append(el2.replace("'", ""))
        pair4.append(tuple(pair3))
    return pair4


fileName = ""
inputNumber = 0
if len(sys.argv) < 3:
    print("Specify number!")
    exit(0)
else:
    fileName = sys.argv[1]
    inputNumber = int(sys.argv[2])

lineList = [line.rstrip('\n') for line in open(fileName, "r")]

sigma = lineList[0].replace("sigma: {", "").replace("}", "").replace(" ", "").split(",")

lineList.pop(0)
rules = [converter(line.split(" -> ")) for line in lineList]
q = collections.deque()
tmp = set()
numOfStage1Commands = 4
q.append(["A_1"])
derivation = []


def printStack(derivation_):
    out = open("prime_generator_result.txt", "w")
    last_gen_index = 0
    for index, production in enumerate(derivation_):
        if any(elem in production for elem in ["A_1", "A_2"]):
            last_gen_index = index

    for index, production in enumerate(derivation_):
        if index > last_gen_index:
            out.write(str(production).lstrip('[').rstrip(']') + "\n")


while q:
    word = q.popleft()
    if tuple(word) in tmp:
        continue
    tmp.add(tuple(word))
    is_terminal = True
    for i in range(len(word)):
        if word[i] not in sigma:
            is_terminal = False
        for ix, rule in enumerate(rules):
            flag = True
            for j in range(len(rule[0])):
                if i + j >= len(word) or word[i + j] != rule[0][j]:
                    flag = False
                    break
            if flag:
                newWord = word.copy()
                for j in range(len(rule[0])):
                    newWord.pop(i)
                for j in range(len(rule[1])):
                    if rule[1][len(rule[1]) - j - 1] != "":
                        newWord.insert(i, rule[1][len(rule[1]) - j - 1])
                if any(elem in newWord for elem in ["A_1", "A_2"]):
                    q.append(newWord)
                else:
                    q.appendleft(newWord)

    derivation.append(word)
    if is_terminal:
        if inputNumber == len(word):
            print(f'YES, {inputNumber} is prime\nCheck [prime_generator_result.txt] for full stack')
            printStack(derivation)
            exit(0)
        elif inputNumber < len(word):
            print(f'NO, {inputNumber} is not prime.')
            exit(0)
        else:
            derivation = []