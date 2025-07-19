import google.generativeai as genai

genai.configure(api_key="AIzaSyDlOz6rh5Xpenh8SDk00l7hHYYoLQjWwEY")  # Replace with your actual key

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

def chat_with_gemini(prompt):
    try:
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {e}"
