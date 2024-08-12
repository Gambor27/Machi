package main

import "time"

type Request struct {
	Model    string `json:"model"`
	Messages []Message
	Stream   bool `json:"stream"`
}

type Response struct {
	Model     string    `json:"model"`
	CreatedAt time.Time `json:"created_at"`
	Message   struct {
		Role    string `json:"role"`
		Content string `json:"content"`
	} `json:"message"`
	DoneReason         string `json:"done_reason"`
	Done               bool   `json:"done"`
	TotalDuration      int64  `json:"total_duration"`
	LoadDuration       int64  `json:"load_duration"`
	PromptEvalCount    int    `json:"prompt_eval_count"`
	PromptEvalDuration int    `json:"prompt_eval_duration"`
	EvalCount          int    `json:"eval_count"`
	EvalDuration       int64  `json:"eval_duration"`
}

type LLM struct {
	Model       string
	BaseURL     string
	Temperature float32
}

type Message struct {
	Role    string
	Content string
}
