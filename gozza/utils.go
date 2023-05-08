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

type (
	Ingredients map[string]struct{}
	Pizza       Ingredients
)

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

func (s Pizza) Add(elt string) {
	s[elt] = struct{}{}
}

func (s Pizza) Includes(elt string) bool {
	_, ok := s[elt]
	return ok
}

func (s Pizza) Remove(elt string) {
	delete(s, elt)
}

type Client struct {
	likes    Ingredients
	dislikes Ingredients
}

func (c Client) LikesPizza(pizza Pizza) bool {
	for k := range c.likes {
		if !pizza.Includes(k) {
			return false
		}
	}
	for k := range pizza {
		if c.dislikes.Includes(k) {
			return false
		}
	}
	return true
}

func ParseInput(filename string) (Ingredients, []Client) {
	file, err := os.Open(filename)
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
		clientLikes := strings.Split(scanner.Text(), " ")
		numLikes, err := strconv.Atoi(clientLikes[0])
		if err != nil {
			log.Fatal(err)
		}
		if numLikes > 0 {
			for _, v := range clientLikes[1:] {
				ingredients.Add(v)
				likes.Add(v)
			}
		}
		scanner.Scan()
		clientDislikes := strings.Split(scanner.Text(), " ")
		numDislikes, err := strconv.Atoi(clientDislikes[0])
		if err != nil {
			log.Fatal(err)
		}
		if numDislikes > 0 {
			for _, v := range clientDislikes[1:] {
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

func SaveSolution(file string, pizza Pizza) {
	f, err := os.Create(file)
	if err != nil {
		log.Fatal(err)
	}
	f.WriteString(fmt.Sprintf("%d %s", len(pizza), strings.Join(maps.Keys(pizza), " ")))
}

func SatisfiedClients(pizza Pizza, clients []Client) int {
	res := 0
	for _, c := range clients {
		if c.LikesPizza(pizza) {
			res += 1
		}
	}
	return res
}
