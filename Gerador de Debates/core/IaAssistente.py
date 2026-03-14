import google.generativeai as genai
import time

class IaAssistente:
  def __init__(self, persona: str, api_key: str, model_name: str, tokens: int, temp: float = 0.3):
    genai.configure(api_key= api_key)

    config = { #configurações da ia
      'temperature' : temp, #padrão 0.3 
      'max_output_tokens' : tokens + 100 #Margem de erro para tokens
    }

    #Definindo modo de geração da ia
    self.model = genai.GenerativeModel(model_name= model_name,
                                       generation_config= config,
                                       system_instruction=(
                                                            f"Persona: {persona}\n"
                                                            f"ESTILO DE RESPOSTA: Extremamente conciso. "
                                                            f"Sua resposta DEVE ter no máximo 2 frases e "
                                                            f"OBRIGATORIAMENTE terminar com um ponto final antes de esgotar o espaço. "
                                                            f"Nunca deixe uma frase incompleta. Se estiver sem espaço, pare na frase anterior."
                                                        )
                                       )

    self.chat = self.model.start_chat(history=[]) #inicia o chat vazio

  def gerar(self, prompt: str) -> str:
    for i in range(3): #numero padão de tentativas
      try:
        response = self.chat.send_message(prompt)
        texto = response.text.split()

        if texto and texto[-1] not in ['.', '!', '?', '"']:
          texto += '...'
        time.sleep(3)

        return texto
      except Exception as e:
        api_erro = str(e)

        if '429' in str(e):
          print('limite batido \nesperando 15 sgd para tentar novamente...')
          time.sleep(15)
          continue
      return f" Erro ao chamar a ia: {api_erro}\n"
    print(api_erro)
    return "Erro: A API está instável no momento."
  
