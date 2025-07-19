import google.generativeai as genai

API_KEY="AIzaSyDlOz6rh5Xpenh8SDk00l7hHYYoLQjWwEY"
genai.configure(api_key=API_KEY)

model=genai.GenerativeModel("gemini-2.0-flash")
chat=model.start_chat()

print("Chat with gemini! Type 'exit' to quit." )
while True:
    user_input=input("You: ")
    if user_input.lower()=='exit':
        break 
response=chat.send_message("Hello")
print("Gemini:", response.text)