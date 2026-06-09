# AV2 — Teoria da Computabilidade
## Máquinas Universais, Turing e λ-Cálculo

**Equipe:** João Pedro Silva da Silva · Rodrigo Marques Matos da Silva · Noagem Geraldo Ismael Coelho  
**Modelos escolhidos:** 4 — NDTM · 7 — λ-Cálculo  
**Professor:** Daniel Leal Souza · Semestre 01/2026

---

## Slide 2 — Agenda

1. Modelo 4: Máquina de Turing Não Determinística
   - Definição formal e motivação
   - Problema: reconhecimento de palíndromos
   - Demonstração
2. Modelo 7: λ-Cálculo
   - Sintaxe, β-redução e Church-Turing
   - Numerais e booleanos de Church
   - Demonstração do avaliador
3. Análise comparativa e Hipótese de Church-Turing
4. Referências

---

## Slide 3 — NDTM: Motivação

**Máquina de Turing Determinística (DTM):**  
δ: Q × Γ → Q × Γ × {L, R, S}   ← um único destino

**Máquina de Turing Não Determinística (NDTM):**  
δ: Q × Γ → **𝒫**(Q × Γ × {L, R, S})  ← *conjunto* de destinos

**Por que estudar?**
- Simplifica a modelagem de problemas onde múltiplos caminhos devem ser explorados simultaneamente
- Árvore de computação em vez de sequência linear
- Critério de aceitação: existe **ao menos um** ramo aceitante
- Equivalente em poder computacional à DTM (simulação por BFS)

---

## Slide 4 — NDTM: Definição Formal

```
M = (Q, Σ, Γ, δ, q₀, q_acc, q_rej)
```

| Componente | Definição |
|-----------|-----------|
| Q | {q0, q_right_a, q_right_b, q_back_a, q_back_b, q_return, q_center_a, q_center_b, q_accept, q_reject} |
| Σ | {a, b} |
| Γ | {a, b, X, $, _} |
| δ | 41 entradas — 2 pares com grau ND = 2 |
| q₀ | q0 |
| q_acc | q_accept |
| q_rej | q_reject |

**Total: 10 estados, 41 transições, 2 pontos de não-determinismo**

---

## Slide 5 — NDTM: Problema — Palíndromos sobre {a,b}

**Linguagem reconhecida:**  
L_pal = { w ∈ {a,b}* | w = wᴿ }

**Exemplos aceitos:** ε, a, b, aa, aba, abba, aabaa  
**Exemplos rejeitados:** ab, ba, abb, abab

**Estratégia — Apagamento de fora para dentro:**
1. Marca o símbolo mais à esquerda não marcado com X
2. Varre até o fim da fita
3. Verifica se o símbolo mais à direita bate (mesmo símbolo)
4. Marca com X e reinicia no início

**Não-determinismo:** em q0, ao ler a ou b:
- **Ramo A** — trata como membro de um par externo
- **Ramo B** — *adivinha* que é o centro do palíndromo ímpar

---

## Slide 6 — NDTM: Árvore de Computação para "aba"

```
                    [q0, $Xba_]
                   /            \
           q_right_a           q_center_a
           [marca par]         [adivinha centro]
               |                      |
           q_back_a              q_center_a
           (verifica 'a'         (lê 'b' ≠ X/_)
            no fim)                  ❌ REJEITA
               |
           q_return → q0
               |
         [q0, $XXX_]
          /         \
    q_right_b    q_center_b
    (vai direita)  (adivinha centro 'b')
         |              |
    q_back_b      [lê X, vai R]
    (encontra X,        |
     sem par 'b')  [lê _, ACEITA] ✅
         ❌
```

**Resultado: ACEITA** — ramo ND que adivinhou o centro 'b' chega a q_accept.

---

## Slide 7 — NDTM: Tabela de Transição (seleção)

| Estado | Lê | → Novo Estado | Escreve | Move | Grau ND |
|--------|----|--------------|---------|------|---------|
| q0 | a | q_right_a **OU** q_center_a | X | R | **2** |
| q0 | b | q_right_b **OU** q_center_b | X | R | **2** |
| q0 | _ | q_accept | _ | S | 1 |
| q_right_a | _ | q_back_a | _ | L | 1 |
| q_back_a | a | q_return | X | L | 1 |
| q_back_a | b | q_reject | b | S | 1 |
| q_return | $ | q0 | $ | R | 1 |
| q_center_a | _ | q_accept | _ | S | 1 |
| q_center_a | b | q_reject | b | S | 1 |

Tabela completa: 41 entradas no arquivo `implementacoes/ndtm_palindromos.py`

---

## Slide 8 — NDTM: Demonstração ao Vivo

**Entradas de teste:**

| Entrada | Tipo | Esperado |
|---------|------|----------|
| `""` | aceita | ✅ ACEITA (0 passos) |
| `"a"` | aceita | ✅ ACEITA (4 passos) |
| `"aba"` | aceita (ímpar) | ✅ ACEITA (11 passos, 7 ramos) |
| `"abba"` | aceita (par) | ✅ ACEITA (16 passos, 6 ramos) |
| `"ab"` | rejeita | ✅ REJEITA (4 ramos rejeitados) |
| `"abab"` | rejeita | ✅ REJEITA (14 ramos rejeitados) |

**Execução:**
```bash
python implementacoes/ndtm_palindromos.py
```

---

## Slide 9 — λ-Cálculo: Motivação e Contexto

**Origem:** Alonzo Church, 1930s — formalismo para computação baseado em funções

**Três construções:**

