def parse_input(file: str) -> tuple[set[str], list[tuple[set[str], set[str]]]]:
    ingredients: set[str] = set()
    clients: list[tuple[set[str], set[str]]] = []
    with open(file, "r") as input:
        num_clients = int(input.readline().strip())
        for _ in range(num_clients):
            likes: set[str] = set()
            dislikes: set[str] = set()
            client_likes = input.readline().strip().split(" ")
            if int(client_likes[0]) > 0:
                for ingredient in client_likes[1:]:
                    ingredients.add(ingredient)
                    likes.add(ingredient)
            client_dislikes = input.readline().strip().split(" ")
            if int(client_dislikes[0]) > 0:
                for ingredient in client_dislikes[1:]:
                    ingredients.add(ingredient)
                    dislikes.add(ingredient)
            clients.append((likes, dislikes))
    return ingredients, clients


def save_solution(ingredients: set[str], file: str):
    with open(file, "w") as output:
        output.write(f"{len(ingredients)} " + " ".join(list(ingredients)))


def likes_pizza(pizza: set[str], client: tuple[set[str], set[str]]) -> bool:
    for ingredient in client[0]:
        if (ingredient not in pizza):
            return False
    # Disliked ingredients
    for ingredient in pizza:
        if (ingredient in client[1]):
            return False
    return True


def satisfied_clients(pizza: set[str], clients: list[tuple[set[str], set[str]]]) -> int:
    return sum(map(lambda c: 1 if likes_pizza(pizza, c) else 0, clients))
