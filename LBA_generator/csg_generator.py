import argparse
import os


def parse_LBA(path, save_path):
    lineList = [line.rstrip('\n') for line in open(path, "r")]
    init = lineList[0].split()[1]
    accept = lineList[1].split()[1]
    sigma = lineList[2].replace("sigma: {", "").replace(
        "}", "").replace(" ", "").split(",")
    gamma = lineList[3].replace("gamma: {", "").replace(
        "}", "").replace(" ", "").split(",") + sigma

    curLine = 5
    delta = []
    while curLine < len(lineList):
        if lineList[curLine] == "" or lineList[curLine][0] == "/":
            curLine += 1
            continue
        delta.append(lineList[curLine].replace(" ", "").split(
            ",") + lineList[curLine + 1].replace(" ", "").split(","))
        curLine += 3

    rules = []
    # 1+4
    for a in sigma:
        rules.append((["A_1"], ["[" + init + ", #, " + a + ", " + a + ", #]"]))
        rules.append((["A_1"], ["[" + init + ", #, " + a + ", " + a + "]", "A_2"]))
        rules.append((["A_2"], ["[" + a + ", " + a + "]", "A_2"]))
        rules.append((["A_2"], ["[" + a + ", " + a + ", #]"]))
    # 2
    for de in delta:
        for a in sigma:
            if de[4] == ">":
                if de[1] == "#":
                    for e in gamma:
                        rules.append((["[" + de[0] + ", #, " + e + ", " + a + ", #]"],  # 2.1
                                      ["[#, " + de[2] + ", " + e + ", " + a + ", #]"]))
                else:
                    rules.append((["[#, " + de[0] + ", " + de[1] + ", " + a + ", #]"],  # 2.3
                                  ["[#, " + de[3] + ", " + a + ", " + de[2] + ", #]"]))
            else:
                if de[1] == "#":
                    for e in gamma:
                        rules.append((["[#, " + e + ", " + a + ", " + de[0] + ", #]"],  # 2.4
                                      ["[#, " + de[2] + ", " + e + ", " + a + ", #]"]))
                else:
                    rules.append((["[#, " + de[0] + ", " + de[1] + ", " + a + ", #]"],  # 2.2
                                  ["[" + de[2] + ", #, " + de[3] + ", " + a + ", #]"]))
    # 3
    for a in sigma:
        for x in gamma:
            rules.append((["[" + accept + ", #, " + x + ", " + a + ", #]"],
                          [a]))
            rules.append((["[#, " + accept + ", " + x + ", " + a + ", #]"],
                          [a]))
            rules.append((["[#, " + x + ", " + a + ", " + accept + ", #]"],
                          [a]))

    # 5
    for de in delta:
        for a in sigma:
            if de[4] == ">":
                if de[1] == "#":
                    for e in gamma:
                        rules.append((["[" + de[0] + ", #, " + e + ", " + a + "]"],
                                      ["[#, " + de[2] + ", " + e + ", " + a + "]"]))
                else:
                    for z in gamma:
                        for b in sigma:
                            rules.append((["[#, " + de[0] + ", " + de[1] + ", " + a + "]", "[" + z + ", " + b + "]"],
                                          ["[#, " + de[3] + ", " + a + "]", "[" + de[2] + ", " + z + ", " + b + "]"]))
                            rules.append(
                                (["[#, " + de[0] + ", " + de[1] + ", " + a + "]", "[" + z + ", " + b + ", #]"],
                                 ["[#, " + de[3] + ", " + a + "]", "[" + de[2] + ", " + z + ", " + b + ", #]"]))
            else:
                rules.append((["[#, " + de[0] + ", " + de[1] + ", " + a + "]"],
                              ["[" + de[2] + ", #, " + de[3] + ", " + a + "]"]))
    # 6
    for de in delta:
        for a in sigma:
            for b in sigma:
                if de[4] == ">":
                    for z in gamma:
                        rules.append((["[" + de[0] + ", " + de[1] + ", " + a + "]", "[" + z + ", " + b + "]"],
                                      ["[" + de[3] + ", " + a + "]", "[" + de[2] + ", " + z + ", " + b + "]"]))
                        rules.append((["[" + de[0] + ", " + de[1] + ", " + a + "]", "[" + z + ", " + b + ", #]"],
                                      ["[" + de[3] + ", " + a + "]", "[" + de[2] + ", " + z + ", " + b + ", #]"]))
                else:
                    for z in gamma:
                        rules.append((["[" + z + ", " + b + "]", "[" + de[0] + ", " + de[1] + ", " + a + "]"],
                                      ["[" + de[2] + ", " + z + ", " + b + "]", "[" + de[3] + ", " + a + "]"]))
                        rules.append((["[#, " + z + ", " + b + "]", "[" + de[0] + ", " + de[1] + ", " + a + "]"],
                                      ["[#, " + de[2] + ", " + z + ", " + b + "]", "[" + de[3] + ", " + a + "]"]))
    # 7
    for de in delta:
        for a in sigma:
            if de[4] == ">":
                rules.append((["[" + de[0] + ", " + de[1] + ", " + a + ", #]"],
                              ["[" + de[3] + ", " + a + ", " + de[2] + ", #]"]))
            else:
                if de[1] == "#":
                    for e in gamma:
                        rules.append((["[" + e + ", " + a + ", " + de[0] + ", #]"],
                                      ["[" + de[2] + ", " + e + ", " + a + ", #]"]))
                else:
                    for z in gamma:
                        for b in sigma:
                            rules.append((["[" + z + ", " + b + "]", "[" + de[0] + ", " + de[1] + ", " + a + ", #]"],
                                          ["[" + de[2] + ", " + z + ", " + b + "]", "[" + de[3] + ", " + a + ", #]"]))
    # 8
    for a in sigma:
        for x in gamma:
            rules.append((["[" + accept + ", #, " + x + ", " + a + "]"],
                          [a]))
            rules.append((["[#, " + accept + ", " + x + ", " + a + "]"],
                          [a]))
            rules.append((["[" + accept + ", " + x + ", " + a + "]"],
                          [a]))
            rules.append((["[" + accept + ", " + x + ", " + a + ", #]"],
                          [a]))
            rules.append((["[" + x + ", " + a + ", " + accept + ", #]"],
                          [a]))
    # 9
    for a in sigma:
        for b in sigma:
            for x in gamma:
                rules.append(([a, "[" + x + ", " + b + "]"],
                              [a, b]))
                rules.append(([a, "[" + x + ", " + b + ", #]"],
                              [a, b]))
                rules.append((["[" + x + ", " + a + "]", b],
                              [a, b]))
                rules.append((["[#, " + x + ", " + a + "]", b],
                              [a, b]))

    bufferFile = "grammar_tmp_lba.txt"
    tmp = open(bufferFile, "w")

    tmp.write(lineList[2] + "\n")  # sigma
    for a, b in rules:
        if "" in a:
            a.remove("")
        if "" in b:
            b.remove("")
        s1 = str(a)[1:-1] + " -> " + str(b)[1:-1]
        tmp.write(s1 + "\n")
    tmp.close()

    def converter(pair):
        pair4 = []
        for el in pair:
            pair2 = el.split("', ")
            pair3 = []
            for el2 in pair2:
                pair3.append(el2.replace("'", ""))
            pair4.append(tuple(pair3))
        return pair4

    lineList = [line.rstrip('\n') for line in open(bufferFile, "r")]

    sigma = lineList[0].replace("sigma: {", "").replace(
        "}", "").replace(" ", "").split(",")

    lineList.pop(0)
    rules = [converter(line.split(" -> ")) for line in lineList]

    size = 7
    numOfStage1Commands = 4
    activeRules = set()
    q = []
    stage2 = []
    tmp = set()
    q.append(["A_1"])
    while q:
        word = q.pop(0)
        if tuple(word) in tmp:
            continue
        tmp.add(tuple(word))
        is_terminal = True
        for i in range(len(word)):
            if word[i] in ["A_1", "A_2", "A_3", "A_4"]:
                is_terminal = False
            for ix, rule in enumerate(rules[:numOfStage1Commands]):
                flag = True
                for j in range(len(rule[0])):
                    if i + j >= len(word) or word[i + j] != rule[0][j]:
                        flag = False
                        break
                if flag:
                    activeRules.add(ix)
                    newWord = word.copy()
                    for j in range(len(rule[0])):
                        newWord.pop(i)
                    for j in range(len(rule[1])):
                        if rule[1][len(rule[1]) - j - 1] != "":
                            newWord.insert(i, rule[1][len(rule[1]) - j - 1])
                    if len(newWord) <= size:
                        q.append(newWord)

        if is_terminal:
            stage2.append(word)
    # for i in stage2:
    #     print(i)
    st = set()
    while stage2:
        word = stage2.pop(0)
        if tuple(word) in st:
            continue
        st.add(tuple(word))
        is_terminal = True
        for i in range(len(word)):
            if word[i] not in sigma:
                is_terminal = False
            for ix, rule in enumerate(rules[numOfStage1Commands:]):
                flag = True
                for j in range(len(rule[0])):
                    if i + j >= len(word) or word[i + j] != rule[0][j]:
                        flag = False
                        break
                if flag:
                    activeRules.add(ix + numOfStage1Commands)
                    newWord = word.copy()
                    for j in range(len(rule[0])):
                        newWord.pop(i)
                    for j in range(len(rule[1])):
                        if rule[1][len(rule[1]) - j - 1] != "":
                            newWord.insert(i, rule[1][len(rule[1]) - j - 1])
                    stage2.append(newWord)
                    # print(newWord)
        # if is_terminal:
        #     for i in word:
        #         print(i, end = "")
        #     print()
    out = open(save_path, "w")
    lineList = [line.rstrip('\n') for line in open(bufferFile, "r")]
    out.write(lineList[0] + "\n")
    for ix, rule in enumerate(lineList):
        if ix - 1 in activeRules:
            out.write(rule + "\n")

    out.close()
    os.remove("grammar_tmp_lba.txt")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-lba", "--lba_path", help="Path to lba file", required=False, type=str, default="./LBA.txt")
    parser.add_argument("-g", "--grammar_path", help="Output grammar path", required=False,
                        type=str, default="./csg_prime_grammar.txt")
    args = parser.parse_args()

    parse_LBA(args.lba_path, args.grammar_path)


if __name__ == '__main__':
    main()
