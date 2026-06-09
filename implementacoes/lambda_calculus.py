"""
AV2 — Teoria da Computabilidade
Opção 7: λ-Cálculo
Problema: Avaliador de λ-expressões com numerais e booleanos de Church

Equipe: João Pedro Silva da Silva · Rodrigo Marques Matos da Silva · Noam Geraldo Ismael Coelho
Semestre: 01/2026 — Prof. Daniel Leal Souza

Execução:
    python lambda_calculus.py

Dependências:
    Python 3.8+   (sem dependências externas)
"""

from __future__ import annotations
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from typing import Optional, Tuple, List


# ──────────────────────────────────────────────────────────────────────────────
# 1. AST — Representação de Termos Lambda
#
# Gramática (BNF):
#   <term> ::= <var>
#            | (λ <var> . <term>)    ← abstração
#            | (<term> <term>)       ← aplicação (associativa à esquerda)
# ──────────────────────────────────────────────────────────────────────────────

class LambdaTerm:
    """Nó base da AST para termos do λ-Cálculo."""
    pass


class Var(LambdaTerm):
    """Variável: referência a um nome."""
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'Var({self.name})'


class Abs(LambdaTerm):
    """Abstração lambda: λparam.body  (função anônima)."""
    def __init__(self, param: str, body: LambdaTerm) -> None:
        self.param = param
        self.body  = body

    def __repr__(self) -> str:
        return f'Abs({self.param}, {self.body!r})'


class App(LambdaTerm):
    """Aplicação: func arg  (aplicação de função a argumento)."""
    def __init__(self, func: LambdaTerm, arg: LambdaTerm) -> None:
        self.func = func
        self.arg  = arg

    def __repr__(self) -> str:
        return f'App({self.func!r}, {self.arg!r})'


# ──────────────────────────────────────────────────────────────────────────────
# 2. Parser — Converte string em AST
# ──────────────────────────────────────────────────────────────────────────────

class LambdaParser:
    """
    Parser recursivo-descendente para λ-expressões.
    Aceita tanto 'λ' quanto '\\' como símbolo de abstração.
    Suporta múltiplos parâmetros: λxy.M = λx.λy.M
    """

    def __init__(self, src: str) -> None:
        self.src = src
        self.pos = 0

    def _skip(self) -> None:
        while self.pos < len(self.src) and self.src[self.pos] in ' \t\n':
            self.pos += 1

    def _peek(self) -> Optional[str]:
        self._skip()
        return self.src[self.pos] if self.pos < len(self.src) else None

    def _eat(self) -> str:
        self._skip()
        ch = self.src[self.pos]
        self.pos += 1
        return ch

    def _expect(self, ch: str) -> None:
        got = self._eat()
        if got != ch:
            raise SyntaxError(f"Esperado '{ch}', obtido '{got}' na pos {self.pos}")

    def _name(self) -> str:
        self._skip()
        s = self.pos
        while self.pos < len(self.src) and (self.src[self.pos].isalnum() or self.src[self.pos] == "'"):
            self.pos += 1
        if self.pos == s:
            raise SyntaxError(f'Nome esperado na pos {self.pos}')
        return self.src[s:self.pos]

    def parse(self) -> LambdaTerm:
        t = self._term()
        self._skip()
        if self.pos < len(self.src):
            raise SyntaxError(f"Token inesperado: '{self.src[self.pos]}' na pos {self.pos}")
        return t

    def _term(self) -> LambdaTerm:
        self._skip()
        return self._abstraction() if self._peek() in ('λ', '\\') else self._application()

    def _abstraction(self) -> LambdaTerm:
        self._eat()  # consome 'λ' ou '\'
        # decide se parâmetros são multi-char (separados por espaço) ou single-char
        scan = self.pos
        while scan < len(self.src) and self.src[scan] != '.':
            scan += 1
        raw = self.src[self.pos:scan]
        params: List[str] = []
        if ' ' in raw or '\t' in raw:
            while self._peek() not in ('.', ')', None):
                params.append(self._name())
        else:
            while self._peek() not in ('.', ')', None):
                params.append(self.src[self.pos])
                self.pos += 1
        self._expect('.')
        body = self._term()
        for p in reversed(params):
            body = Abs(p, body)
        return body

    def _application(self) -> LambdaTerm:
        atoms: List[LambdaTerm] = []
        while True:
            a = self._atom()
            if a is None:
                break
            atoms.append(a)
        if not atoms:
            raise SyntaxError(f'Termo esperado na pos {self.pos}')
        result = atoms[0]
        for a in atoms[1:]:
            result = App(result, a)
        return result

    def _atom(self) -> Optional[LambdaTerm]:
        ch = self._peek()
        if ch is None or ch in (')', '.'):
            return None
        if ch == '(':
            self._eat()
            inner = self._term()
            self._expect(')')
            return inner
        if ch in ('λ', '\\'):
            return None
        if ch.isalpha():
            return Var(self._name())
        return None


