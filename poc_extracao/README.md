# POC: extração de promessas e pendências em conversas de vendas

Lê uma conversa (WhatsApp, transcrição, registros do CRM) e devolve dados estruturados: perguntas abertas do cliente, promessas do vendedor com prazo, de quem é a vez, objeções, motivo real da perda e uma tarefa sugerida com rascunho de mensagem.

## Arquivos
- `01_schema_extracao.json`: os campos que o modelo preenche.
- `02_prompt_sistema.md`: as instruções dadas ao modelo.
- `03_parse_conversas.py` → `conversas.json`: as 13 conversas do PDF em formato estruturado (já gerado).
- `extrair.py`: roda o modelo em cada conversa (ou em uma só, ou "voltando no tempo" com `--ate`).
- `gabarito_rascunho.json`: resposta esperada, RASCUNHO a ser revisado por você.
- `avaliar.py`: compara a saída do modelo com o gabarito e gera `relatorio.md`.

## Como rodar
1. `pip install anthropic`
2. Crie uma chave de API em console.anthropic.com e rode `export ANTHROPIC_API_KEY=...` (no Windows: `set ANTHROPIC_API_KEY=...`).
3. Teste sem custo: `python extrair.py --id 3 --dry-run` (mostra o que seria enviado).
4. Rode tudo: `python extrair.py`. As saídas ficam em `saidas/`.
5. Revise `gabarito_rascunho.json` com o seu julgamento e rode `python avaliar.py`.
6. Teste a "viagem no tempo": `python extrair.py --id 3 --ate 2026-06-19` (o sistema teria percebido as 2 perguntas sem resposta no mesmo dia?).

## Limites conhecidos
- O modelo usado é configurável pela variável `MODELO`.
- As datas do PDF não têm ano; o parser assume 2026.
- Nada aqui está conectado ao HubSpot. Os dados do case são confidenciais: apague `conversas.json` e `saidas/` ao fim do processo.
