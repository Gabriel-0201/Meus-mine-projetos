#05/02/26 - 06/02/26 - 07/02/26 -
from fpdf import FPDF
import google.generativeai as genai


class AssistenteIa:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def gerar(self, prompt):
        try:
            resposta = self.model.generate_content(prompt)
            return resposta.text
        except Exception as e:
            return f"Erro na IA: {e}"


class App:
    def __init__(self, assistente):
        self.assistente = assistente
  
    def coletar(self):
        evento = input('Evento: ').strip().title()
        if not evento:
            return None
        
        topico = input('Topico: ').strip()
        if not topico:
            return None
        
        items = input('Produtos e preços (ex: bolo: 2.50, suco: 5): ')
        if not items:
            return None

        lista_itens = items.split(',')
        dicionario_produtos = {}

        for item in lista_itens:
            if ':' in item:
                nome, preco = item.split(':')
                try:
                    dicionario_produtos[nome.strip().title()] = float(preco.strip())
                except ValueError:
                    print('erro: use "produto: numero"')
                    return None

        if not dicionario_produtos:
            return None
        
        pessoas = input('numero de pessoas: ')
        try:
            pessoas = int(pessoas)
        except ValueError:
            return None

        local_evento = input('local do evento (seja especifico): ').strip()
        if not local_evento:
            return None
        
        regiao_compra = input('região de compra das mercadorias (seja especifico): ').strip()
        if not regiao_compra:
            return None
        
        return {
            'evento': evento,
            'topico': topico,
            'produtos': dicionario_produtos,
            'pessoas': pessoas,
            'local': local_evento,
            'região_compra' : regiao_compra
        }

    def analise_com_IA(self, dados):
        prompt = f"""
Você é um especialista em organização de eventos e análise de custos.

CONTEXTO DO EVENTO:
Evento: {dados['evento']}
Tópico: {dados['topico']}
Número de pessoas: {dados['pessoas']}
Local de ocorrência: {dados['local']}
Região de compra: {dados['região_compra']}

PRODUTOS E CUSTOS INFORMADOS:
{dados['produtos']}

TAREFAS:
1. Para cada produto, informe preços prováveis de mercado.
2. Gere um relatório estratégico curto sobre o evento.
3. Sugira um valor total de venda.
4. Dê dicas e alertas importantes.

REGRAS:
- Não invente marcas.
- Sem emojis e sem explicações introdutórias.
- Não use '**' no texto.
- Use EXATAMENTE o formato abaixo.

[PRECOS_IA]
(apenas valor)

[RELATORIO]
...

[SUGESTAO]
(apenas numero)

[OBS]
...
"""
        return self.assistente.gerar(prompt)

    def extrair(self, texto, tag):
      tag = tag.upper()

      if f"[{tag}]" not in texto:
            return "Conteúdo não gerado pela IA. "
      
      parte = texto.split(f'[{tag}]')[1]
      
      proximas_tags = ["PRECOS_IA", "RELATORIO", "SUGESTAO", "OBS"]
      proximas_tags.remove(tag)
    
      fim = len(parte)
      for t in proximas_tags:
          pos = parte.find(f'[{t}]')

          if pos != -1 and pos < fim:
            fim = pos
    
      return parte[:fim].strip()

    def criar_pdf(self, dados, analise):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Fonte base
        pdf.set_font("Arial", size=12)

        # ===== TÍTULO =====
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, dados["evento"], ln=True, align="C")
        pdf.ln(5)

        # ===== TÓPICO =====
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Tópico:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, dados["topico"])
        pdf.ln(4)

        # ===== PRODUTOS =====
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Produtos informados:", ln=True)
        pdf.set_font("Arial", size=12)

        for produto, valor in dados["produtos"].items():
            pdf.cell(0, 8, f"{produto} - R$ {valor:.2f}", ln=True)

        pdf.ln(6)

        # ===== PRECOS IA =====
        precos_ia = self.extrair(analise, "PRECOS_IA")
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Preços de mercado (IA):", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, precos_ia)
        pdf.ln(5)

        # ===== SUGESTÃO =====
        sugestao = self.extrair(analise, "SUGESTAO")
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Sugestão de valor:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, sugestao)
        pdf.ln(5)

        # ===== RELATÓRIO =====
        relatorio = self.extrair(analise, "RELATORIO")
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Relatório estratégico:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, relatorio)
        pdf.ln(5)

        # ===== OBS =====
        obs = self.extrair(analise, "OBS")
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Observações:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, obs)

        # ===== SALVAR =====
        nome_arquivo = f"{dados['evento'].replace(' ', '_')}.pdf"
        pdf.output(nome_arquivo)

        print(f"PDF gerado com sucesso: {nome_arquivo}")



def main():
    api = 'SUA_API_KEY'
    assistente = AssistenteIa(api)
    app = App(assistente)

    while True:
        dados = app.coletar()
        if dados:
            break
        print('preencha corretamente')

    analise = app.analise_com_IA(dados)

    app.criar_pdf(dados, analise)

main()

