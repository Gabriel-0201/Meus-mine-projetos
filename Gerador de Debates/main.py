from gui import Interface
from core.IaAssistente import IaAssistente
from core.Sistema import Sistema

import os
import time
from dotenv import load_dotenv

load_dotenv() # Carrega o arquivo .env


def gerar_debate(dados: dict): #main
  dialogo = []
  sistema = Sistema()

  MINHA_API_KEY = os.getenv("GEMINI_API_KEY")
  MODEL = 'gemini-2.5-flash' #'models/gemini-2.0-flash' #'gemini-2.5-flash'

  #definindo arquivo de debates
  caminho_arquivo = sistema.gerar_nome_arquivo(base_nome= 'Debate')

  #Traduzir a 'perspectiva' em números de tokens
  mapa_tokens = {"Direto": 250, "Moderado": 400, "Palestrante": 800}

  #define o como será o debate com os parametros da Gui
  tema = dados['tema'] #ideia pricipal
  nucleo = dados['nucleo'] #parte mas importante da ideia
  max_tokens = mapa_tokens.get(dados['perspectiva'], 400)
  temp_defensor =dados['temp_pro']
  temp_contrariador = dados['temp_contra']

  #Define as ia's
  defensor = IaAssistente(
    persona=f'''Você argumentará sobre o tema {tema}.
                seu papel será defender fervorosamente {nucleo}''',
    api_key= MINHA_API_KEY,
    model_name= MODEL,
    tokens= max_tokens,
    temp= temp_defensor)
  
  contrariador = IaAssistente(
    persona=f'''Você agumentara sobre o tema {tema}.
                seu papel será criticar {nucleo}''',
    api_key= MINHA_API_KEY,
    model_name= MODEL,
    tokens= max_tokens,
    temp= temp_contrariador)
  
  redator = IaAssistente(
      persona="Você é um redator de atas profissional, neutro e analítico.",
      api_key=MINHA_API_KEY,
      model_name=MODEL,
      tokens=1000, # Atas precisam de mais espaço
      temp=0.1)

  #___Fluxo do Debate___
  for i in range(3): #Define a quantidades de turnos
    if i == 0: # se for o primeiro turno
      resposta = defensor.gerar("Apresente seu argumento inicial.")
    else:
      resposta = defensor.gerar(f"O oponente disse: '{ultima_fala}'. Contra-argumente.")

    dialogo.append({'debatente': 'Defensor', 'argumento': resposta})

    #vez do contrariador
    resposta = contrariador.gerar(f"O oponente disse: '{resposta}'. Responda à altura.")
    dialogo.append({'debatente': 'Contrariador', 'argumento': resposta})

    ultima_fala = resposta

    print(f"Turno {i+1} concluído...")
  #___Fluxo do Debate___

  #___Gerar Ata___
  print("Debate finalizado. Aguardando estabilização da API para gerar a Ata...")
  time.sleep(20)
  print("Ata Gerando")

  ata = sistema.gerar_ata(
        analisador= redator,
        dialogo_lista= dialogo,
        tema= tema,
        nucleo= nucleo
      )
  #___Gerar Ata___

  sistema.salvar(dialogo, ata, caminho_arquivo)
  print(f"\nDebate finalizado e salvo em: {caminho_arquivo}")

if __name__ == "__main__":
  app = Interface(800, 500, "AI Debate Generator", comando_gerar=gerar_debate)
  app.rodar()