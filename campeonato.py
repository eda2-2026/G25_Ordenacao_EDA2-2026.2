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


@dataclass
class Campeonato:
    times: dict = field(default_factory=dict)
    partidas: list = field(default_factory=list)

    @classmethod
    def novo(cls, nomes=None):
        """Cria um campeonato com os times informados, todos zerados."""
        nomes = TIMES_INICIAIS if nomes is None else nomes
        return cls(times={nome: Time(nome) for nome in nomes})

    def registrar_partida(self, mandante, gols_mandante, visitante, gols_visitante):
        """Valida, registra a partida e atualiza as estatísticas dos dois times.

        Lança ValueError se a partida for inválida (nesse caso nada é alterado).
        """
        self._validar(mandante, gols_mandante, visitante, gols_visitante)

        casa = self.times[mandante]
        fora = self.times[visitante]

        casa.gols_pro += gols_mandante
        casa.gols_contra += gols_visitante
        fora.gols_pro += gols_visitante
        fora.gols_contra += gols_mandante

        if gols_mandante > gols_visitante:
            casa.vitorias += 1
            fora.derrotas += 1
        elif gols_mandante < gols_visitante:
            fora.vitorias += 1
            casa.derrotas += 1
        else:
            casa.empates += 1
            fora.empates += 1

        partida = Partida(
            len(self.partidas) + 1, mandante, gols_mandante, visitante, gols_visitante
        )
        self.partidas.append(partida)
        return partida

    def _validar(self, mandante, gols_mandante, visitante, gols_visitante):
        for nome in (mandante, visitante):
            if nome not in self.times:
                raise ValueError(f"Time desconhecido: {nome}")
        if mandante == visitante:
            raise ValueError("Um time não pode jogar contra ele mesmo.")
        for gols in (gols_mandante, gols_visitante):
            # bool é subclasse de int em Python, então é excluído explicitamente.
            if not isinstance(gols, int) or isinstance(gols, bool):
                raise ValueError("Os gols devem ser números inteiros.")
            if gols < 0:
                raise ValueError("Os gols não podem ser negativos.")

    def classificacao(self, criterio="pontos", decrescente=True):
        """Retorna os times ordenados pelo Merge Sort implementado manualmente."""
        return merge_sort(list(self.times.values()), criterio, decrescente)
