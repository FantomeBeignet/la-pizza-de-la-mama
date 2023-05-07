package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"

	"golang.org/x/exp/maps"
)

type Ingredients map[string]struct{}

func (s Ingredients) Add(elt string) {
	s[elt] = struct{}{}
}

func (s Ingredients) Includes(elt string) bool {
	_, ok := s[elt]
	return ok
}

func (s Ingredients) Remove(elt string) {
	delete(s, elt)
}

type Client struct {
	likes    Ingredients
	dislikes Ingredients
}

func (c Client) LikesPizza(pizza Ingredients) bool {
	for k := range c.likes {
		if !pizza.Includes(k) {
			return false
		}
	}
	for k := range pizza {
		if !c.dislikes.Includes(k) {
			return false
		}
	}
	return true
}

func ParseInput(filename string) (Ingredients, []Client) {
	file, err := os.Open("/path/to/file.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	// Read first line
	scanner.Scan()
	num_clients, err := strconv.Atoi(scanner.Text())
	if err != nil {
		log.Fatal(err)
	}

	ingredients := Ingredients{}
	var clients []Client

	for i := 0; i < num_clients; i++ {
		likes := Ingredients{}
		dislikes := Ingredients{}
		scanner.Scan()
		client_likes := strings.Split(scanner.Text(), " ")
		if num_likes, err := strconv.Atoi(client_likes[0]); err != nil && num_likes > 0 {
			for _, v := range client_likes[1:] {
				ingredients.Add(v)
				likes.Add(v)
			}
		}
		scanner.Scan()
		client_dislikes := strings.Split(scanner.Text(), " ")
		if num_dislikes, err := strconv.Atoi(client_dislikes[0]); err != nil && num_dislikes > 0 {
			for _, v := range client_dislikes[1:] {
				ingredients.Add(v)
				dislikes.Add(v)
			}
		}
		clients = append(clients, Client{likes: likes, dislikes: dislikes})
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return ingredients, clients
}

func SaveSolution(file string, pizza Ingredients) {
	f, err := os.Create(file)
	if err != nil {
		log.Fatal(err)
	}
	f.WriteString(fmt.Sprintf("%d %s", len(pizza), strings.Join(maps.Keys(pizza), " ")))
}

func SatisfiedClients(pizza Ingredients, clients []Client) int {
	res := 0
	for _, c := range clients {
		if c.LikesPizza(pizza) {
			res += 1
		}
	}
	return res
}
