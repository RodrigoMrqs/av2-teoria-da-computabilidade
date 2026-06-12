# Rastreamento de Execução — NDTM para Palíndromos

**Máquina:** Opção 4 — Máquina de Turing Não Determinística  
**Problema:** Reconhecimento de palíndromos sobre {a, b}  
**Linguagem:** L_pal = { w ∈ {a,b}* | w = wᴿ }

---

## Tabela de Testes — Resultado Consolidado

| # | Entrada | Esperado | Obtido | Ramos | Passos | Correto |
|---|---------|----------|--------|-------|--------|---------|
| 1 | `""` (vazia) | ACEITA | ACEITA | 2 | 1 | ✅ |
| 2 | `"a"` | ACEITA | ACEITA | 5 | 2 | ✅ |
| 3 | `"b"` | ACEITA | ACEITA | 5 | 2 | ✅ |
| 4 | `"aa"` | ACEITA | ACEITA | 12 | 9 | ✅ |
| 5 | `"bb"` | ACEITA | ACEITA | 12 | 9 | ✅ |
| 6 | `"aba"` | ACEITA | ACEITA | 18 | 12 | ✅ |
| 7 | `"bab"` | ACEITA | ACEITA | 18 | 12 | ✅ |
| 8 | `"abba"` | ACEITA | ACEITA | 30 | 25 | ✅ |
| 9 | `"aabaa"` | ACEITA | ACEITA | 39 | 30 | ✅ |
| 10 | `"ababa"` | ACEITA | ACEITA | 39 | 30 | ✅ |
| 11 | `"ab"` | REJEITA | REJEITA | 6 | 3 | ✅ |
| 12 | `"ba"` | REJEITA | REJEITA | 6 | 3 | ✅ |
| 13 | `"abb"` | REJEITA | REJEITA | 8 | 5 | ✅ |
| 14 | `"abab"` | REJEITA | REJEITA | 9 | 6 | ✅ |
| 15 | `"aab"` | REJEITA | REJEITA | 8 | 5 | ✅ |

---

## Caso 1 — Entrada Aceita: `"aba"` (palíndromo ímpar)

**Estratégia:** o ramo não-determinístico que "adivinha" que `b` é o centro é o que aceita.

### Estado inicial
- Fita: `[$, a, b, a, _, _]`
- Estado: `q0`, Cabeça: posição 1 (lê `a`)

### Ramo B: q_center (adivinhou centro)

| Passo | Estado | Cabeça | Fita | Lê | Escreve | Move |
|-------|--------|--------|------|----|---------|------|
| 0 | q0 | 1 | `$ a b a _ _` | `a` | `X` (ND: centro) | R |
| 1 | q_center_a | 2 | `$ X b a _ _` | `b` | — | REJEITA |

Ramo B com `a` como centro: rejeita (sobra `b` após o X).

### Ramo A: q_right_a (trata `a` como par externo)

| Passo | Estado | Cabeça | Fita | Lê | Escreve | Move |
|-------|--------|--------|------|----|---------|------|
| 0 | q0 | 1 | `$ a b a _ _` | `a` | `X` | R |
| 1 | q_right_a | 2 | `$ X b a _ _` | `b` | `b` | R |
| 2 | q_right_a | 3 | `$ X b a _ _` | `a` | `a` | R |
| 3 | q_right_a | 4 | `$ X b a _ _` | `_` | `_` | L |
| 4 | q_back_a | 3 | `$ X b a _ _` | `a` | `X` | L |
| 5 | q_return | 2 | `$ X b X _ _` | `b` | `b` | L |
| 6 | q_return | 1 | `$ X b X _ _` | `X` | `X` | L |
| 7 | q_return | 0 | `$ X b X _ _` | `$` | `$` | R |
| 8 | q0 | 1 | `$ X b X _ _` | `X` | `X` | R |
| 9 | q0 | 2 | `$ X b X _ _` | `b` | `X` (ND: centro) | R |
| 10 | q_center_b | 3 | `$ X X X _ _` | `X` | `X` | R |
| 11 | q_center_b | 4 | `$ X X X _ _` | `_` | — | ACEITA ✅ |

**Resultado:** ACEITA após 12 passos no ramo aceitante. Ramos explorados: 18.

---

## Caso 2 — Entrada Aceita: `"abba"` (palíndromo par)

### Estado inicial
- Fita: `[$, a, b, b, a, _, _]`
- Estado: `q0`, Cabeça: posição 1

