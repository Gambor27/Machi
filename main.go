package main


func main() {
	var LLM = LLM{
		Model:       "llama3",
		BaseURL:     "http://main:11434",
		Temperature: 0.7,
	}
	init := LLM.DefineChatbot(machi)
	LLM.Conversation(init)
}
