from core.Agents import IaAgent
from core.Engine import MsgDebate
from core.Sistema import Sistema

def main():
    # Definir tema
    tema = "A contribuição da retórica na filosofia"
    nucleo = "retórica na filosofia"

    # Criar agentes
    defensor = IaAgent(
        nome="Sócrates",
        persona=(
            f"Filósofo grego que utiliza o diálogo e a retórica para questionar a sabedoria. "
            f"Seu papel é defender o tema '{tema}', destacando a importância da {nucleo}."
        )
    )

    critico = IaAgent(
        nome="Nietzsche",
        persona=(
            f"Filósofo existencialista e crítico da tradição filosófica. "
            f"Seu papel é criticar o tema '{tema}', questionando o valor da {nucleo}."
        )
    )

    # Engine do debate
    gerar_debate = MsgDebate(defensor, critico)

    # Sistema
    sistema = Sistema(pasta_main= __file__)

    # Executar debate
    debate_gerado = gerar_debate.run_debate(rounds=3)

    # Salvar resultado
    debate_formatado = "\n".join(debate_gerado)
    indice = 0

    while True:
      nome_escolhodo = "Debates" + str(indice) if indice != 0 else "Debates"

      salvar_arquivo = sistema.salvar(
          nome_arquivo= nome_escolhodo,
          conteudo= debate_formatado
      )

      if salvar_arquivo == 'Arquivo salvo com sucesso!':
         break
      
      indice += 1

if __name__ == "__main__":
    main()