import os
import re

class Sistema:
  def __init__(self, pasta_main):
    self.pasta_main = pasta_main

  def salvar(self, nome_arquivo: str, conteudo: str):
      # limpar nome do arquivo
      nome_arquivo = re.sub(r'[\\/*?:"<>|]', "_", nome_arquivo)

      # checando se a pasta existe para criar

      # caminho da pasta do script
      base_dir = os.path.dirname(os.path.abspath(self.pasta_main))

      pasta = os.path.join(base_dir, "Debates salvos")
      os.makedirs(pasta, exist_ok=True)

      # salvando conteúdo na pasta
      caminho = os.path.join(pasta, f"{nome_arquivo}.txt")

      #se o arquivo ja existir
      if os.path.exists(caminho): 
        return "Arquivo já existe!"
      
      # salvar conteúdo
      with open(caminho, 'w', encoding='utf-8') as arquivo:
          arquivo.write(conteudo)
      
      return "Arquivo salvo com sucesso!"