import sys
from itertools import combinations
from utils import parse_input, satisfied_clients, save_solution

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    ingredients, clients = parse_input(input_file)
    max_score = 0
    best_res = set()
    print(ingredients, clients)
    for i in range(1, len(ingredients)):
        for c in combinations(ingredients, i):
            score = satisfied_clients(set(c), clients)
            print(c, score)
            if score > max_score:
                max_score = score
                best_res = set(c)
    save_solution(best_res, output_file)
