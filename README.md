# Simulador de Campeonato de Futebol — EDA2

Projeto acadêmico da disciplina de Estruturas de Dados e Algoritmos 2. É um
simulador de campeonato com 8 times em que a tabela de classificação é ordenada
por um **Merge Sort implementado manualmente** em Python, com interface web em
Streamlit.

|Nome | Matrícula|
|--|--|
|Edson Pereira | 232025730| 
|Giovanni Ferreira| 232002664|

## Estrutura

| Arquivo | Conteúdo |
| --- | --- |
| `app.py` | Interface Streamlit |`
| `algoritmos.py` | Merge Sort, intercalação e função de comparação entre times |
| `campeonato.py` | Times, partidas, validação e atualização das estatísticas |

Os dados ficam só em memória (`st.session_state`): não há banco de dados nem
API externa.

## Instalação e execução

Requer Python 3.10 ou superior.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

O navegador abre em `http://localhost:8501`.

## Funcionalidades

- 8 times brasileiros pré-cadastrados, todos começando zerados.
- Registro de partidas (mandante, gols, visitante, gols) com validação: um time
  não pode jogar contra ele mesmo e os gols precisam ser inteiros não negativos.
- Atualização automática de jogos, vitórias, empates, derrotas, gols pró, gols
  contra, saldo e pontos (vitória = 3, empate = 1, derrota = 0).
- Cada partida é processada uma única vez: o registro acontece só no clique do
  botão do formulário, e recarregar ou mexer em outros controles não a duplica.
- Seletor "Ordenar classificação por": pontos, vitórias, empates, derrotas, gols
  pró, gols contra, saldo de gols ou nome do time.
- Ordem decrescente/crescente para critérios numéricos e A a Z / Z a A para o nome.
  A tabela muda na hora ao trocar o critério.
- Lista das partidas registradas.
- Botão de reinício do campeonato, que só fica habilitado após marcar a confirmação.
- Seção expansível "Como funciona o algoritmo", com a explicação do Merge Sort e
  as etapas reais de divisão e intercalação com os times cadastrados.

## Critérios de desempate

O critério escolhido é sempre o principal, na direção escolhida. Em caso de
empate, aplica-se a sequência abaixo, pulando o critério que já é o principal:

1. Maior número de pontos
2. Maior número de vitórias
3. Maior saldo de gols
4. Maior número de gols pró
5. Nome do time em ordem alfabética (sem diferenciar acentos e maiúsculas)

Exemplo: ordenando por **saldo de gols**, a ordem de comparação é saldo → pontos
→ vitórias → gols pró → nome. Os desempates são sempre do maior para o menor,
mesmo quando o critério principal está em ordem crescente. Ao ordenar por nome
não há desempate, porque os nomes são únicos.

## Como o Merge Sort foi aplicado

Toda a classificação passa por `Campeonato.classificacao()`, que chama
`merge_sort()` de `algoritmos.py`. Não há `sorted()` nem `.sort()` no código.

```text
merge_sort(lista):
    se a lista tem 0 ou 1 time -> já está ordenada
    dividir a lista ao meio
    ordenar recursivamente a metade esquerda
    ordenar recursivamente a metade direita
    intercalar as duas metades ordenadas
```

- **Divisão:** `times[:meio]` e `times[meio:]`, até restarem listas de 1 elemento.
- **Intercalação (`intercalar`):** compara o primeiro time de cada metade e copia
  para o resultado o que deve vir antes. Quando uma metade acaba, o restante da
  outra é copiado.
- **Comparação (`comparar`):** é aqui que entra o critério escolhido. A função
  percorre a sequência "critério principal + desempates" e retorna negativo se o
  time `a` vem antes, positivo se o `b` vem antes ou 0 se forem equivalentes.
  O Merge Sort é sempre o mesmo; apenas a regra de comparação muda.
- **Estabilidade:** ao usar `<= 0` na intercalação, elementos equivalentes
  mantêm a ordem original.
- **Sem efeitos colaterais:** `merge_sort` devolve uma lista nova e só lê os
  atributos dos times. A lista original e as estatísticas não são alteradas.

## Complexidade

- **Tempo: O(n log n)** no melhor, médio e pior caso. A lista é dividida ao meio
  a cada nível de recursão, o que gera cerca de log₂ n níveis, e em cada nível a
  intercalação percorre os n elementos uma vez. Cada comparação verifica no
  máximo 5 critérios, um custo constante.
- **Espaço: O(n)** de memória auxiliar, por causa das listas temporárias da
  intercalação, mais O(log n) da pilha de recursão.

Com 8 times, a ordenação faz 7 divisões e 7 intercalações, em 3 níveis (8 → 4 → 2 → 1).

## Exemplo de uso

1. Rode `streamlit run app.py`.
2. Em "Registrar partida", escolha **Flamengo 3 x 1 Palmeiras** e clique em
   "Confirmar resultado". O Flamengo vai ao topo com 3 pontos e saldo +2.
3. Registre **Grêmio 2 x 2 Internacional**: os dois recebem 1 ponto.
4. Em "Ordenar classificação por", escolha **Gols contra**: Palmeiras, Grêmio e
   Internacional aparecem primeiro. Troque para "Crescente" para ver o inverso.
5. Escolha **Nome do time** e alterne entre A a Z e Z a A.
6. Abra "Como funciona o algoritmo" para ver as etapas do Merge Sort com o
   critério selecionado.
7. Para recomeçar, marque a confirmação e clique em "Reiniciar campeonato".
