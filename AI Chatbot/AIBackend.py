import google.generativeai as genai
from PIL import Image
import io
import fitz

def pdf_to_text(file_path):
    text = ""
    pdf_document = fitz.open(file_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text += page.get_text()
    pdf_document.close()
    return text

class Conversation:
    def __init__(self):
        with open(r"C:\Users\eyupi\OneDrive\Masaüstü\Neurazum\model.txt", "r") as file:
            api_key = file.read().strip()

        genai.configure(api_key=api_key)

        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 4096,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        self.convo = model.start_chat(history=[])

    def send_message(self, message):
        self.convo.send_message(message)
        response_text = self.convo.last.text.replace("Gemini", "NeurAI").replace("Google", "BrAIn")
        return response_text

    def send_pdf(self, file_path):
        pdf_text = pdf_to_text(file_path)
        self.convo.send_message(pdf_text)
        response_text = self.convo.last.text.replace("Gemini", "NeurAI").replace("Google", "BrAIn")
        return response_text


conversation = Conversation()

def main():
    while True:
        message = input("You: ")
        if message.lower() == 'exit':
            break
        elif message.lower().startswith('pdf'):
            file_path = message.split(' ', 1)[1]
            response = conversation.send_pdf(file_path)
        else:
            response = conversation.send_message(message)
        print("NeurAI: " + response)

if __name__ == "__main__":
    main()
