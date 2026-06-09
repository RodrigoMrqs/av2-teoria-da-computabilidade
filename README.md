# AV2 — Teoria da Computabilidade
## Máquinas Universais, Turing e λ-Cálculo

**Disciplina:** Teoria da Computabilidade  
**Professor:** Daniel Leal Souza  
**Semestre:** 01/2026 — CESUPA  

**Equipe:**
- João Pedro Silva da Silva
- Rodrigo Marques Matos da Silva
- Noam Geraldo Ismael Coelho

**Modelos escolhidos:**
- **Opção 4 — Máquina de Turing Não Determinística (NDTM)**
- **Opção 7 — λ-Cálculo**

---

## Problemas Resolvidos

| Modelo | Problema | Linguagem / Função |
|--------|---------|-------------------|
| NDTM (Opção 4) | Reconhecimento de palíndromos | L_pal = { w ∈ {a,b}* \| w = wᴿ } |
| λ-Cálculo (Opção 7) | Avaliador de expressões lambda com numerais e booleanos de Church | β-redução em ordem normal |

Os problemas são **distintos**: o primeiro é um problema de reconhecimento de linguagem (autômato + fita), o segundo é um problema de avaliação funcional (redução de termos).

---

## Estrutura do Repositório

```
av2-teoria-da-computabilidade/
├── README.md                          ← este arquivo
├── AV2_Computabilidade.ipynb          ← notebook Jupyter com código completo e outputs
├── implementacoes/
│   ├── ndtm_palindromos.py            ← NDTM standalone (Python 3, sem dependências externas)
│   └── lambda_calculus.py             ← λ-Cálculo standalone (Python 3, sem dependências externas)
├── testes/
│   ├── rastreamento_ndtm.md           ← rastreamentos detalhados de execução da NDTM
│   └── rastreamento_lambda.md         ← rastreamentos detalhados de execução do λ-Cálculo
├── slides/
│   └── slides.md                      ← slides em Markdown (15 slides)
└── uso_ia.md                          ← declaração de uso de inteligência artificial
```

---

## Dependências e Requisitos

### Scripts standalone (`implementacoes/`)
- **Python 3.8 ou superior**
- Sem dependências externas (apenas biblioteca padrão)

### Notebook Jupyter (`AV2_Computabilidade.ipynb`)
- Python 3.8+
- `jupyter` ou `jupyterlab`
- `matplotlib` (visualizações opcionais)
- `IPython`

Instalação das dependências do notebook:
```bash
pip install jupyter matplotlib ipython
```

---

## Como Executar

### Opção 1 — Scripts standalone (recomendada para reprodução rápida)

**NDTM — Reconhecedor de Palíndromos:**
```bash
python implementacoes/ndtm_palindromos.py
```

Saída esperada:
- Definição formal da máquina (Q, Σ, Γ, δ, q₀, q_acc, q_rej)
- Tabela completa de transições
- Tabela de testes com 15 entradas (aceitas e rejeitadas)
- Rastreamentos passo-a-passo das entradas aceitas
- Estatísticas dos ramos rejeitados

**λ-Cálculo — Avaliador de Expressões Lambda:**
```bash
python implementacoes/lambda_calculus.py
```

Saída esperada:
- Tabela de variáveis livres e ligadas
- Verificação de α-equivalência (6 pares)
- 11 exemplos de β-redução com todos os passos intermediários
- Tabela resumo com número de passos por exemplo

### Opção 2 — Notebook Jupyter (completo, com visualizações)

```bash
jupyter notebook AV2_Computabilidade.ipynb
```

ou

```bash
jupyter lab AV2_Computabilidade.ipynb
```

Execute as células em ordem. O notebook contém todas as implementações, definições formais, visualizações da árvore de computação NDTM e tabelas HTML.

---

## Exemplos de Entrada e Saída

### NDTM — Palíndromos

```
Entrada: 'aba'   → ACEITA  (ramos: 7, passos: 11)
Entrada: 'abba'  → ACEITA  (ramos: 6, passos: 16)
Entrada: 'ab'    → REJEITA (ramos: 4)
Entrada: 'abab'  → REJEITA (ramos: 14)
Entrada: ''      → ACEITA  (ramos: 1, passos: 0)
```

### λ-Cálculo — β-Redução

```
ADD 1 1:   (λm.λn.λf.λx.m f (n f x)) (λf.λx.f x) (λf.λx.f x)
           → ... (6 passos) ...
           → λf.λx.f (f x)   [Church(2)] ✅

NOT TRUE:  (λp.λa.λb.p b a) (λt.λf.t)
           → ... (3 passos) ...
           → λa.λb.b   [α-equiv FALSE] ✅

MUL 2 2:   → λf.λx.f(f(f(f x)))   [Church(4)] ✅
```

---

## Formalização dos Modelos

### NDTM

**7-tupla:** M = (Q, Σ, Γ, δ, q₀, q_acc, q_rej)

