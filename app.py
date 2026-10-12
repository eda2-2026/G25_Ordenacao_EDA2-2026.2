"""Interface Streamlit do Simulador de Campeonato de Futebol."""

import streamlit as st

from algoritmos import CRITERIOS, DESEMPATES, merge_sort
from campeonato import Campeonato

ROTULOS = {atributo: rotulo for rotulo, atributo in CRITERIOS.items()}

st.set_page_config(page_title="Simulador de Campeonato de Futebol", page_icon="⚽")

# O Streamlit reexecuta o script a cada interação; o campeonato fica guardado
# em session_state para persistir em memória durante a sessão.
if "campeonato" not in st.session_state:
    st.session_state.campeonato = Campeonato.novo()
campeonato = st.session_state.campeonato
nomes = list(campeonato.times)

st.title("⚽ Simulador de Campeonato de Futebol")
st.caption("Projeto de EDA2 — classificação ordenada com Merge Sort implementado manualmente")

# ---------------------------------------------------------------- Partidas
st.header("Registrar partida")

# O formulário só dispara uma vez por clique no botão: recarregar a página ou
# mudar outros controles não processa a mesma partida novamente.
with st.form("registrar_partida", clear_on_submit=True):
    col1, col2 = st.columns(2)
    mandante = col1.selectbox("Time mandante", nomes, index=0)
    gols_mandante = col1.number_input("Gols do mandante", min_value=0, step=1, value=0)
    visitante = col2.selectbox("Time visitante", nomes, index=1)
    gols_visitante = col2.number_input("Gols do visitante", min_value=0, step=1, value=0)
    enviado = st.form_submit_button("Confirmar resultado", type="primary")

if enviado:
    try:
        partida = campeonato.registrar_partida(
            mandante, int(gols_mandante), visitante, int(gols_visitante)
        )
        st.success(f"Partida registrada: {partida.placar()}")
    except ValueError as erro:
        st.error(str(erro))

# ------------------------------------------------------------ Classificação
st.header("Classificação")

col1, col2 = st.columns(2)
rotulo_criterio = col1.selectbox("Ordenar classificação por", list(CRITERIOS))
criterio = CRITERIOS[rotulo_criterio]
if criterio == "nome":
    ordem = col2.radio("Ordem", ["A a Z", "Z a A"], horizontal=True)
    decrescente = ordem == "Z a A"
else:
    ordem = col2.radio(
        "Ordem", ["Decrescente (maior → menor)", "Crescente (menor → maior)"],
        horizontal=True,
    )
    decrescente = ordem.startswith("Decrescente")

if criterio == "nome":
    st.caption("Desempate: não se aplica (os nomes são únicos).")
else:
    desempates = [ROTULOS[c] for c in DESEMPATES if c != criterio] + ["Nome (A a Z)"]
    st.caption(
        f"Critério principal: **{rotulo_criterio}** — {ordem}. "
        f"Desempate: {' → '.join(desempates)} (maior → menor, exceto o nome)."
    )

classificacao = campeonato.classificacao(criterio, decrescente)
st.dataframe(
    [
        {
            "Pos.": posicao,
            "Time": t.nome,
            "Pontos": t.pontos,
            "Jogos": t.jogos,
            "Vitórias": t.vitorias,
            "Empates": t.empates,
            "Derrotas": t.derrotas,
            "Gols pró": t.gols_pro,
            "Gols contra": t.gols_contra,
            "Saldo": t.saldo_gols,
        }
        for posicao, t in enumerate(classificacao, start=1)
    ],
    hide_index=True,
    width="stretch",
)

# ------------------------------------------------------- Partidas jogadas
st.header("Partidas registradas")
if campeonato.partidas:
    st.dataframe(
        [
            {
                "Nº": p.numero,
                "Mandante": p.mandante,
                "Placar": f"{p.gols_mandante} x {p.gols_visitante}",
                "Visitante": p.visitante,
            }
            for p in reversed(campeonato.partidas)
        ],
        hide_index=True,
        width="stretch",
    )
else:
    st.info("Nenhuma partida registrada ainda.")

# ------------------------------------------------------ Demonstração didática
with st.expander("Como funciona o algoritmo"):
    st.markdown(
        """
**O que é o Merge Sort?**
É um algoritmo de ordenação do tipo *dividir para conquistar*. Ele quebra o
problema em partes menores, resolve cada parte e depois junta as soluções.

**1. Divisão** — a lista de times é cortada ao meio repetidamente até sobrarem
listas com um único time (uma lista de um elemento já está ordenada).

**2. Intercalação** — duas listas já ordenadas são unidas comparando sempre o
primeiro time de cada uma: o que deve vir antes é copiado para o resultado.
Quando uma das listas acaba, o restante da outra é copiado direto.

**3. Critérios escolhidos** — toda comparação é feita pela função `comparar`
(em `algoritmos.py`). Ela olha primeiro o critério principal selecionado acima
(na ordem crescente ou decrescente) e, se houver empate, passa para os
critérios de desempate. O Merge Sort em si não muda: só a regra de comparação.

**4. Complexidade O(n log n)** — a lista é dividida ao meio a cada nível,
então existem cerca de log₂ n níveis de recursão. Em cada nível, a intercalação
percorre os n elementos uma vez. Total: n × log n operações. Isso vale para o
melhor, médio e pior caso. A memória auxiliar é O(n), por causa das listas
temporárias criadas na intercalação.
"""
    )

    st.subheader("Exemplo com os times cadastrados")
    st.caption(
        f"Etapas para ordenar por **{rotulo_criterio}** — {ordem}, "
        "partindo da ordem de cadastro dos times."
    )

    def formatar(times):
        if criterio == "nome":
            return "[" + ", ".join(t.nome for t in times) + "]"
        valores = ", ".join(f"{t.nome} ({getattr(t, criterio)})" for t in times)
        return f"[{valores}]"

    etapas = []
    merge_sort(list(campeonato.times.values()), criterio, decrescente, etapas)
    linhas = []
    for nivel, tipo, listas in etapas:
        recuo = "    " * nivel
        if tipo == "Dividir":
            esquerda, direita = listas
            linhas.append(f"{recuo}Dividir:    {formatar(esquerda)} | {formatar(direita)}")
        else:
            esquerda, direita, resultado = listas
            linhas.append(
                f"{recuo}Intercalar: {formatar(esquerda)} + {formatar(direita)}"
                f"\n{recuo}         => {formatar(resultado)}"
            )
    st.code("\n".join(linhas), language=None)

# ------------------------------------------------------------- Reinício
st.header("Reiniciar campeonato")
confirmar = st.checkbox(
    "Confirmo que desejo apagar todas as partidas e estatísticas.",
    key="confirmar_reinicio",
)
if st.button("Reiniciar campeonato", disabled=not confirmar):
    st.session_state.campeonato = Campeonato.novo()
    del st.session_state["confirmar_reinicio"]
    st.rerun()
