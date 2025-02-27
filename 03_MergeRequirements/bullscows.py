import random
import sys
import cowsay
import urllib.request

def bullscows(guess: str, riddle: str) -> (int, int):
    bull = 0
    cows = 0
    guess_dict = {i:0 for i in guess}
    riddle_dict = {i:0 for i in riddle}
    for i, j in zip(guess, riddle):
        if i == j:
            bull += 1
            continue
        guess_dict[i] += 1
        riddle_dict[j] += 1
    for i in set(guess_dict.keys()).intersection(set(riddle_dict.keys())):
        cows += min(guess_dict[i], riddle_dict[i])
    return bull, cows

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    riddle = random.choice(words)
    print(riddle)
    cnt = 0
    b = 0
    while b != len(riddle):
        cnt += 1
        guess = ask("Введите слово: ", words)
        b, c = bullscows(guess, riddle)
        inform("Быки: {}, Коровы: {}", b, c)
    return cnt

def ask(prompt: str, valid: list[str] = None) -> str:
    s = input(prompt)
    if valid:
        while s not in valid:
            s = input(prompt)
    return s

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))

if __name__ == '__main__':
    if len(sys.argv) > 2:
        l = int(sys.argv[2])
    else:
        l = 5
    try:
        words = urllib.request.urlopen(sys.argv[1]).read().decode().split('\n')
    except ValueError:
        words = open(sys.argv[1]).read().split('\n')
    if words[-1] == '':
        words = words[:-1]
    print("Количество попыток:", gameplay(ask, inform, words)) 