def parse(src: str) -> LambdaTerm:
    """Converte uma string em um termo lambda (AST)."""
    return LambdaParser(src).parse()


# ──────────────────────────────────────────────────────────────────────────────
# 3. Operações sobre Termos: show, free_vars, bound_vars, subst, alpha_equiv
# ──────────────────────────────────────────────────────────────────────────────

def show(t: LambdaTerm, ctx: str = 'top') -> str:
    """Converte um termo lambda em string legível (notação padrão)."""
    if isinstance(t, Var):
        return t.name
    if isinstance(t, Abs):
        # Compacta λ-aninhados: λx.λy.M → λxy.M
        ps, b = [], t
        while isinstance(b, Abs):
            ps.append(b.param)
            b = b.body
        s = f"λ{''.join(ps)}.{show(b, 'top')}"
        return f'({s})' if ctx in ('arg', 'func') else s
    if isinstance(t, App):
        s = f"{show(t.func, 'func')} {show(t.arg, 'arg')}"
        return f'({s})' if ctx == 'arg' else s
    return '?'


def free_vars(t: LambdaTerm) -> set:
    """Retorna o conjunto de variáveis livres do termo."""
    if isinstance(t, Var):
        return {t.name}
    if isinstance(t, Abs):
        return free_vars(t.body) - {t.param}
    if isinstance(t, App):
        return free_vars(t.func) | free_vars(t.arg)
    return set()


def bound_vars(t: LambdaTerm) -> set:
    """Retorna o conjunto de variáveis ligadas do termo."""
    if isinstance(t, Var):
        return set()
    if isinstance(t, Abs):
        return {t.param} | bound_vars(t.body)
    if isinstance(t, App):
        return bound_vars(t.func) | bound_vars(t.arg)
    return set()


_fresh_counter = [0]


def fresh(base: str = 'v') -> str:
    """Gera um nome de variável fresco (para evitar captura na substituição)."""
    _fresh_counter[0] += 1
    return f"{base}'{_fresh_counter[0]}"


def subst(t: LambdaTerm, var: str, repl: LambdaTerm) -> LambdaTerm:
    """
    Substituição captura-evitante: t[var := repl]
    Renomeia variáveis ligadas quando necessário para evitar captura.
    """
    if isinstance(t, Var):
        return repl if t.name == var else t
    if isinstance(t, Abs):
        if t.param == var:
            return t   # parâmetro ligado oculta a variável livre
        if t.param in free_vars(repl):
            # renomeia para evitar captura
            new_param = fresh(t.param)
            new_body  = subst(t.body, t.param, Var(new_param))
            return Abs(new_param, subst(new_body, var, repl))
        return Abs(t.param, subst(t.body, var, repl))
    if isinstance(t, App):
        return App(subst(t.func, var, repl), subst(t.arg, var, repl))
    return t


def alpha_equiv(t1: LambdaTerm, t2: LambdaTerm, env: Optional[dict] = None) -> bool:
    """
    Verifica α-equivalência: dois termos são α-equivalentes se diferem apenas
    nos nomes das variáveis ligadas (λx.x =α λy.y).
    """
    if env is None:
        env = {}
    if isinstance(t1, Var) and isinstance(t2, Var):
        return env.get(t1.name, t1.name) == env.get(t2.name, t2.name)
    if isinstance(t1, Abs) and isinstance(t2, Abs):
        return alpha_equiv(t1.body, t2.body, {**env, t1.param: t1.param, t2.param: t1.param})
    if isinstance(t1, App) and isinstance(t2, App):
        return alpha_equiv(t1.func, t2.func, env) and alpha_equiv(t1.arg, t2.arg, env)
    return False


# ──────────────────────────────────────────────────────────────────────────────
# 4. Motor de β-Redução
#
# Estratégia: ordem normal (leftmost-outermost).
#   Garante encontrar a forma normal se ela existir (por confluência + normalização).
#
# Regra β: (λx.M) N →β M[x := N]
# ──────────────────────────────────────────────────────────────────────────────

