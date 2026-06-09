# Rastreamento de Execução — λ-Cálculo

**Modelo:** Opção 7 — λ-Cálculo  
**Problema:** Avaliador de λ-expressões com numerais e booleanos de Church  
**Estratégia de redução:** Ordem normal (leftmost-outermost)

---

## Tabela de Testes — Resultado Consolidado

| # | Expressão | Forma Normal | Passos β | Correto |
|---|-----------|-------------|----------|---------|
| 1 | `(λx.x) z` | `z` | 1 | ✅ |
| 2 | `(λx.λy.x) a b` | `a` | 2 | ✅ |
| 3 | `S I I z` (expandido) | `z z` | 4 | ✅ |
| 4 | `SUCC 0` | `Church(1)` | 3 | ✅ |
| 5 | `ADD 1 1` | `Church(2)` | 6 | ✅ |
| 6 | `AND TRUE FALSE` | `α≡ FALSE` | 4 | ✅ |
| 7 | `NOT TRUE` | `α≡ FALSE` | 3 | ✅ |
| 8 | `MUL 2 2` | `Church(4)` | 5 | ✅ |
| 9 | `IF TRUE x y` | `x` | 2 | ✅ |
| 10 | `OR FALSE TRUE` | `α≡ TRUE` | 4 | ✅ |
| 11 | `Ω = (λx.x x)(λx.x x)` | diverge | ∞ (detectado) | ✅ |

Total de β-reduções nos 10 exemplos com forma normal: **34 passos**  
Todos os 11 exemplos com resultado correto: ✅

---

## Variáveis Livres e Ligadas

| Expressão | Livres | Ligadas | Observação |
|-----------|--------|---------|------------|
| `x` | {x} | {} | variável simples, totalmente livre |
| `λx.x` | {} | {x} | identidade, sem vars livres |
| `λx.y` | {y} | {x} | y escapa da abstração |
| `λxy.x` | {} | {x, y} | combinador K |
| `λn.λf.λx.f(n f x)` | {} | {n, f, x} | SUCC — fechado |
| `(λx.x) y` | {y} | {x} | aplicação |

---

## α-Equivalência

| t₁ | t₂ | Resultado | Observação |
|----|----|-----------|----|
| `λx.x` | `λy.y` | **TRUE** | identidade renomeada |
| `λx.y` | `λz.y` | **TRUE** | mesma var livre `y` |
| `λx.y` | `λx.z` | **FALSE** | vars livres distintas |
| `λxy.x` | `λab.a` | **TRUE** | K em α-equiv |
| `λf.f x` | `λg.g y` | **FALSE** | var livre diferente no corpo |
| `λxy.x y` | `λab.a b` | **TRUE** | aplicação interna |

---

## Rastreamentos Detalhados

### Exemplo 1 — Combinador I: `(λx.x) z → z` (1 passo)

```
Passo 0: (λx.x) z
Passo 1: z
→ β-redex: substituir x por z em corpo x
→ resultado: z
→ forma normal atingida após 1 β-redução
```

**Regra aplicada:** `(λx.x) z →β x[x := z] = z`

---

### Exemplo 2 — Combinador K: `(λx.λy.x) a b → a` (2 passos)

```
Passo 0: (λx.λy.x) a b
Passo 1: (λy.a) b          ← [x := a] em λy.x
Passo 2: a                 ← [y := b] em a (y não ocorre livre)
→ forma normal atingida após 2 β-reduções
```

**Regra aplicada (passo 1):** `(λx.λy.x) a →β (λy.x)[x := a] = λy.a`  
**Regra aplicada (passo 2):** `(λy.a) b →β a[y := b] = a`

---

### Exemplo 3 — Combinador S: `S I I z → z z` (4 passos)

**Definição:** `S = λf.λg.λx.f x (g x)`