- **Q** = {q0, q_right_a, q_right_b, q_back_a, q_back_b, q_return, q_center_a, q_center_b, q_accept, q_reject} — **10 estados**
- **Σ** = {a, b}
- **Γ** = {a, b, X, $, _}
- **δ**: Q × Γ → 𝒫(Q × Γ × {L, R, S}) — **41 entradas, 2 com grau ND = 2**
- **Critério de aceitação:** existe ao menos um ramo que atinge q_accept
- **Simulação:** BFS sobre todos os ramos da árvore de computação

**Não-determinismo:** em (q0, 'a') e (q0, 'b'), dois ramos simultâneos:
- Ramo A: trata o símbolo como membro de um par externo
- Ramo B: *adivinha* que é o símbolo central (palíndromo ímpar)

### λ-Cálculo

**Gramática BNF:**
```
<term> ::= <var>
         | (λ <var> . <term>)    ← abstração
         | (<term> <term>)       ← aplicação (assoc. esquerda)
```

**Operações implementadas:**
- `free_vars(t)` — variáveis livres
- `bound_vars(t)` — variáveis ligadas
- `subst(t, var, repl)` — substituição captura-evitante
- `alpha_equiv(t1, t2)` — α-equivalência
- `beta_step(t)` — um passo de β-redução em ordem normal
- `reduce(t)` — redução à forma normal

**Estratégia:** Ordem normal (leftmost-outermost) — garante encontrar forma normal se ela existir (por confluência Church-Rosser).

---

## Testes e Rastreamentos

Os rastreamentos detalhados estão em:
- [`testes/rastreamento_ndtm.md`](testes/rastreamento_ndtm.md) — 5 casos aceitos + 5 rejeitados com tabelas passo-a-passo
- [`testes/rastreamento_lambda.md`](testes/rastreamento_lambda.md) — 11 exemplos de β-redução com todos os passos

Para gerar os rastreamentos ao vivo:
```bash
python implementacoes/ndtm_palindromos.py > testes/saida_ndtm.txt
python implementacoes/lambda_calculus.py  > testes/saida_lambda.txt
```

---

## Relação com a Hipótese de Church-Turing

| Propriedade | NDTM | λ-Cálculo |
|------------|------|-----------|
| Poder computacional | = DTM | = DTM (Church, 1936) |
| Linguagens/Funções | Recursivamente enumeráveis | Funções computáveis |
| Terminação | Decidível para L_pal | Não garantida (ex.: Ω) |
| Simulação | NDTM → DTM por BFS | β-redução normal termina se FN existe |

Ambos os formalismos capturam exatamente a mesma classe de algoritmos descritos pela **Hipótese de Church-Turing**.

---

## Referências

1. DIVERIO, T. A.; MENEZES, P. B. *Teoria da Computação: Máquinas Universais e Computabilidade*. 3. ed. Porto Alegre: Bookman, 2011.
2. MENEZES, P. B. *Linguagens Formais e Autômatos*. 6. ed. Porto Alegre: Bookman, 2011.
3. SIPSER, M. *Introduction to the Theory of Computation*. 3. ed. Cengage Learning, 2013.
4. CHURCH, A. An unsolvable problem of elementary number theory. *American Journal of Mathematics*, v. 58, n. 2, p. 345–363, 1936.
5. TURING, A. M. On computable numbers, with an application to the Entscheidungsproblem. *Proceedings of the London Mathematical Society*, v. 42, n. 1, p. 230–265, 1937.
6. BARENDREGT, H. P. *The Lambda Calculus: Its Syntax and Semantics*. North-Holland, 1984.
7. Slides da disciplina Teoria da Computabilidade — Prof. Daniel Leal Souza, CESUPA, 2026.

---

## Declaração de Uso de IA

Consulte o arquivo [`uso_ia.md`](uso_ia.md) para a declaração completa de uso de inteligência artificial.

Em resumo: a IA foi utilizada como auxílio ao estudo e revisão; toda a lógica de implementação, os estados da NDTM, a função de transição e os exemplos de λ-Cálculo foram desenvolvidos e verificados manualmente pela equipe.

---

## Checklist (conforme lauda AV2)

- [x] Turma, professor e todos os integrantes identificados
- [x] Exatamente 2 máquinas/modelos distintos (equipe de 3 integrantes)
- [x] 1 implementação bem elaborada para cada modelo (total: 2)
- [x] Cada implementação resolve um problema diferente
- [x] NDTM: 10 estados (> 8 exigidos), 41 transições (> 10 recomendadas)
- [x] λ-Cálculo: 11 exemplos com 34 passos β totais (> 7 exigidos)
- [x] Rastreamentos com entradas aceitas, rejeitadas e de fronteira
- [x] README com instruções de execução, dependências e exemplos
- [x] Pasta `implementacoes/` com código-fonte organizado
- [x] Pasta `testes/` com rastreamentos detalhados
- [x] Pasta `slides/` com slides em Markdown
- [x] Arquivo `uso_ia.md` com declaração de IA
- [x] Referências bibliográficas citadas
- [x] Implementações executáveis com `python <arquivo>.py`
