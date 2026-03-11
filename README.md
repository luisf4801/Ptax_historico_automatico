🏛️ BCB PTAX Downloader (USD/BRL)
Este repositório contém um script robusto em Python para a extração massiva de dados históricos da PTAX (USD/BRL) diretamente da API Olinda do Banco Central do Brasil (SGS/BCB).

Ao contrário de abordagens simplistas que utilizam o endpoint CotacaoDolarPeriodo (que frequentemente retorna Erro 400 ou limita o volume de dados), este script utiliza o endpoint CotacaoMoedaPeriodo. Isso permite acessar o campo tipoBoletim, essencial para filtrar entre as cotações de abertura, intermediárias e o fechamento oficial.

🚀 Destaques do Projeto
Chunking Temporal: Automatiza a quebra de grandes intervalos de tempo (ex: 20 anos) em blocos anuais para evitar timeouts e limites de registros da API.

Gestão de Boletins: Permite filtrar cotações por tipo (Abertura, Intermediário, Fechamento) ou baixar o histórico completo de intradia da PTAX.

Data Science Ready: O output é um pandas.DataFrame limpo, com cálculo automático de Mid-Price e tratamento de duplicatas.

Logging Profissional: Sistema de logs integrado para monitorar o progresso da extração em tempo real.

🤖 Copiloto de Produtividade
Este código foi desenvolvido com o suporte do Claude 3.5 Sonnet. A IA foi utilizada para:

Refatoração de Lógica: Otimização do loop de requisições para garantir que nenhum dia útil fosse perdido.

Tratamento de Exceções: Implementação de retries e captura de erros HTTP específicos da API Olinda.

Documentação: Estruturação das Docstrings seguindo padrões profissionais de Engenharia de Dados.

🛠️ Requisitos
Python 3.8+

requests

pandas

📖 Como Usar
Basta ajustar as variáveis de data no final do script e executar:

Python
START   = datetime(2000, 1, 1)
END     = datetime(2025, 12, 31)
BOLETIM = "Fechamento" # Opções: "Fechamento", "Abertura", "Intermediario", "todos"

df = download_ptax(START, END, boletim=BOLETIM)
📊 Estrutura dos Dados
O DataFrame resultante contém:

timestamp: Data e hora exata da cotação.

boletim: Tipo do boletim (Abertura, 1-3 Intermediário, Fechamento).

bid: Cotação de compra.

ask: Cotação de venda.

mid: Preço médio (Bid + Ask) / 2.

Dica para o LinkedIn: Ao postar o link deste repositório na quarta-feira, você pode mencionar que este README ajuda a explicar por que o mercado financeiro precisa de dados "limpos" para modelagem macroeconômica.
