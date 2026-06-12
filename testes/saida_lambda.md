# Saída: λ-Cálculo — Avaliador de Expressões

```

========================================================================
  VARIÁVEIS LIVRES E LIGADAS
========================================================================

  Expressão                    Livres             Ligadas             Descrição
  ────────────────────────────────────────────────────────────────────────────────
  x                            ['x']              []                  variável livre simples
  λx.x                         []                 ['x']               identidade — x é ligada
  λx.y                         ['y']              ['x']               corpo com var livre y
  λxy.x                        []                 ['x', 'y']          K — x,y ligadas
  λn.λf.λx.f(n f x)            []                 ['f', 'n', 'x']     SUCC — n,f,x ligadas
  (λx.x) y                     ['y']              ['x']               aplicação — x ligada, y livre

========================================================================
  VERIFICAÇÃO DE α-EQUIVALÊNCIA
========================================================================

  t1                 t2                 Esp      Res      OK   Descrição
  ────────────────────────────────────────────────────────────────────────────────
  λx.x               λy.y               True     True     OK  identidade renomeada
  λx.y               λz.y               True     True     OK  corpo com var livre igual
  λx.y               λx.z               False    False    OK  vars livres diferentes
  λx.λy.x            λa.λb.a            True     True     OK  K em α-equiv
  λf.f x             λg.g y             False    False    OK  var livre diferente no corpo
  λx.λy.x y          λa.λb.a b          True     True     OK  aplicação interna α-equiv

========================================================================
  EXEMPLOS DE β-REDUÇÃO — λ-CÁLCULO
========================================================================

────────────────────────────────────────────────────────────────────────
  Exemplo 1 — Combinador I (identidade): I z → z
  Entrada : (λx.x) z
────────────────────────────────────────────────────────────────────────
  Passo  0: (λx.x) z
  Passo  1: z
  → forma normal atingida após 1 β-redução(ões).


────────────────────────────────────────────────────────────────────────
  Exemplo 2 — Combinador K (projeção): K a b → a
  Entrada : (λxy.x) a b
────────────────────────────────────────────────────────────────────────
  Passo  0: (λxy.x) a b
  Passo  1: (λy.a) b
  Passo  2: a
  → forma normal atingida após 2 β-redução(ões).


────────────────────────────────────────────────────────────────────────
  Exemplo 3 — Combinador S: S I I z → z z
  Entrada : (λfgx.f x (g x)) (λx.x) (λx.x) z
────────────────────────────────────────────────────────────────────────
  Passo  0: (λfgx.f x (g x)) (λx.x) (λx.x) z
  Passo  1: (λgx.(λx.x) x (g x)) (λx.x) z
  Passo  2: (λx.(λx.x) x ((λx.x) x)) z
  Passo  3: (λx.x) z ((λx.x) z)
  Passo  4: z ((λx.x) z)
  Passo  5: z z
  → forma normal atingida após 5 β-redução(ões).


────────────────────────────────────────────────────────────────────────
  Exemplo 4 — SUCC 0 (sucessor do zero de Church)
  Entrada : (λnfx.f (n f x)) (λfx.x)
────────────────────────────────────────────────────────────────────────
  Passo  0: (λnfx.f (n f x)) (λfx.x)
  Passo  1: λfx.f ((λfx.x) f x)
  Passo  2: λfx.f ((λx.x) x)
  Passo  3: λfx.f x
  → forma normal atingida após 3 β-redução(ões).

  Verificação numérica: church_to_int = 1

────────────────────────────────────────────────────────────────────────
  Exemplo 5 — ADD 1 1 = 2 (adição de numerais de Church)
  Entrada : (λmnfx.m f (n f x)) (λfx.f x) (λfx.f x)
────────────────────────────────────────────────────────────────────────
  Passo  0: (λmnfx.m f (n f x)) (λfx.f x) (λfx.f x)
  Passo  1: (λnfx.(λfx.f x) f (n f x)) (λfx.f x)
  Passo  2: λfx.(λfx.f x) f ((λfx.f x) f x)
  Passo  3: λfx.(λx.f x) ((λfx.f x) f x)
  Passo  4: λfx.f ((λfx.f x) f x)
  Passo  5: λfx.f ((λx.f x) x)
  Passo  6: λfx.f (f x)
  → forma normal atingida após 6 β-redução(ões).

  Verificação numérica: church_to_int = 2

────────────────────────────────────────────────────────────────────────
  Exemplo 6 — AND TRUE FALSE (booleanos de Church)
  Entrada : (λpq.p q p) (λtf.t) (λtf.f)
────────────────────────────────────────────────────────────────────────
  Passo  0: (λpq.p q p) (λtf.t) (λtf.f)
  Passo  1: (λq.(λtf.t) q (λtf.t)) (λtf.f)
  Passo  2: (λtf.t) (λtf.f) (λtf.t)
  Passo  3: (λftf.f) (λtf.t)
  Passo  4: λtf.f
  → forma normal atingida após 4 β-redução(ões).

  α-equivalente a FALSE: True

────────────────────────────────────────────────────────────────────────
  Exemplo 7 — NOT TRUE (negação booleana de Church)
  Entrada : (λpab.p b a) (λtf.t)
────────────────────────────────────────────────────────────────────────
  Passo  0: (λpab.p b a) (λtf.t)
  Passo  1: λab.(λtf.t) b a
  Passo  2: λab.(λf.b) a
  Passo  3: λab.b
  → forma normal atingida após 3 β-redução(ões).

  α-equivalente a FALSE: True

────────────────────────────────────────────────────────────────────────
  Exemplo 8 — MUL 2 2 = 4 (multiplicação de Church)
  Entrada : (λmnf.m (n f)) (λfx.f (f x)) (λfx.f (f x))
────────────────────────────────────────────────────────────────────────
  Passo  0: (λmnf.m (n f)) (λfx.f (f x)) (λfx.f (f x))
  Passo  1: (λnf.(λfx.f (f x)) (n f)) (λfx.f (f x))
  Passo  2: λf.(λfx.f (f x)) ((λfx.f (f x)) f)
  Passo  3: λfx.(λfx.f (f x)) f ((λfx.f (f x)) f x)
  Passo  4: λfx.(λx.f (f x)) ((λfx.f (f x)) f x)
  Passo  5: λfx.f (f ((λfx.f (f x)) f x))
  Passo  6: λfx.f (f ((λx.f (f x)) x))
  Passo  7: λfx.f (f (f (f x)))
  → forma normal atingida após 7 β-redução(ões).

  Verificação numérica: church_to_int = 4

────────────────────────────────────────────────────────────────────────
  Exemplo 9 — IF TRUE x y → x (condicional de Church)
  Entrada : (λpab.p a b) (λtf.t) x y
────────────────────────────────────────────────────────────────────────
  Passo  0: (λpab.p a b) (λtf.t) x y
  Passo  1: (λab.(λtf.t) a b) x y
  Passo  2: (λb.(λtf.t) x b) y
  Passo  3: (λtf.t) x y
  Passo  4: (λf.x) y
  Passo  5: x
  → forma normal atingida após 5 β-redução(ões).


────────────────────────────────────────────────────────────────────────
  Exemplo 10 — OR FALSE TRUE (disjunção booleana de Church)
  Entrada : (λpq.p p q) (λtf.f) (λtf.t)
────────────────────────────────────────────────────────────────────────
  Passo  0: (λpq.p p q) (λtf.f) (λtf.t)
  Passo  1: (λq.(λtf.f) (λtf.f) q) (λtf.t)
  Passo  2: (λtf.f) (λtf.f) (λtf.t)
  Passo  3: (λf.f) (λtf.t)
  Passo  4: λtf.t
  → forma normal atingida após 4 β-redução(ões).

  α-equivalente a TRUE: True

────────────────────────────────────────────────────────────────────────
  Exemplo 11 — Ω (sem forma normal — divergência detectada)
  Entrada : (λx.x x) (λx.x x)
────────────────────────────────────────────────────────────────────────
  Passo  0: (λx.x x) (λx.x x)
  Passo  1: (λx.x x) (λx.x x)
  → loop detectado (sem forma normal).


========================================================================
  TABELA RESUMO — EXEMPLOS DE β-REDUÇÃO
========================================================================

  #   Termo (abreviado)                            Passos   Resultado
  ────────────────────────────────────────────────────────────────────────────────
  1   (λx.x) z                                     1        I z → z  [Identidade]
  2   (λx.λy.x) a b                                2        K a b → a  [Constante K]
  3   (λf.λg.λx.f x (g x)) (λx.x) (λx.x) z         5        S I I z → z z  [Combinador S]
  4   (λn.λf.λx.f(n f x)) (λf.λx.x)                3        SUCC 0 → Church(1)  [Sucessor]
  5   (λm.λn.λf.λx.m f (n f x)) (λf.λx.f x) (λf.…  6        ADD 1 1 → Church(2)  [Adição]
  6   (λp.λq.p q p) (λt.λf.t) (λt.λf.f)            4        AND TRUE FALSE → FALSE  [Conjunção]
  7   (λp.λa.λb.p b a) (λt.λf.t)                   3        NOT TRUE → FALSE  [Negação]
  8   (λm.λn.λf.m(n f)) (λf.λx.f(f x)) (λf.λx.f(…  7        MUL 2 2 → Church(4)  [Multiplicação]
  9   (λp.λa.λb.p a b) (λt.λf.t) x y               5        IF TRUE x y → x  [Condicional]
  10  (λp.λq.p p q) (λt.λf.f) (λt.λf.t)            4        OR FALSE TRUE → TRUE  [Disjunção]

  Ex.11  Ω = (λx.x x)(λx.x x)  →  diverge (sem forma normal)
```