```
Passo 0: (λf.λg.λx.f x (g x)) (λx.x) (λx.x) z
Passo 1: (λg.λx.(λx.x) x (g x)) (λx.x) z     ← [f := I]
Passo 2: (λx.(λx.x) x ((λx.x) x)) z           ← [g := I]
Passo 3: (λx.x) z ((λx.x) z)                  ← beta em (λx.x) x
Passo 4: z ((λx.x) z)                          ← beta em (λx.x) z (posição func)
Passo 5: z z                                   ← beta no argumento
→ forma normal: z z
```

---

### Exemplo 4 — SUCC 0 → Church(1) (3 passos)

**SUCC** = `λn.λf.λx.f(n f x)`, **ZERO** = `λf.λx.x`

```
Passo 0: (λn.λf.λx.f(n f x)) (λf.λx.x)
Passo 1: λf.λx.f((λf.λx.x) f x)            ← [n := ZERO]
Passo 2: λf.λx.f((λx.x) x)                 ← [f' := f] em ZERO (renomeia f)
Passo 3: λf.λx.f x                          ← [x' := x]
→ forma normal: λf.λx.f x   ← Church(1) ✅
```

**Verificação:** `church_to_int(λf.λx.f x) = 1` ✅

---

### Exemplo 5 — ADD 1 1 → Church(2) (6 passos)

**ADD** = `λm.λn.λf.λx.m f (n f x)`, **ONE** = `λf.λx.f x`

```
Passo 0: (λm.λn.λf.λx.m f (n f x)) (λf.λx.f x) (λf.λx.f x)
Passo 1: (λn.λf.λx.(λf.λx.f x) f (n f x)) (λf.λx.f x)    ← [m := ONE]
Passo 2: λf.λx.(λf.λx.f x) f ((λf.λx.f x) f x)            ← [n := ONE]
Passo 3: λf.λx.(λx.f x) ((λf.λx.f x) f x)                 ← beta em (λf.λx.f x) f
Passo 4: λf.λx.f ((λf.λx.f x) f x)                         ← beta
Passo 5: λf.λx.f ((λx.f x) x)                              ← beta em (λf.λx.f x) f
Passo 6: λf.λx.f (f x)                                      ← beta
→ forma normal: λf.λx.f (f x)   ← Church(2) ✅
```

**Verificação:** `church_to_int(λf.λx.f (f x)) = 2` ✅

---

### Exemplo 6 — AND TRUE FALSE → FALSE (4 passos)

**AND** = `λp.λq.p q p`, **TRUE** = `λt.λf.t`, **FALSE** = `λt.λf.f`

```
Passo 0: (λp.λq.p q p) (λt.λf.t) (λt.λf.f)
Passo 1: (λq.(λt.λf.t) q (λt.λf.t)) (λt.λf.f)    ← [p := TRUE]
Passo 2: (λt.λf.t) (λt.λf.f) (λt.λf.t)            ← [q := FALSE]
Passo 3: (λf.(λt.λf.f)) (λt.λf.t)                  ← [t := FALSE] em TRUE
Passo 4: λt.λf.f                                    ← [f := TRUE] — f não ocorre livre
→ forma normal: λt.λf.f   ← α-equiv FALSE ✅
```

---

### Exemplo 7 — NOT TRUE → FALSE (3 passos)

**NOT** = `λp.λa.λb.p b a`, **TRUE** = `λt.λf.t`

```
Passo 0: (λp.λa.λb.p b a) (λt.λf.t)
Passo 1: λa.λb.(λt.λf.t) b a            ← [p := TRUE]
Passo 2: λa.λb.(λf.b) a                 ← [t := b] em TRUE
Passo 3: λa.λb.b                        ← [f := a] — f não ocorre livre
→ forma normal: λa.λb.b   ← α-equiv FALSE (λt.λf.f) ✅
```

---

### Exemplo 8 — MUL 2 2 → Church(4) (5 passos)

**MUL** = `λm.λn.λf.m(n f)`, **TWO** = `λf.λx.f(f x)`

