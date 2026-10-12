"""Cadastro dos times, registro de partidas e atualização das estatísticas."""

from dataclasses import dataclass, field

from algoritmos import merge_sort

TIMES_INICIAIS = [
    "Flamengo",
    "Palmeiras",
    "Corinthians",
    "São Paulo",
    "Grêmio",
    "Internacional",
    "Cruzeiro",
    "Fluminense",
]

PONTOS_VITORIA = 3
PONTOS_EMPATE = 1


@dataclass
class Time:
    nome: str
    vitorias: int = 0
    empates: int = 0
    derrotas: int = 0
    gols_pro: int = 0
    gols_contra: int = 0

    # Atributos derivados: calculados a partir dos demais, por isso nunca
    # ficam inconsistentes com as estatísticas armazenadas.
    @property
    def jogos(self):
        return self.vitorias + self.empates + self.derrotas

    @property
    def saldo_gols(self):
        return self.gols_pro - self.gols_contra

    @property
    def pontos(self):
        return PONTOS_VITORIA * self.vitorias + PONTOS_EMPATE * self.empates


@dataclass
class Partida:
    numero: int
    mandante: str
    gols_mandante: int
    visitante: str
    gols_visitante: int

    def placar(self):
        return (
            f"{self.mandante} {self.gols_mandante} x "
            f"{self.gols_visitante} {self.visitante}"
        )
