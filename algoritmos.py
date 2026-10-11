"""Implementação manual do Merge Sort e da função de comparação entre times.

Nenhuma função pronta de ordenação (sorted, list.sort) é usada aqui.
"""

import unicodedata

# Rótulo exibido na interface -> atributo do objeto Time.
CRITERIOS = {
    "Pontos": "pontos",
    "Vitórias": "vitorias",
    "Empates": "empates",
    "Derrotas": "derrotas",
    "Gols pró": "gols_pro",
    "Gols contra": "gols_contra",
    "Saldo de gols": "saldo_gols",
    "Nome do time": "nome",
}

# Desempates aplicados (sempre do maior para o menor) depois do critério
# principal. O nome em ordem alfabética é sempre o último desempate.
DESEMPATES = ["pontos", "vitorias", "saldo_gols", "gols_pro"]


def _normalizar_nome(nome):
    """Remove acentos e ignora maiúsculas, para que 'Grêmio' fique entre 'G...'."""
    sem_acentos = unicodedata.normalize("NFKD", nome)
    sem_acentos = "".join(c for c in sem_acentos if not unicodedata.combining(c))
    return sem_acentos.lower()


def _valor(time, atributo):
    valor = getattr(time, atributo)
    return _normalizar_nome(valor) if atributo == "nome" else valor


def sequencia_de_criterios(criterio, decrescente):
    """Lista de (atributo, decrescente) na ordem em que serão comparados.

    Ex.: criterio="saldo_gols" -> saldo, pontos, vitórias, gols pró, nome.
    """
    if criterio == "nome":
        return [("nome", decrescente)]
    sequencia = [(criterio, decrescente)]
    sequencia += [(c, True) for c in DESEMPATES if c != criterio]
    sequencia.append(("nome", False))
    return sequencia


def comparar(a, b, criterio="pontos", decrescente=True):
    """Compara dois times.

    Retorna um número negativo se `a` deve aparecer antes de `b`, positivo se
    `b` deve aparecer antes de `a` e 0 se forem equivalentes em todos os
    critérios.
    """
    for atributo, desc in sequencia_de_criterios(criterio, decrescente):
        va, vb = _valor(a, atributo), _valor(b, atributo)
        if va == vb:
            continue  # empate neste critério: passa para o próximo
        a_e_maior = va > vb
        if desc:
            return -1 if a_e_maior else 1
        return 1 if a_e_maior else -1
    return 0


def merge_sort(times, criterio="pontos", decrescente=True, etapas=None, nivel=0):
    """Ordena a lista de times com Merge Sort e retorna uma NOVA lista.

    A lista recebida não é alterada. Se `etapas` for uma lista, cada divisão e
    intercalação é registrada nela (usado na demonstração da interface).
    """
    # Caso base: lista com 0 ou 1 elemento já está ordenada.
    if len(times) <= 1:
        return list(times)

    # 1) Dividir: separa a lista em duas metades.
    meio = len(times) // 2
    esquerda, direita = times[:meio], times[meio:]
    if etapas is not None:
        etapas.append((nivel, "Dividir", [esquerda, direita]))

    # 2) Conquistar: ordena cada metade recursivamente.
    esquerda = merge_sort(esquerda, criterio, decrescente, etapas, nivel + 1)
    direita = merge_sort(direita, criterio, decrescente, etapas, nivel + 1)

    # 3) Combinar: intercala as duas metades já ordenadas.
    resultado = intercalar(esquerda, direita, criterio, decrescente)
    if etapas is not None:
        etapas.append((nivel, "Intercalar", [esquerda, direita, resultado]))
    return resultado


def intercalar(esquerda, direita, criterio="pontos", decrescente=True):
    """Junta duas listas ordenadas em uma única lista ordenada."""
    resultado = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        # "<= 0" mantém a ordem original entre equivalentes (estabilidade).
        if comparar(esquerda[i], direita[j], criterio, decrescente) <= 0:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    # Uma das listas acabou: o restante da outra já está em ordem.
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado
