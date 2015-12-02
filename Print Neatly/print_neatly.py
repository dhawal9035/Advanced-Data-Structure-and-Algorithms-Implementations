import sys
import numpy

INFINITY = sys.maxint


def print_neatly(words, M):
    """
    >>> print_neatly(["Dhawal", "loves", "to", "code"],10)
    (72, 'Dhawal\\nloves to\\ncode')
    >>> print_neatly(["Dhawal", "loves", "cricket", "and", "football"],15)
    (91, 'Dhawal loves\\ncricket and\\nfootball')
    """
    word_length = len(words)
    total_cost = numpy.zeros((word_length+1, word_length+1))
    total_cost = total_cost.astype(int)
    for i in range(1, word_length+1):
        total_cost[i][i] = M - len(words[i-1])
        for j in range(i+1, word_length+1):
            total_cost[i][j] = total_cost[i][j - 1] - len(words[j-1]) - 1

    for i in range(1, word_length+1):
        for j in range(i, word_length+1):
            if total_cost[i][j] < 0:
                total_cost[i][j] = INFINITY
            elif j == word_length and total_cost[i][j] >= 0:
                total_cost[i][j] = 0
            else:
                total_cost[i][j] **= 3

    cost = numpy.zeros(word_length+1)
    word_index = numpy.zeros(word_length+1)
    word_index = word_index.astype(int)

    for j in range(1, word_length+1):
        cost[j] = INFINITY
        for i in range(1, j+1):
            if cost[i-1] + total_cost[i][j] < cost[j]:
                cost[j] = cost[i-1] + total_cost[i][j]
                word_index[j] = i
    cost = int(cost[-1])
    text = determine_text(word_length, word_index, words)
    return cost, text


def determine_text(word_length, word_index, words):
    x = word_length-1
    y = word_index[-1] - 1
    z = y + 1
    textlist = []
    text = ''
    textlist.append(words[int(z-1):x+1])
    while y >= 1:
        textlist.append(words[int(word_index[y]-1):int(y)])
        y = word_index[y] - 1
    for i in range(len(textlist)-1, -1, -1):
        text += " ".join(str(y) for y in textlist[i])
        text += "\n"
    text = text[:-1]
    return text
