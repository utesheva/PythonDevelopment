import random
import sys
import cowsay

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
    cnt = 0
    b = 0
    while b != len(riddle):
        cnt += 1
        guess = ask("Введите слово: ", words)
        b, c = bullscows(guess, riddle)
        inform("Быки: {}, Коровы: {}", b, c)
    return cnt

