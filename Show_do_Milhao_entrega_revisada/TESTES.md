# Testes e evidências — registro da dupla

**Importante:** os casos abaixo ainda precisam ser executados pela dupla no Supabase real e nos dois editores. Não marque como aprovado sem testar.

| Caso | Resultado esperado | Resultado observado | Status |
|---|---|---|---|
| 9 respostas corretas | R$ 1.000.000,00; valores não somados | A preencher | Pendente |
| Erro na 1ª questão | Encerrar com R$ 0,00 | A preencher | Pendente |
| Erro após acertos | Manter o último prêmio | A preencher | Pendente |
| Desistência | Encerrar e manter o prêmio atual | A preencher | Pendente |
| Apelido vazio | Solicitar novamente | A preencher | Pendente |
| Alternativa inválida | Solicitar novamente | A preencher | Pendente |
| Ordem das perguntas | 3 fáceis, 3 médias, 3 difíceis | A preencher | Pendente |
| Sem repetição | Nenhuma pergunta repetida na partida | A preencher | Pendente |
| Mesmo prêmio, tempos diferentes | Menor tempo primeiro | A preencher | Pendente |
| Apelido repetido | Mostrar melhor partida do apelido | A preencher | Pendente |
| Jogos diferentes | Rankings separados por jogo | A preencher | Pendente |
| Falha ao salvar | Não afirmar que salvou; permitir nova tentativa | A preencher | Pendente |
| Reenvio do mesmo UUID | Não duplicar partida | A preencher | Pendente |
| Ranking vazio | Mostrar mensagem informativa | A preencher | Pendente |
| Falha de consulta | Mostrar mensagem de erro | A preencher | Pendente |
| Persistência | Fechar Python e atualizar site; registro permanece | A preencher | Pendente |
| PyCharm | Executar e conectar ao Supabase | A preencher | Pendente |
| VS Code | Executar e conectar ao Supabase | A preencher | Pendente |

## Evidências que a dupla deve anexar
1. Captura do jogo Python mostrando apelido, prêmio e tempo.
2. Captura do site mostrando o mesmo apelido, prêmio, tempo e data.
3. Captura/registro da consulta no Supabase.
4. Captura do jogo executando no PyCharm.
5. Captura do jogo executando no VS Code.

## Problemas encontrados e correções
- Problema: o carregamento do `.env` dependia da pasta de trabalho do editor.
- Correção aplicada: o `main.py` agora carrega o `.env` usando o caminho absoluto da pasta do próprio arquivo.
- Teste de confirmação nos dois editores: **ainda pendente**.
