def parse_input(file: str):
    ingredients = set()
    clients = []
    with open(file, "r") as input:
        num_clients = int(input.readline().strip())
        for i in range(num_clients):
            likes = set()
            dislikes = set()
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