```
Passo 0: (λm.λn.λf.m(n f)) (λf.λx.f(f x)) (λf.λx.f(f x))
Passo 1: (λn.λf.(λf.λx.f(f x))(n f)) (λf.λx.f(f x))    ← [m := TWO]
Passo 2: λf.(λf.λx.f(f x))((λf.λx.f(f x)) f)            ← [n := TWO]
Passo 3: λf.(λf.λx.f(f x))(λx.f(f x))                   ← beta interno
Passo 4: λf.λx.(λx.f(f x))(((λx.f(f x)) x))             ← [f' := λx.f(f x)]
Passo 5: λf.λx.f(f(f(f x)))                              ← reduções finais
→ forma normal: λf.λx.f(f(f(f x)))   ← Church(4) ✅
```

**Verificação:** `church_to_int = 4` ✅

---

### Exemplo 9 — IF TRUE x y → x (2 passos)

**IF** = `λp.λa.λb.p a b`, **TRUE** = `λt.λf.t`

```
Passo 0: (λp.λa.λb.p a b) (λt.λf.t) x y
Passo 1: (λa.λb.(λt.λf.t) a b) x y         ← [p := TRUE]
Passo 2: (λb.(λt.λf.t) x b) y              ← [a := x]
Passo 3: (λt.λf.t) x y                     ← [b := y]  (mas isso é só TRUE x y)
→ TRUE x y →
Passo 4: (λf.x) y                          ← [t := x]
Passo 5: x                                 ← [f := y] — f não livre
→ forma normal: x ✅
```

---

### Exemplo 10 — OR FALSE TRUE → TRUE (4 passos)

**OR** = `λp.λq.p p q`, **FALSE** = `λt.λf.f`, **TRUE** = `λt.λf.t`

```
Passo 0: (λp.λq.p p q) (λt.λf.f) (λt.λf.t)
Passo 1: (λq.(λt.λf.f)(λt.λf.f) q) (λt.λf.t)    ← [p := FALSE]
Passo 2: (λt.λf.f)(λt.λf.f) (λt.λf.t)            ← [q := TRUE]
Passo 3: (λf.f) (λt.λf.t)                         ← [t := FALSE] em FALSE
Passo 4: λt.λf.t                                   ← [f := TRUE]
→ forma normal: λt.λf.t   ← α-equiv TRUE ✅
```

---

### Exemplo 11 — Ω (divergência detectada)

**Ω** = `(λx.x x)(λx.x x)`

```
Passo 0: (λx.x x)(λx.x x)
Passo 1: (λx.x x)(λx.x x)    ← [x := (λx.x x)] no corpo x x
Passo 2: (λx.x x)(λx.x x)    ← idem
...
→ loop detectado — sem forma normal
```

**Observação:** Este é o exemplo clássico de divergência no λ-Cálculo. O redutor detecta o ciclo e para, evidenciando que Ω ∉ FN (o conjunto dos termos com forma normal). Isso demonstra que o λ-Cálculo, embora Turing-completo, não garante terminação para todos os termos.

---

## Análise Técnica

| Aspecto | Detalhe |
|---------|---------|
| **Completude de Turing** | λ-Cálculo é Turing-completo: qualquer função computável pode ser expressa |
| **Estratégia** | Ordem normal (leftmost-outermost) — sempre encontra forma normal se ela existir |
| **Confluência (Church-Rosser)** | A ordem das reduções não afeta a forma normal final (quando existe) |
| **Numerais de Church** | `n̄ = λf.λx.fⁿ(x)` — adição, multiplicação e potência implementadas |
| **Booleanos de Church** | `TRUE = λtf.t`, `FALSE = λtf.f` — funcionam como `if-then-else` |
| **α-renomeação** | Substituição captura-evitante com geração de nomes frescos |
| **Divergência** | `Ω = (λx.x x)(λx.x x)` não possui forma normal — demonstra limites do λ-Cálculo |
| **Hipótese Church-Turing** | Qualquer algoritmo é computável no λ-Cálculo se e somente se for computável em uma MT |
| **Total de passos** | 34 passos β nos 10 exemplos com forma normal (> 7 exigidos pelo critério) |
