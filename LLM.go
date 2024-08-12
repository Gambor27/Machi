package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
	"bufio"
	"log"
	"os"
)

func (llm LLM) GetReply(messages []Message) (Response, error) {
	client := http.Client{Timeout: time.Minute}
	fullURL := llm.BaseURL + "/api/chat"

	request := Request{
		Model:    llm.Model,
		Messages: messages,
		Stream:   false,
	}

	body, err := json.Marshal(request)
	if err != nil {
		return Response{}, err
	}

	requestBody := bytes.NewBuffer(body)

	req, err := http.NewRequest("POST", fullURL, requestBody)
	if err != nil {
		return Response{}, err
	}

	resp, err := client.Do(req)
	if err != nil {
		return Response{}, err
	}

	defer resp.Body.Close()

	if resp.StatusCode > 399 {
		return Response{}, fmt.Errorf("bad status: %v", resp.StatusCode)
	}

	data, err := io.ReadAll(resp.Body)
	if err != nil {
		return Response{}, err
	}

	response := Response{}
	err = json.Unmarshal(data, &response)
	if err != nil {
		return Response{}, err
	}

	return response, nil
}

func (llm LLM) DefineChatbot(prompt string) ([]Message) {
	messages := make([]Message, 0)
	aiDefinition := Message{
		Role:    "system",
		Content: prompt,
	}
	messages = append(messages, aiDefinition)
	return messages
}

func (llm LLM) GetIntent(prompt string) (string, error) {
	messages := make([]Message, 0)
	message := Message{
		Role:    "user",
		Content: prompt,
	}
	aiDefinition := Message{
		Role:    "system",
		Content: intent,
	}
	messages = append(messages, aiDefinition, message)
	response, err := llm.GetReply(messages)
	if err != nil {
		return "", err
	}
	fmt.Println(response.Message.Content)
	return response.Message.Content, nil
}

func (llm LLM) Conversation(context []Message) {
	input := bufio.NewScanner(os.Stdin)
	messages := context
	for {
		fmt.Print(len(messages))
		fmt.Print("> ")
		input.Scan()
		userInput := input.Text()

		intent, err := llm.GetIntent(userInput)
		if err != nil {
			log.Fatal(err)
		}

		switch intent {
		case "exit":
			os.Exit(0)
		}

		message := Message{
			Role:    "user",
			Content: userInput,
		}
		messages = append(messages, message)

		response, err := llm.GetReply(messages)
		if err != nil {
			log.Fatal(err)
		}
		messages = append(messages, Message(response.Message))
		fmt.Println(response.Message.Content)

	}
}