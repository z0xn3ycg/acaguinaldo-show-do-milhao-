import os
import random
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

# Carrega o .env a partir da pasta deste arquivo, independentemente
# da pasta de trabalho escolhida no PyCharm ou no VS Code.
load_dotenv(dotenv_path=Path(__file__).resolve().with_name(".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip().rstrip("/")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()
JOGO_ID = os.getenv("JOGO_ID", "show-do-milhao").strip()

PREMIOS = [1000, 5000, 10000, 25000, 50000, 100000, 200000, 500000, 1000000]
NIVEIS = ("facil", "media", "dificil")


def headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }


def conectado():
    return bool(SUPABASE_URL and SUPABASE_KEY and "SEU-PROJETO" not in SUPABASE_URL)


def buscar_perguntas():
    if not conectado():
        raise RuntimeError(
            "Configure SUPABASE_URL e SUPABASE_KEY no arquivo jogo/.env."
        )

    resposta = requests.get(
        f"{SUPABASE_URL}/rest/v1/perguntas",
        headers=headers(),
        params={
            "select": "id,enunciado,alternativa_a,alternativa_b,alternativa_c,"
                      "alternativa_d,correta,dificuldade",
            "order": "id.asc",
        },
        timeout=20,
    )
    resposta.raise_for_status()
    perguntas = resposta.json()

    for nivel in NIVEIS:
        quantidade = sum(p.get("dificuldade") == nivel for p in perguntas)
        if quantidade < 5:
            raise RuntimeError(
                f"O banco precisa ter pelo menos 5 perguntas de cada nível. "
                f"Foram encontradas {quantidade} em '{nivel}'."
            )
    return perguntas


def montar_partida(perguntas):
    selecionadas = []
    for nivel in NIVEIS:
        grupo = [p for p in perguntas if p["dificuldade"] == nivel]
        selecionadas.extend(random.sample(grupo, 3))
    return selecionadas


def calcular_premio(acertos):
    if acertos <= 0:
        return 0
    return PREMIOS[acertos - 1]


def salvar_partida(resultado):
    if not conectado():
        raise RuntimeError("Configure a conexão com o Supabase antes de salvar.")

    # O mesmo UUID é mantido nas tentativas. A chave primária evita duplicações.
    resposta = requests.post(
        f"{SUPABASE_URL}/rest/v1/partidas",
        headers={
            **headers(),
            "Prefer": "resolution=ignore-duplicates,return=representation",
        },
        json=resultado,
        timeout=20,
    )
    resposta.raise_for_status()
    return resposta.json()


def consultar_ranking():
    if not conectado():
        print("Configure a conexão com o Supabase para consultar o ranking.")
        return

    try:
        resposta = requests.get(
            f"{SUPABASE_URL}/rest/v1/ranking",
            headers=headers(),
            params={
                "select": "id,apelido,valor_ganho,tempo_segundos,data_hora",
                "jogo_id": f"eq.{JOGO_ID}",
                "order": "valor_ganho.desc,tempo_segundos.asc,data_hora.asc,id.asc",
                "limit": "10",
            },
            timeout=20,
        )
        resposta.raise_for_status()
        dados = resposta.json()

        print("\n=== RANKING — SHOW DO MILHÃO ===")
        if not dados:
            print("Ainda não existem resultados para este jogo.")
            return

        for posicao, partida in enumerate(dados, start=1):
            minutos, segundos = divmod(int(float(partida["tempo_segundos"])), 60)
            premio = float(partida["valor_ganho"])
            print(
                f'{posicao}. {partida["apelido"]} — '
                f'R$ {premio:,.2f} — {minutos:02d}:{segundos:02d}'
            )
    except (requests.RequestException, ValueError) as erro:
        print(f"Falha ao consultar o ranking: {erro}")


def solicitar_apelido():
    apelido = input("Digite seu apelido: ").strip()
    while not apelido:
        apelido = input("O apelido não pode ficar vazio. Digite novamente: ").strip()
    return apelido


def jogar():
    apelido = solicitar_apelido()

    try:
        perguntas = montar_partida(buscar_perguntas())
    except (requests.RequestException, RuntimeError, ValueError) as erro:
        print(f"Não foi possível iniciar a partida: {erro}")
        return

    partida_id = str(uuid.uuid4())
    acertos = 0
    premio = 0
    motivo = "nove_acertos"
    inicio = None

    print("\nResponda com A, B, C ou D. Você também pode digitar DESISTIR.")

    for indice, pergunta in enumerate(perguntas):
        if inicio is None:
            inicio = time.perf_counter()

        print(
            f"\nPergunta {indice + 1}/9 "
            f"({pergunta['dificuldade'].upper()}): {pergunta['enunciado']}"
        )
        for letra in "abcd":
            print(f"  {letra.upper()}) {pergunta['alternativa_' + letra]}")

        resposta = input("Sua resposta: ").strip().lower()
        while resposta not in ("a", "b", "c", "d", "desistir"):
            resposta = input(
                "Entrada inválida. Digite A, B, C, D ou DESISTIR: "
            ).strip().lower()

        if resposta == "desistir":
            motivo = "desistencia"
            break

        if resposta != pergunta["correta"].strip().lower():
            motivo = "erro"
            print(f"Resposta incorreta. A correta era {pergunta['correta'].upper()}.")
            break

        acertos += 1
        premio = calcular_premio(acertos)
        print(f"Resposta correta! Prêmio atual: R$ {premio:,.2f}")

    fim = time.perf_counter()
    duracao = round(fim - inicio, 2) if inicio is not None else 0.0

    if acertos == 9:
        motivo = "nove_acertos"

    resultado = {
        "id": partida_id,
        "jogo_id": JOGO_ID,
        "apelido": apelido,
        "valor_ganho": premio,
        "tempo_segundos": duracao,
        "acertos": acertos,
        "motivo_encerramento": motivo,
        "data_hora": datetime.now(timezone.utc).isoformat(),
    }

    print(
        f"\nFim da partida, {apelido}! "
        f"Você fez {acertos} acerto(s) e ganhou R$ {premio:,.2f}."
    )
    print(f"Tempo: {duracao:.2f} segundos. Motivo: {motivo}.")

    # O resultado fica em memória enquanto o programa estiver aberto.
    # O jogador pode tentar novamente sem precisar jogar outra partida.
    while True:
        try:
            salvar_partida(resultado)
            print("Resultado enviado ao banco com sucesso.")
            break
        except (requests.RequestException, RuntimeError) as erro:
            print(f"Não foi possível confirmar o salvamento: {erro}")
            opcao = input(
                "Tentar enviar novamente? (s = sim / n = deixar pendente): "
            ).strip().lower()
            if opcao == "s":
                continue
            print(
                "Resultado mantido nesta execução. "
                f"Anote o ID para referência: {partida_id}"
            )
            break


def main():
    while True:
        print("\n=== SHOW DO MILHÃO ===")
        print("1 - Iniciar partida")
        print("2 - Consultar ranking")
        print("3 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            jogar()
        elif opcao == "2":
            consultar_ranking()
        elif opcao == "3":
            print("Até a próxima!")
            break
        else:
            print("Opção inválida. Escolha 1, 2 ou 3.")


if __name__ == "__main__":
    main()
