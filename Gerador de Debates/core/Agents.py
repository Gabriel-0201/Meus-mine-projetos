import google.generativeai as genai
import os
from dotenv import load_dotenv

class IaAgent:
  def __init__(self, nome: str, persona: str, model_name: str = "gemini-2.5-flash"):
      load_dotenv()
      genai.configure(api_key= os.getenv("GEMINI_API_KEY"))

      self.nome = nome
      self.model = genai.GenerativeModel(
          model_name=model_name,
          system_instruction=f"Você é {nome}. {persona}. Seja conciso e persuasivo. suas repostas devem ter no maximo 1000 caracteres" # da as instruções a Ia
      )
      self.chat = self.model.start_chat(history=[]) #inicia a memoria do chat

  def gerar(self, resposta_anterior: str = None) -> str:
     prompt = resposta_anterior if resposta_anterior else "Apresente seu argumanto para iniciar o debate"
     
     try:
         response = self.chat.send_message(prompt)
     except Exception as e:
        return f"Erro na API: {e}"

     return response.text