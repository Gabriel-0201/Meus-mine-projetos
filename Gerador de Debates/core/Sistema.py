import os

class Sistema:
  def __init__(self, pasta_destino = 'debates_salvos'):
    self.pasta_destino = pasta_destino
    if not os.path.exists(self.pasta_destino): #garente que exeista uma pasta destino
      os.makedirs(self.pasta_destino)

  def gerar_nome_arquivo(self, base_nome:str): #responsavel por criar o arquivo
    indice = 1
    while True:
      nome = f"{base_nome}{indice if indice > 1 else ''}.txt"
      caminho = os.path.join(self.pasta_destino, nome)
      if not os.path.exists(caminho):
        return caminho
      indice += 1
  
  def gerar_ata(self, analisador, dialogo_lista: list, tema: str, nucleo: str):
    texto_debate = ""
    for t in dialogo_lista:
      texto_debate += f"{t['debatente']}: {t['argumento']}\n\n"

    prompt_analise = f"""
        Como redator profissional, analise o debate abaixo sobre '{tema}'.
        Foco principal: {nucleo}.

        ESTRUTURA DA ATA:
        1. INTRODUÇÃO: Resumo do objetivo do debate.
        2. PONTOS DO DEFENSOR: Liste os 3 principais argumentos.
        3. PONTOS DO CONTRARIADOR: Liste os 3 principais argumentos.
        4. CONCLUSÃO FINAL: Avalie a consistência lógica de cada lado.

        TRANSCRICÃO DO DEBATE:
        {texto_debate}
        """
    return analisador.gerar(prompt= prompt_analise)

  def salvar(self, dialogo: list, ata: str, caminho_arq: str):

    with open(caminho_arq, 'a', encoding= 'utf-8') as arquivo:
      #savando o debate
      for turno in dialogo:
        arquivo.write(f"{turno['debatente']}: {turno['argumento']}\n")
      
      #savando a ata
      arquivo.write(f"ATA:\n\n {ata} \n")
        
      arquivo.write("-" * 30 + "\n") # Separador de debates