# Show do Milhão — Python, Supabase e ranking web

## Integrantes
- Integrante 1: **Giancarlo Vilardo**
- Integrante 2: **Miguel Homem de Melo**
- Turma: **1º IA B**

## Conteúdo
- `jogo/main.py`: jogo no terminal.
- `jogo/requirements.txt`: bibliotecas necessárias.
- `jogo/.env.example`: modelo de configuração (não contém credenciais reais).
- `banco/schema.sql`: tabelas, políticas RLS e visão do ranking.
- `banco/perguntas.sql`: 15 perguntas iniciais com fontes de referência.
- `site/`: página de ranking que consulta o Supabase.
- `prompts.md`: registro de uso de IA — a dupla deve completar com o histórico integral real.
- `TESTES.md`: casos obrigatórios e espaço para resultados observados.
- `ENTREGA_MOODLE.txt`: dados a copiar para o campo de texto do Moodle.

## 1. Banco Supabase
No projeto Supabase já criado pela dupla:

1. Abra o **SQL Editor**.
2. Execute `banco/schema.sql`.
3. Execute `banco/perguntas.sql`.
4. Confira a quantidade de perguntas:
   ```sql
   select dificuldade, count(*)
   from public.perguntas
   group by dificuldade
   order by dificuldade;
   ```
   O esperado é pelo menos 5 perguntas em cada nível.
5. Confira se o jogo existe:
   ```sql
   select * from public.jogos;
   ```
6. Confira se a visão está disponível:
   ```sql
   select * from public.ranking limit 10;
   ```

O arquivo `perguntas.sql` evita inserir novamente uma pergunta com o mesmo enunciado. As fontes indicadas são referências oficiais ou documentação técnica para a dupla conferir; revisem cada questão e gabarito antes da entrega.

## 2. Executar no PyCharm ou VS Code
É o mesmo projeto e o mesmo arquivo Python nos dois editores.

1. Instale Python 3.10 ou superior.
2. Abra a pasta `jogo` no PyCharm ou no VS Code.
3. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv .venv
   ```
4. Ative o ambiente virtual:
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
   - Windows CMD: `.venv\Scripts\activate.bat`
5. Instale as dependências:
   ```bash
   python -m pip install -r requirements.txt
   ```
6. Copie `.env.example` e renomeie a cópia para `.env`.
7. No `.env`, preencha:
   - `SUPABASE_URL`: URL do projeto Supabase.
   - `SUPABASE_KEY`: chave anon/public do projeto.
   - `JOGO_ID`: mantenha `show-do-milhao`.
8. Execute `main.py` pelo botão Run ou pelo terminal:
   ```bash
   python main.py
   ```

O código procura o `.env` na mesma pasta de `main.py`, então funciona mesmo que PyCharm e VS Code usem pastas de trabalho diferentes.

## 3. Configurar e publicar o site no GitHub Pages
1. Abra `site/config.js`.
2. Preencha `SUPABASE_URL` e `SUPABASE_ANON_KEY` com a URL do projeto e a chave **anon/public**.
3. Nunca use `service_role`, senha do banco ou outra chave secreta no site.
4. Crie um repositório GitHub e envie a pasta `site` (ou configure o repositório para publicar essa pasta).
5. No GitHub: **Settings → Pages**. Escolha a branch e a pasta que contém `index.html`, salve e aguarde a publicação.
6. Abra o endereço fornecido pelo GitHub Pages e teste filtro e atualização do ranking.

O site lê somente a visão `ranking` e o catálogo de jogos. O jogo Python e o site devem apontar para o mesmo projeto Supabase.

## 4. Regras do jogo
- Apelido obrigatório e não vazio.
- 3 perguntas fáceis, 3 médias e 3 difíceis, sem repetição na partida.
- Prêmios fictícios: R$ 1.000, R$ 5.000, R$ 10.000, R$ 25.000, R$ 50.000, R$ 100.000, R$ 200.000, R$ 500.000 e R$ 1.000.000.
- O prêmio exibido é o último atingido, não a soma.
- A partida termina no primeiro erro, por desistência ou após 9 acertos.
- O ranking seleciona a melhor partida por apelido em cada jogo: maior prêmio, menor tempo, data mais antiga e ID.

## 5. Segurança
- `.env` não deve ser enviado ao Moodle nem publicado no GitHub.
- A chave `anon/public` pode ser usada no front-end somente com RLS e permissões configuradas corretamente.
- Nunca coloque a chave `service_role` no código Python distribuído, HTML, JavaScript ou GitHub.
- A política de inserção direta é adequada apenas ao protótipo escolar: em um sistema público real, o servidor deve validar respostas e pontuação.

## 6. Testes e evidências
Consulte `TESTES.md`. Preencha os resultados observados somente depois de executar cada teste. Guardem capturas reais:
- jogo Python com apelido, prêmio e tempo;
- site mostrando a mesma partida;
- consulta ao Supabase;
- execução nos dois editores.

## 7. Links
- Repositório GitHub: **PREENCHER**
- Site GitHub Pages: **PREENCHER**

## 8. Antes de entregar
- Preencher nomes e turma.
- Completar `prompts.md` com todos os prompts completos realmente usados pela dupla.
- Executar e registrar todos os testes.
- Publicar o site e preencher os links.
- Confirmar que `.env` não está no ZIP nem no GitHub.
- Nomear o ZIP conforme a orientação do professor: `Turma_Nome1_Nome2.zip`.
