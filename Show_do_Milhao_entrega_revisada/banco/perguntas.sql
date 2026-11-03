-- 15 perguntas iniciais, com fonte para conferência.
-- INSERT idempotente: não duplica perguntas já cadastradas pelo enunciado.
insert into public.perguntas
(enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, correta, dificuldade, fonte)
select v.enunciado, v.alternativa_a, v.alternativa_b, v.alternativa_c, v.alternativa_d, v.correta, v.dificuldade, v.fonte
from (values
('Qual palavra-chave cria uma função em Python?', 'function', 'def', 'fun', 'make', 'b', 'facil', 'https://docs.python.org/3/reference/compound_stmts.html#function-definitions'),
('Qual tipo representa texto em Python?', 'int', 'float', 'str', 'bool', 'c', 'facil', 'https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str'),
('Qual símbolo é usado para comentário de uma linha?', '//', '#', '<!--', '**', 'b', 'facil', 'https://docs.python.org/3/reference/lexical_analysis.html#comments'),
('Qual comando mostra uma mensagem na tela?', 'input()', 'print()', 'write()', 'show()', 'b', 'facil', 'https://docs.python.org/3/library/functions.html#print'),
('Qual estrutura permite repetir enquanto uma condição for verdadeira?', 'if', 'for', 'while', 'def', 'c', 'facil', 'https://docs.python.org/3/reference/compound_stmts.html#the-while-statement'),
('Qual estrutura armazena pares de chave e valor?', 'lista', 'tupla', 'dicionário', 'conjunto', 'c', 'media', 'https://docs.python.org/3/library/stdtypes.html#mapping-types-dict'),
('Qual método adiciona um item ao final de uma lista?', 'append()', 'add()', 'insert_end()', 'pushback()', 'a', 'media', 'https://docs.python.org/3/tutorial/datastructures.html#more-on-lists'),
('O que len(lista) retorna?', 'O último item', 'A quantidade de elementos', 'A soma dos elementos', 'O tipo da lista', 'b', 'media', 'https://docs.python.org/3/library/functions.html#len'),
('Qual comando trata uma possível exceção?', 'try/except', 'if/else', 'for/in', 'def/return', 'a', 'media', 'https://docs.python.org/3/tutorial/errors.html#handling-exceptions'),
('Qual é o resultado de 10 // 3 em Python?', '3.33', '1', '3', '4', 'c', 'media', 'https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations'),
('O que é uma API?', 'Um tipo de monitor', 'Uma interface para sistemas trocarem dados', 'Uma linguagem de marcação', 'Um antivírus', 'b', 'dificil', 'https://developer.mozilla.org/en-US/docs/Glossary/API'),
('Qual biblioteca é comumente usada para fazer requisições HTTP em Python?', 'random', 'requests', 'turtle', 'math', 'b', 'dificil', 'https://requests.readthedocs.io/en/latest/'),
('Para que serve uma chave primária em um banco de dados?', 'Permitir valores repetidos', 'Identificar unicamente cada registro', 'Ordenar por nome automaticamente', 'Criptografar todas as tabelas', 'b', 'dificil', 'https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-PRIMARY-KEYS'),
('Qual cuidado é essencial ao publicar um site conectado ao Supabase?', 'Publicar a senha administrativa', 'Colocar a chave secreta no HTML', 'Configurar permissões e não expor chaves administrativas', 'Desativar toda segurança', 'c', 'dificil', 'https://supabase.com/docs/guides/api/api-keys'),
('O que time.perf_counter() fornece?', 'Data atual', 'Um relógio de alta resolução para medir intervalos', 'Número aleatório', 'Uso de memória', 'b', 'dificil', 'https://docs.python.org/3/library/time.html#time.perf_counter')
) as v(enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, correta, dificuldade, fonte)
where not exists (select 1 from public.perguntas p where p.enunciado = v.enunciado);

-- Confira no Supabase se há pelo menos 5 perguntas em cada dificuldade:
-- select dificuldade, count(*) from public.perguntas group by dificuldade order by dificuldade;