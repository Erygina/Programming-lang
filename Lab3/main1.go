package main

import (
	"fmt"
	"time"
)

type Token struct {
	data      string
	recipient int
	ttl       int
}

type Node struct {
	ID   int
	prev chan Token
	next chan Token
}

func initializeRing(size int) []*Node {
	var ring []*Node

	first := &Node{
		ID:   0,
		next: make(chan Token),
	}
	ring = append(ring, first)

	for i := 1; i < size; i++ {
		node := &Node{
			ID:   i,
			prev: ring[i-1].next,
			next: make(chan Token),
		}
		ring = append(ring, node)
	}
	first.prev = ring[size-1].next

	return ring
}

func (node *Node) operate() {
	for incomingToken := range node.prev {
		node.handle(incomingToken)
	}
}

func (node *Node) handle(token Token) {
	if token.recipient == node.ID {
		fmt.Printf("Токен: %s доставлен!\n", token.data)
		fmt.Printf("Адресат %d\n", token.recipient)
		fmt.Printf("(срок действия ttl = %d)\n", token.ttl)
	} else if token.ttl > 0 {
		token.ttl -= 1
		node.next <- token
	} else {
		fmt.Printf("Истек срок действия токена для адресата %d\n", token.recipient)
	}
}

func main() {
	var N int
	fmt.Print("Введите количество узлов N: ")
	fmt.Scan(&N)
	ring := initializeRing(N)

	for _, node := range ring {
		go node.operate()
	}

	centralNode := ring[len(ring)/2].next
	var token Token
	fmt.Print("Введите текст токена, номер получателя и срок действия ttl: ")
	fmt.Scan(&token.data, &token.recipient, &token.ttl)
	centralNode <- token

	time.Sleep(1 * time.Second)
}