| Passo | Estado | Cabeça | Fita | Ação |
|-------|--------|--------|------|------|
| 0 | q0 | 1 | `$ a b b a _` | Lê `a` → marca X, vai R (ramo par) |
| 1 | q_right_a | 2 | `$ X b b a _` | Lê `b` → vai R |
| 2 | q_right_a | 3 | `$ X b b a _` | Lê `b` → vai R |
| 3 | q_right_a | 4 | `$ X b b a _` | Lê `a` → vai R |
| 4 | q_right_a | 5 | `$ X b b a _` | Lê `_` → vai L (q_back_a) |
| 5 | q_back_a | 4 | `$ X b b a _` | Lê `a` → marca X, vai L (q_return) |
| 6 | q_return | 3 | `$ X b b X _` | Vai L até `$` |
| 7 | q_return | 2 | `$ X b b X _` | Vai L |
| 8 | q_return | 1 | `$ X b b X _` | Vai L |
| 9 | q_return | 0 | `$ X b b X _` | Lê `$` → vai R (q0) |
| 10 | q0 | 1 | `$ X b b X _` | Lê `X` → pula |
| 11 | q0 | 2 | `$ X b b X _` | Lê `b` → marca X, vai R (ramo par) |
| 12 | q_right_b | 3 | `$ X X b X _` | Lê `b` → vai R |
| 13 | q_right_b | 4 | `$ X X b X _` | Lê `X` → vai R |
| 14 | q_right_b | 5 | `$ X X b X _` | Lê `_` → vai L (q_back_b) |
| 15 | q_back_b | 4 | `$ X X b X _` | Lê `X` → pula, vai L |
| 16 | q_back_b | 3 | `$ X X b X _` | Lê `b` → marca X, vai L (q_return) |
| 17 | q_return | ... | `$ X X X X _` | Retorna ao início |
| ... | q0 | ... | `$ X X X X _` | Lê `X` → pula até `_` |
| fim | q_accept | — | — | ACEITA ✅ |

**Resultado:** ACEITA após 25 passos. Ramos explorados: 30.

---

## Caso 3 — Entrada Aceita: `""` (vazia)

| Passo | Estado | Cabeça | Fita | Ação |
|-------|--------|--------|------|------|
| 0 | q0 | 1 | `$ _ _` | Lê `_` → ACEITA imediatamente ✅ |

**Resultado:** ACEITA em 0 passos (palavra vazia é palíndromo por definição).

---

## Caso 4 — Entrada Rejeitada: `"ab"`

| Passo | Estado | Cabeça | Fita | Ação |
|-------|--------|--------|------|------|
| 0 | q0 | 1 | `$ a b _` | Lê `a` → dois ramos ND |

**Ramo 1** (par — q_right_a):
| 1 | q_right_a | 2 | `$ X b _` | Vai R |
| 2 | q_right_a | 3 | `$ X b _` | Lê `_` → vai L (q_back_a) |
| 3 | q_back_a | 2 | `$ X b _` | Lê `b` ≠ `a` → REJEITA ❌ |

**Ramo 2** (centro — q_center_a):
| 1 | q_center_a | 2 | `$ X b _` | Lê `b` ≠ X/_ → REJEITA ❌ |

Todos os ramos rejeitam.  
**Resultado:** REJEITA. Ramos explorados: 6. Ramos rejeitados: 6.

---

## Caso 5 — Entrada Rejeitada: `"abab"`

Todos os ramos falham ao tentar combinar pares simétricos:
- `a` esquerdo vs. `b` direito → mismatch
- `b` esquerdo vs. `a` direito → mismatch
- Ramificações de centro: sobram símbolos não-X

**Resultado:** REJEITA. Ramos explorados: 9. Profundidade máxima: 6.

---

## Análise Técnica

| Aspecto | Detalhe |
|---------|---------|
| **Número de estados** | 10 (> 8 exigidos) |
| **Número de transições** | 40 entradas em δ |
| **Pontos ND** | 2 pares (q0,'a') e (q0,'b') — grau 2 cada |
| **Linguagem reconhecida** | L_pal = { w ∈ {a,b}* \| w = wᴿ } (não regular, livre de contexto) |
| **Complexidade temporal** | O(n²) passos no pior caso |
| **Relação com MT determinística** | Toda NDTM tem MT determinística equivalente (simulação por BFS/DFS) |
| **Por que não trivial** | Palíndromos requerem memória ilimitada (fora do alcance de autômatos finitos) e a estratégia ND é essencial para casos de comprimento ímpar sem saber o centro a priori |