def beta_step(t: LambdaTerm) -> Optional[LambdaTerm]:
    """
    Realiza um único passo de β-redução em ordem normal.
    Retorna None se o termo já está em forma normal.
    """
    if isinstance(t, App):
        if isinstance(t.func, Abs):                    # redex encontrado!
            return subst(t.func.body, t.func.param, t.arg)
        rf = beta_step(t.func)
        if rf is not None:
            return App(rf, t.arg)                      # reduz na posição da função
        ra = beta_step(t.arg)
        if ra is not None:
            return App(t.func, ra)                     # reduz na posição do argumento
    if isinstance(t, Abs):
        rb = beta_step(t.body)
        if rb is not None:
            return Abs(t.param, rb)                    # reduz sob abstração
    return None


def reduce(t: LambdaTerm, max_steps: int = 200) -> Tuple[LambdaTerm, List[str]]:
    """
    Reduz um termo à forma normal por passos de β-redução.
    Retorna (forma_normal_ou_ultimo, lista_de_representações_por_passo).
    """
    passos = [show(t)]
    for _ in range(max_steps):
        prox = beta_step(t)
        if prox is None:
            break
        t = prox
        s = show(t)
        if s == passos[-1]:
            break
        passos.append(s)
    return t, passos


def show_reduction(src: str, label: str = '', max_steps: int = 40) -> Tuple[LambdaTerm, int]:
    """
    Imprime toda a sequência de β-reduções de um termo.
    Retorna (forma_normal, número_de_passos).
    """
    t   = parse(src)
    sep = '─' * 72
    print(f'\n{sep}')
    if label:
        print(f'  {label}')
    print(f'  Entrada : {show(t)}')
    print(sep)

    atual  = t
    vistos = {show(t)}
    n      = 0
    print(f'  Passo {n:>2}: {show(atual)}')

    for _ in range(max_steps):
        prox = beta_step(atual)
        if prox is None:
            print(f'  → forma normal atingida após {n} β-redução(ões).')
            break
        atual = prox
        n    += 1
        s     = show(atual)
        print(f'  Passo {n:>2}: {s}')
        if s in vistos:
            print(f'  → loop detectado (sem forma normal).')
            break
        vistos.add(s)
    else:
        print(f'  → limite de {max_steps} passos atingido.')

    print()
    return atual, n


# ──────────────────────────────────────────────────────────────────────────────
# 5. Numerais e Combinadores de Church
#
# Numeral de Church:  n̄ = λf.λx.f^n(x)
#   ZERO  = λf.λx.x
#   ONE   = λf.λx.f x
#   TWO   = λf.λx.f(f x)
#   ...
#
# Aritmética:
#   SUCC  = λn.λf.λx.f(n f x)
#   ADD   = λm.λn.λf.λx.m f (n f x)
#   MUL   = λm.λn.λf.m(n f)
#   POW   = λb.λe.e b
#
# Booleanos de Church:
#   TRUE  = λt.λf.t    FALSE = λt.λf.f
#   AND   = λp.λq.p q p
#   OR    = λp.λq.p p q
#   NOT   = λp.λa.λb.p b a
#   IF    = λp.λa.λb.p a b
# ──────────────────────────────────────────────────────────────────────────────

ZERO  = parse("λf.λx.x")
ONE   = parse("λf.λx.f x")
TWO   = parse("λf.λx.f(f x)")
THREE = parse("λf.λx.f(f(f x))")
FOUR  = parse("λf.λx.f(f(f(f x)))")

SUCC  = parse("λn.λf.λx.f(n f x)")
ADD   = parse("λm.λn.λf.λx.m f (n f x)")
MUL   = parse("λm.λn.λf.m(n f)")
POW   = parse("λb.λe.e b")

TRUE  = parse("λt.λf.t")
FALSE = parse("λt.λf.f")
AND   = parse("λp.λq.p q p")
OR    = parse("λp.λq.p p q")
NOT   = parse("λp.λa.λb.p b a")
IF    = parse("λp.λa.λb.p a b")

PAIR  = parse("λa.λb.λf.f a b")
FST   = parse("λp.p(λa.λb.a)")
SND   = parse("λp.p(λa.λb.b)")


