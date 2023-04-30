import random as rd
from utils import parse_input, satisfied_clients


def create_pizzas(ingredients: set[str], n: int) -> list[set[str]]:
    pizza_list = []
    for i in range(n):
        pizza = set()
        for ing in ingredients:
            if rd.random() > 0.5:
                pizza.add(ing)
        pizza_list.append(pizza)
    return pizza_list


def is_gen_good(pizza_list: list[set[str]], clients: list[tuple[set[str], set[str]]]) -> bool:
    ref_score = satisfied_clients(pizza_list[0], clients)
    for pizza in pizza_list:
        if satisfied_clients(pizza, clients) != ref_score:
            return False
    return True


# print(create_pizzas(parse_input("subject/a_exemple.txt")[0], 3))
# print(is_gen_good([{"peppers", "cheese"}, {"cheese", "mushrooms", "tomatoes", "peppers", "pineappple"}, {
#       "peppers", "mushrooms"}], parse_input("subject/a_exemple.txt")[1]))
