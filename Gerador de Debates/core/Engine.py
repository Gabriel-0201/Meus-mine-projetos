import time


class MsgDebate:
  def __init__(self, defensor, critico):
    self.defensor = defensor
    self.critico = critico

    self.historico = []

  def run_debate(self, rounds: int = 3): # 3 rounds como padrão

    ultima_fala = None
    
    for i in range(rounds):
      #vez do defensor
      resposta_defensor = self.defensor.gerar(ultima_fala)
      ultima_fala = resposta_defensor
      time.sleep(1)

      #vez do critico
      resposta_critico = self.critico.gerar(ultima_fala)
      ultima_fala = resposta_critico
      time.sleep(1)
      
      #salvando round
      self.historico.append(f"{self.defensor.nome}: {resposta_defensor}")
      self.historico.append(f"{self.critico.nome}: {resposta_critico}")
    return self.historico