def church_to_int(numeral: LambdaTerm, max_steps: int = 500) -> Optional[int]:
    """
    Converte um numeral de Church reduzido para int Python.
    Conta o número de aplicações de 'f' na forma normal.
    """
    reduced, _ = reduce(numeral, max_steps)
    if not isinstance(reduced, Abs):
        return None
    f   = reduced.param
    b1  = reduced.body
    if not isinstance(b1, Abs):
        return None
    x    = b1.param
    body = b1.body
    count = 0
    t     = body
    while isinstance(t, App) and isinstance(t.func, Var) and t.func.name == f:
        count += 1
        t = t.arg
    return count if (isinstance(t, Var) and t.name == x) else None


# ──────────────────────────────────────────────────────────────────────────────
# 6. Exemplos de β-Redução (≥ 7 etapas relevantes)
# ──────────────────────────────────────────────────────────────────────────────

def run_examples() -> None:
    sep = "=" * 72
    print(f"\n{sep}")
    print("  EXEMPLOS DE β-REDUÇÃO — λ-CÁLCULO")
    print(sep)

    # Exemplo 1 — Combinador I: 1 passo
    show_reduction("(λx.x) z",
                   label="Exemplo 1 — Combinador I (identidade): I z → z")

    # Exemplo 2 — Combinador K: 2 passos
    show_reduction("(λx.λy.x) a b",
                   label="Exemplo 2 — Combinador K (projeção): K a b → a")

    # Exemplo 3 — Combinador S: 4 passos  S I I z = I z (I z) = z z
    show_reduction("(λf.λg.λx.f x (g x)) (λx.x) (λx.x) z",
                   label="Exemplo 3 — Combinador S: S I I z → z z")

    # Exemplo 4 — SUCC 0 → 1: 3 passos
    resultado, _ = show_reduction(
        "(λn.λf.λx.f(n f x)) (λf.λx.x)",
        label="Exemplo 4 — SUCC 0 (sucessor do zero de Church)")
    print(f"  Verificação numérica: church_to_int = {church_to_int(resultado)}")

    # Exemplo 5 — ADD 1 1 → 2: 6 passos
    resultado, _ = show_reduction(
        "(λm.λn.λf.λx.m f (n f x)) (λf.λx.f x) (λf.λx.f x)",
        label="Exemplo 5 — ADD 1 1 = 2 (adição de numerais de Church)")
    print(f"  Verificação numérica: church_to_int = {church_to_int(resultado)}")

    # Exemplo 6 — AND TRUE FALSE → FALSE: 4 passos
    resultado, _ = show_reduction(
        "(λp.λq.p q p) (λt.λf.t) (λt.λf.f)",
        label="Exemplo 6 — AND TRUE FALSE (booleanos de Church)")
    falso = parse("λt.λf.f")
    print(f"  α-equivalente a FALSE: {alpha_equiv(resultado, falso)}")

    # Exemplo 7 — NOT TRUE → FALSE: 3 passos
    resultado, _ = show_reduction(
        "(λp.λa.λb.p b a) (λt.λf.t)",
        label="Exemplo 7 — NOT TRUE (negação booleana de Church)")
    print(f"  α-equivalente a FALSE: {alpha_equiv(resultado, falso)}")

    # Exemplo 8 — MUL 2 2 → 4: 5 passos
    resultado, _ = show_reduction(
        "(λm.λn.λf.m(n f)) (λf.λx.f(f x)) (λf.λx.f(f x))",
        label="Exemplo 8 — MUL 2 2 = 4 (multiplicação de Church)")
    print(f"  Verificação numérica: church_to_int = {church_to_int(resultado)}")

    # Exemplo 9 — IF TRUE x y → x: 2 passos
    show_reduction(
        "(λp.λa.λb.p a b) (λt.λf.t) x y",
        label="Exemplo 9 — IF TRUE x y → x (condicional de Church)")

    # Exemplo 10 — OR FALSE TRUE → TRUE: 4 passos
    resultado, _ = show_reduction(
        "(λp.λq.p p q) (λt.λf.f) (λt.λf.t)",
        label="Exemplo 10 — OR FALSE TRUE (disjunção booleana de Church)")
    verdade = parse("λt.λf.t")
    print(f"  α-equivalente a TRUE: {alpha_equiv(resultado, verdade)}")

    # Exemplo 11 — Ω (sem forma normal)
    show_reduction("(λx.x x)(λx.x x)",
                   label="Exemplo 11 — Ω (sem forma normal — divergência detectada)",
                   max_steps=6)