| Construção | Notação | Significado |
|-----------|---------|-------------|
| Variável | x | Referência a nome |
| Abstração | λx.M | Função anônima com parâmetro x |
| Aplicação | M N | Aplica M ao argumento N |

**Única regra de computação — β-redução:**
```
(λx.M) N →β M[x := N]
```

**Relação com Turing:** λ-Cálculo é Turing-completo — Church e Turing demonstraram independentemente que seus formalismos são equivalentes (Hipótese de Church-Turing, 1936).

---

## Slide 10 — λ-Cálculo: Numerais e Booleanos de Church

**Numerais de Church:** n̄ = λf.λx.fⁿ(x)

```
ZERO  = λf.λx.x
ONE   = λf.λx.f x
TWO   = λf.λx.f(f x)
SUCC  = λn.λf.λx.f(n f x)
ADD   = λm.λn.λf.λx.m f (n f x)
MUL   = λm.λn.λf.m(n f)
```

**Booleanos de Church:**

```
TRUE  = λt.λf.t     FALSE = λt.λf.f
AND   = λp.λq.p q p
OR    = λp.λq.p p q
NOT   = λp.λa.λb.p b a
IF    = λp.λa.λb.p a b
```

Tudo é função. Não há tipos primitivos, números ou booleanos nativos — apenas λ-expressões.

---

## Slide 11 — λ-Cálculo: Exemplos de β-Redução

**ADD 1 1 → Church(2)** — 6 passos:

```
(λm.λn.λf.λx.m f (n f x)) (λf.λx.f x) (λf.λx.f x)
→ (λn.λf.λx.(λf.λx.f x) f (n f x)) (λf.λx.f x)
→ λf.λx.(λf.λx.f x) f ((λf.λx.f x) f x)
→ λf.λx.(λx.f x) ((λf.λx.f x) f x)
→ λf.λx.f ((λf.λx.f x) f x)
→ λf.λx.f ((λx.f x) x)
→ λf.λx.f (f x)        ← Church(2) ✅
```

**NOT TRUE → FALSE** — 3 passos:

```
(λp.λa.λb.p b a) (λt.λf.t)
→ λa.λb.(λt.λf.t) b a
→ λa.λb.(λf.b) a
→ λa.λb.b              ← α≡ FALSE ✅
```

---

## Slide 12 — λ-Cálculo: Demonstração ao Vivo

**Execução do avaliador:**
```bash
python implementacoes/lambda_calculus.py
```

**11 exemplos documentados** (> 7 exigidos):

| # | Expressão | Passos β | Resultado |
|---|-----------|----------|-----------|
| 1-3 | Combinadores I, K, S | 1, 2, 4 | corretos |
| 4-5 | SUCC 0, ADD 1 1 | 3, 6 | Church(1), Church(2) |
| 6-7 | AND/NOT com booleanos | 4, 3 | α≡ FALSE |
| 8 | MUL 2 2 | 5 | Church(4) |
| 9-10 | IF TRUE, OR FALSE | 2, 4 | corretos |
| 11 | Ω (divergência) | ∞ | detectado |

**Total: 34 β-reduções nos 10 exemplos com forma normal**

---

## Slide 13 — Análise: Hipótese de Church-Turing

| Propriedade | NDTM | λ-Cálculo |
|------------|------|-----------|
| **Poder computacional** | = DTM (toda NDTM → DTM equivalente) | = DTM (Church-Turing) |
| **Linguagem reconhecida** | Recursivamente enumerável | Funções computáveis |
| **Terminação** | Decidível para L_pal | Não garantida (Ω) |
| **Não-determinismo** | Explícito (δ multivalorada) | Confluência (Church-Rosser) |
| **Relação com LC** | Palíndromos = LLC ⊂ LSC | Expressividade de FP |

**Conclusão:** Ambos os formalismos são equivalentes em poder computacional e representam diferentes formas de expressar a mesma classe de algoritmos descritos pela Hipótese de Church-Turing.

---

## Slide 14 — Referências

1. DIVERIO, T. A.; MENEZES, P. B. *Teoria da Computação: Máquinas Universais e Computabilidade*. 3. ed. Porto Alegre: Bookman, 2011.

2. MENEZES, P. B. *Linguagens Formais e Autômatos*. 6. ed. Porto Alegre: Bookman, 2011.

3. SIPSER, M. *Introduction to the Theory of Computation*. 3. ed. Cengage Learning, 2013.

4. CHURCH, A. An unsolvable problem of elementary number theory. *American Journal of Mathematics*, v. 58, n. 2, p. 345–363, 1936.

5. TURING, A. M. On computable numbers, with an application to the Entscheidungsproblem. *Proceedings of the London Mathematical Society*, v. 42, n. 1, p. 230–265, 1937.

6. BARENDREGT, H. P. *The Lambda Calculus: Its Syntax and Semantics*. North-Holland, 1984.

7. Slides da disciplina Teoria da Computabilidade — Prof. Daniel Leal Souza, CESUPA, 2026.

---

## Slide 15 — Checklist Final

- [x] 2 máquinas/modelos distintos (Opções 4 e 7)
- [x] 2 implementações resolvendo problemas diferentes
- [x] NDTM: 10 estados (> 8), 41 transições (> 10)
- [x] λ-Cálculo: 11 exemplos com > 7 etapas de redução total documentadas
- [x] Rastreamentos com entradas aceitas, rejeitadas e de fronteira
- [x] README completo com instruções de execução
- [x] Repositório GitHub organizado
- [x] Declaração de uso de IA
- [x] Referências citadas

**Obrigado!**
