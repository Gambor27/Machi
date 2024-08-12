import openai

client = openai.OpenAI(
    api_key="anything",
    base_url="http://msi:11434/v1"
)


conversation = [{"role":"system", "content":"You are the central processor for a smart house. Your role is to analyze strings of user input text for desire analysis and sort them into the cases of [Lights, Weather, Recipe, Other].  Your response should be in the form of a JSON object with a field \"Reason\" that contains 25-50 words on why you chose your selection, and a field \"Category\" that is the category chosen."}]

while True:
    user_prompt = input("> ")
    if user_prompt == "exit":
        break
    conversation.append({"role":"user", "content":user_prompt})
    response = client.chat.completions.create(model = "dolphin-llama3", messages = conversation, temperature= 0.8, frequency_penalty= 0.8)
    reply = response.choices[0].message.content
    print(reply)
    conversation.append({"role":"assistant", "content":reply})