def run_free_bound_tests() -> None:
    sep = "=" * 72
    print(f"\n{sep}")
    print("  VARIÁVEIS LIVRES E LIGADAS")
    print(sep)

    exemplos = [
        ("x",                 "variável livre simples"),
        ("λx.x",              "identidade — x é ligada"),
        ("λx.y",              "corpo com var livre y"),
        ("λxy.x",             "K — x,y ligadas"),
        ("λn.λf.λx.f(n f x)", "SUCC — n,f,x ligadas"),
        ("(λx.x) y",          "aplicação — x ligada, y livre"),
    ]

    print(f"\n  {'Expressão':<28} {'Livres':<18} {'Ligadas':<18}  Descrição")
    print("  " + "─" * 80)
    for src, desc in exemplos:
        t  = parse(src)
        fv = sorted(free_vars(t))
        bv = sorted(bound_vars(t))
        print(f"  {src:<28} {str(fv):<18} {str(bv):<18}  {desc}")


def run_alpha_equiv_tests() -> None:
    sep = "=" * 72
    print(f"\n{sep}")
    print("  VERIFICAÇÃO DE α-EQUIVALÊNCIA")
    print(sep)

    pares = [
        ("λx.x",    "λy.y",    True,  "identidade renomeada"),
        ("λx.y",    "λz.y",    True,  "corpo com var livre igual"),
        ("λx.y",    "λx.z",    False, "vars livres diferentes"),
        ("λx.λy.x", "λa.λb.a", True,  "K em α-equiv"),
        ("λf.f x",  "λg.g y",  False, "var livre diferente no corpo"),
        ("λx.λy.x y", "λa.λb.a b", True, "aplicação interna α-equiv"),
    ]

    print(f"\n  {'t1':<18} {'t2':<18} {'Esp':<8} {'Res':<8} OK   Descrição")
    print("  " + "─" * 80)
    for s1, s2, esp, desc in pares:
        res = alpha_equiv(parse(s1), parse(s2))
        ok  = "OK" if res == esp else "FALHOU"
        print(f"  {s1:<18} {s2:<18} {str(esp):<8} {str(res):<8} {ok}  {desc}")


def run_summary_table() -> None:
    sep = "=" * 72
    print(f"\n{sep}")
    print("  TABELA RESUMO — EXEMPLOS DE β-REDUÇÃO")
    print(sep)

    casos = [
        ("(λx.x) z",
         "I z → z",                           "Identidade"),
        ("(λx.λy.x) a b",
         "K a b → a",                         "Constante K"),
        ("(λf.λg.λx.f x (g x)) (λx.x) (λx.x) z",
         "S I I z → z z",                     "Combinador S"),
        ("(λn.λf.λx.f(n f x)) (λf.λx.x)",
         "SUCC 0 → Church(1)",                "Sucessor"),
        ("(λm.λn.λf.λx.m f (n f x)) (λf.λx.f x) (λf.λx.f x)",
         "ADD 1 1 → Church(2)",               "Adição"),
        ("(λp.λq.p q p) (λt.λf.t) (λt.λf.f)",
         "AND TRUE FALSE → FALSE",            "Conjunção"),
        ("(λp.λa.λb.p b a) (λt.λf.t)",
         "NOT TRUE → FALSE",                  "Negação"),
        ("(λm.λn.λf.m(n f)) (λf.λx.f(f x)) (λf.λx.f(f x))",
         "MUL 2 2 → Church(4)",               "Multiplicação"),
        ("(λp.λa.λb.p a b) (λt.λf.t) x y",
         "IF TRUE x y → x",                   "Condicional"),
        ("(λp.λq.p p q) (λt.λf.f) (λt.λf.t)",
         "OR FALSE TRUE → TRUE",              "Disjunção"),
    ]

    print(f"\n  {'#':<3} {'Termo (abreviado)':<44} {'Passos':<8} Resultado")
    print("  " + "─" * 80)
    for i, (src, resultado, desc) in enumerate(casos, 1):
        _, ps = reduce(parse(src), max_steps=100)
        n     = len(ps) - 1
        abrev = src[:42] + '…' if len(src) > 42 else src
        print(f"  {i:<3} {abrev:<44} {n:<8} {resultado}  [{desc}]")

    print()
    total, _ = reduce(parse("(λx.x x)(λx.x x)"), max_steps=10)
    print("  Ex.11  Ω = (λx.x x)(λx.x x)  →  diverge (sem forma normal)")


# ──────────────────────────────────────────────────────────────────────────────
# 7. Ponto de Entrada
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    run_free_bound_tests()
    run_alpha_equiv_tests()
    run_examples()
    run_summary_table()
