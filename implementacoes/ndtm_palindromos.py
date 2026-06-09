"""
AV2 - Teoria da Computabilidade
Opção 4: Máquina de Turing Não Determinística (NDTM)
Problema: Reconhecimento de Palíndromos sobre {a, b}

Equipe: João Pedro Silva da Silva · Rodrigo Marques Matos da Silva · Noagem Geraldo Ismael Coelho
Semestre: 01/2026 — Prof. Daniel Leal Souza

Execução:
    python ndtm_palindromos.py

Dependências:
    Python 3.8+   (sem dependências externas)
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import copy
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Set
from enum import Enum


# ──────────────────────────────────────────────────────────────────────────────
# 1. Tipos e Estruturas de Dados
# ──────────────────────────────────────────────────────────────────────────────

class Direction(Enum):
    LEFT  = 'L'
    RIGHT = 'R'
    STAY  = 'S'


# Uma transição é (novo_estado, símbolo_a_escrever, direção)
Transition    = Tuple[str, str, Direction]
# O mapa de transição mapeia (estado, símbolo_lido) → lista de transições possíveis
TransitionMap = Dict[Tuple[str, str], List[Transition]]


@dataclass
class Configuration:
    """Representa uma configuração instantânea (ID) da NDTM."""
    state  : str
    tape   : List[str]
    head   : int
    step   : int = 0
    history: List['Configuration'] = field(default_factory=list, repr=False)

    def __hash__(self):
        return hash((self.state, tuple(self.tape), self.head))

    def __eq__(self, other):
        return (self.state == other.state
                and self.tape == other.tape
                and self.head == other.head)

    def tape_repr(self) -> str:
        """Formata a fita com colchetes indicando a posição da cabeça."""
        parts = [f"[{s}]" if i == self.head else f" {s} "
                 for i, s in enumerate(self.tape)]
        return "".join(parts).rstrip()

    def short_repr(self) -> str:
        return (f"Passo {self.step:>3} | "
                f"Estado: {self.state:<16} | "
                f"Cab:{self.head:>2} | "
                f"Fita: {self.tape_repr()}")


# ──────────────────────────────────────────────────────────────────────────────
# 2. Classe NDTM — Máquina de Turing Não Determinística
# ──────────────────────────────────────────────────────────────────────────────

class NTM:
    """
    NDTM = (Q, Σ, Γ, δ, q0, q_acc, q_rej)

    δ: Q × Γ → P(Q × Γ × {L, R, S})   (função de transição não determinística)

    Simulação por BFS sobre todos os ramos de computação.
    Aceitação: existe ao menos um ramo que atinge q_acc.
    """

    def __init__(self, states: Set[str], input_alpha: Set[str],
                 tape_alpha: Set[str], transitions: TransitionMap,
                 initial_state: str, accept_state: str,
                 reject_state: str, blank: str = '_'):
        self.Q     = states
        self.sigma = input_alpha
        self.gamma = tape_alpha
        self.delta = transitions
        self.q0    = initial_state
        self.q_acc = accept_state
        self.q_rej = reject_state
        self.blank = blank

    def _make_tape(self, w: str) -> List[str]:
        """Inicializa a fita com marcador de início '$' e brancos à direita."""
        return ['$'] + list(w) + [self.blank, self.blank]

    def _step(self, cfg: Configuration) -> List[Configuration]:
        """Expande um nó: retorna todos os sucessores não determinísticos."""
        symbol = cfg.tape[cfg.head] if cfg.head < len(cfg.tape) else self.blank
        key    = (cfg.state, symbol)
        if key not in self.delta:
            return []

        next_cfgs = []
        for (new_state, write, direction) in self.delta[key]:
            new_tape = copy.copy(cfg.tape)
            if cfg.head >= len(new_tape):
                new_tape.extend([self.blank] * (cfg.head - len(new_tape) + 2))
            new_tape[cfg.head] = write

            if direction == Direction.RIGHT:
                new_head = cfg.head + 1
                if new_head >= len(new_tape):
                    new_tape.append(self.blank)
            elif direction == Direction.LEFT:
                new_head = max(0, cfg.head - 1)
            else:
                new_head = cfg.head

            next_cfgs.append(Configuration(
                state   = new_state,
                tape    = new_tape,
                head    = new_head,
                step    = cfg.step + 1,
                history = cfg.history + [cfg],
            ))
        return next_cfgs

    def run(self, w: str, max_steps: int = 1000) -> Tuple[bool, List[Configuration], dict]:
        """
        Executa a NDTM sobre a entrada w usando BFS.
        Retorna (aceito, caminho_aceitante, estatísticas).
        """
        initial = Configuration(
            state   = self.q0,
            tape    = self._make_tape(w),
            head    = 1,
            step    = 0,
            history = [],
        )
        queue   = deque([initial])
        visited : Set[Configuration] = set()
        stats   = {
            'ramos_explorados' : 0,
            'profundidade_max' : 0,
            'total_transicoes' : 0,
            'ramos_rejeitados' : 0,
        }

        while queue:
            cfg = queue.popleft()
            if cfg in visited:
                continue
            visited.add(cfg)
            stats['ramos_explorados'] += 1
            stats['profundidade_max'] = max(stats['profundidade_max'], cfg.step)

            if cfg.state == self.q_acc:
                caminho = cfg.history + [cfg]
                stats['total_transicoes'] = len(caminho) - 1
                return True, caminho, stats

            if cfg.state == self.q_rej or cfg.step >= max_steps:
                stats['ramos_rejeitados'] += 1
                continue

            proximos = self._step(cfg)
            if not proximos:
                stats['ramos_rejeitados'] += 1
            else:
                for nc in proximos:
                    queue.append(nc)

        return False, [], stats

    def print_formal(self) -> None:
        sep = '─' * 64
        print(sep)
        print("  DEFINIÇÃO FORMAL DA NDTM")
        print(sep)
        print(f"  Q       = {sorted(self.Q)}")
        print(f"  Σ       = {sorted(self.sigma)}")
        print(f"  Γ       = {sorted(self.gamma)}")
        print(f"  q₀      = {self.q0}")
        print(f"  q_acc   = {self.q_acc}")
        print(f"  q_rej   = {self.q_rej}")
        print(f"  |δ|     = {len(self.delta)} entradas na função de transição")
        nd = [k for k, v in self.delta.items() if len(v) > 1]
        print(f"  ND pts  = {len(nd)} pares (estado,símbolo) com múltiplas transições")
        print(sep)

    def print_delta(self) -> None:
        print("\n  FUNÇÃO DE TRANSIÇÃO δ")
        print(f"  {'(Estado, Símbolo)':<28} → (novo_estado, escreve, move)  [grau ND]")
        print("  " + "─" * 70)
        for (state, sym), opts in sorted(self.delta.items()):
            opts_str = "  |  ".join(f"({ns}, '{ws}', {d.value})" for ns, ws, d in opts)
            print(f"  ({state}, '{sym}'){'':<{24 - len(state)}} → {opts_str}  [{len(opts)}]")
        print()


# ──────────────────────────────────────────────────────────────────────────────
# 3. Definição da NDTM para Palíndromos sobre {a, b}
#
# Linguagem: L_pal = { w ∈ {a,b}* | w = wᴿ }
#
# Estratégia: apagamento simétrico de fora para dentro + adivinhação do centro.
#   (1) Marca o símbolo mais à esquerda não marcado com 'X'.
#   (2) Varre até o final da fita.
#   (3) Verifica se o símbolo mais à direita é igual ao marcado.
#   (4) Marca com 'X' e retorna ao início para reiniciar.
#
# Não determinismo: em q0, ao ler 'a' ou 'b', dois ramos simultâneos:
#   Ramo A — trata o símbolo como membro de um par externo.
#   Ramo B — ADIVINHA que é o símbolo central (palíndromo de comprimento ímpar).
#
# Estados (10):
#   q0          – encontra próximo símbolo não marcado (início de cada ciclo)
#   q_right_a   – varre para a direita após marcar 'a' esquerdo
#   q_right_b   – varre para a direita após marcar 'b' esquerdo
#   q_back_a    – retorna para a esquerda verificando par 'a' direito
#   q_back_b    – retorna para a esquerda verificando par 'b' direito
#   q_return    – par verificado; volta ao início ('$')
#   q_center_a  – [ND] verifica se restam só X (centro 'a' adivinhado)
#   q_center_b  – [ND] verifica se restam só X (centro 'b' adivinhado)
#   q_accept    – estado de aceitação
#   q_reject    – estado de rejeição
# ──────────────────────────────────────────────────────────────────────────────

R = Direction.RIGHT
L = Direction.LEFT
S = Direction.STAY

delta_palindrome: TransitionMap = {
    # ── q0: início de cada ciclo ──────────────────────────────────────────────
    ('q0', '$'): [('q0',        '$', R)],
    ('q0', 'X'): [('q0',        'X', R)],
    ('q0', '_'): [('q_accept',  '_', S)],   # fita vazia (ou tudo marcado) → aceita
    ('q0', 'a'): [('q_right_a', 'X', R),    # ← NÃO DETERMINÍSTICO: ramo par
                  ('q_center_a','X', R)],   # ← NÃO DETERMINÍSTICO: ramo centro
    ('q0', 'b'): [('q_right_b', 'X', R),    # ← NÃO DETERMINÍSTICO: ramo par
                  ('q_center_b','X', R)],   # ← NÃO DETERMINÍSTICO: ramo centro

    # ── q_right_a: varre para a direita (marcou 'a' à esquerda) ──────────────
    ('q_right_a', 'a'): [('q_right_a', 'a', R)],
    ('q_right_a', 'b'): [('q_right_a', 'b', R)],
    ('q_right_a', 'X'): [('q_right_a', 'X', R)],
    ('q_right_a', '$'): [('q_right_a', '$', R)],
    ('q_right_a', '_'): [('q_back_a',  '_', L)],  # chegou ao fim

    # ── q_right_b: varre para a direita (marcou 'b' à esquerda) ──────────────
    ('q_right_b', 'a'): [('q_right_b', 'a', R)],
    ('q_right_b', 'b'): [('q_right_b', 'b', R)],
    ('q_right_b', 'X'): [('q_right_b', 'X', R)],
    ('q_right_b', '$'): [('q_right_b', '$', R)],
    ('q_right_b', '_'): [('q_back_b',  '_', L)],  # chegou ao fim

    # ── q_back_a: retorna verificando par direito de 'a' ─────────────────────
    ('q_back_a', 'a'): [('q_return', 'X', L)],    # par válido: 'a' = 'a'
    ('q_back_a', 'b'): [('q_reject', 'b', S)],    # par inválido: 'a' ≠ 'b'
    ('q_back_a', 'X'): [('q_back_a', 'X', L)],
    ('q_back_a', '_'): [('q_back_a', '_', L)],
    ('q_back_a', '$'): [('q_reject', '$', S)],

    # ── q_back_b: retorna verificando par direito de 'b' ─────────────────────
    ('q_back_b', 'b'): [('q_return', 'X', L)],    # par válido: 'b' = 'b'
    ('q_back_b', 'a'): [('q_reject', 'a', S)],    # par inválido: 'b' ≠ 'a'
    ('q_back_b', 'X'): [('q_back_b', 'X', L)],
    ('q_back_b', '_'): [('q_back_b', '_', L)],
    ('q_back_b', '$'): [('q_reject', '$', S)],

    # ── q_return: par verificado; volta até '$' para reiniciar ────────────────
    ('q_return', 'a'): [('q_return', 'a', L)],
    ('q_return', 'b'): [('q_return', 'b', L)],
    ('q_return', 'X'): [('q_return', 'X', L)],
    ('q_return', '_'): [('q_return', '_', L)],
    ('q_return', '$'): [('q0',       '$', R)],    # reinicia ciclo

    # ── q_center_a: [ND] verifica se restam apenas X (centro 'a') ────────────
    ('q_center_a', 'X'): [('q_center_a', 'X', R)],
    ('q_center_a', '_'): [('q_accept',   '_', S)],  # só X restam → aceita
    ('q_center_a', 'a'): [('q_reject',   'a', S)],  # sobrou símbolo → rejeita
    ('q_center_a', 'b'): [('q_reject',   'b', S)],
    ('q_center_a', '$'): [('q_center_a', '$', R)],

    # ── q_center_b: [ND] verifica se restam apenas X (centro 'b') ────────────
    ('q_center_b', 'X'): [('q_center_b', 'X', R)],
    ('q_center_b', '_'): [('q_accept',   '_', S)],
    ('q_center_b', 'a'): [('q_reject',   'a', S)],
    ('q_center_b', 'b'): [('q_reject',   'b', S)],
    ('q_center_b', '$'): [('q_center_b', '$', R)],
}


# ──────────────────────────────────────────────────────────────────────────────
# 4. Instanciação da Máquina
# ──────────────────────────────────────────────────────────────────────────────

ndtm_palindrome = NTM(
    states        = {'q0', 'q_right_a', 'q_right_b', 'q_back_a', 'q_back_b',
                     'q_return', 'q_center_a', 'q_center_b', 'q_accept', 'q_reject'},
    input_alpha   = {'a', 'b'},
    tape_alpha    = {'a', 'b', 'X', '$', '_'},
    transitions   = delta_palindrome,
    initial_state = 'q0',
    accept_state  = 'q_accept',
    reject_state  = 'q_reject',
)


# ──────────────────────────────────────────────────────────────────────────────
# 5. Funções de Saída / Rastreamento
# ──────────────────────────────────────────────────────────────────────────────

def print_trace(history: List[Configuration], accepted: bool, entrada: str) -> None:
    verdict = "ACEITA" if accepted else "REJEITADA"
    sep = "─" * 80
    print(f"\n{sep}")
    print(f"  Entrada: '{entrada}'  →  {verdict}")
    print(sep)
    for cfg in history:
        print(cfg.short_repr())
    print()


def run_tests() -> None:
    sep = "=" * 80
    print(sep)
    print("  TESTES — NDTM para Palíndromos sobre {a, b}")
    print(sep)

    aceitos    = ["", "a", "b", "aa", "bb", "aba", "bab", "abba", "aabaa", "ababa",
                  "aabbaa", "baab", "bbaabb"]
    rejeitados = ["ab", "ba", "abb", "baa", "abab", "abcd", "aab", "bba"]

    print(f"\n{'Entrada':<14} {'Esperado':<11} {'Obtido':<11} {'Ramos':<8} {'Passos':<8} Correto")
    print("─" * 65)

    corretos = 0
    total    = 0
    for w in aceitos + rejeitados:
        aceito, caminho, stats = ndtm_palindrome.run(w)
        esperado = "ACEITA"    if w in aceitos else "REJEITA"
        obtido   = "ACEITA"    if aceito       else "REJEITA"
        ps       = stats['total_transicoes'] if aceito else stats['profundidade_max']
        ok       = "OK" if esperado == obtido else "FALHOU"
        if esperado == obtido:
            corretos += 1
        total += 1
        print(f"  '{w}'{'':>{10-len(w)}} {esperado:<11} {obtido:<11} "
              f"{stats['ramos_explorados']:<8} {ps:<8} {ok}")

    print(f"\n  Resultado: {corretos}/{total} corretos")


def run_trace_examples() -> None:
    """Imprime rastreamentos detalhados para os casos de exemplo."""
    sep = "=" * 80
    print(f"\n{sep}")
    print("  RASTREAMENTOS DE EXECUÇÃO (CAMINHO ACEITANTE)")
    print(sep)

    for w in ["", "a", "aba", "abba", "aabaa"]:
        aceito, caminho, stats = ndtm_palindrome.run(w)
        print_trace(caminho, aceito, w)

    print(f"\n{sep}")
    print("  RASTREAMENTOS DE EXECUÇÃO (ENTRADAS REJEITADAS)")
    print(sep)

    for w in ["ab", "abb", "abab"]:
        aceito, caminho, stats = ndtm_palindrome.run(w)
        print(f"\n  Entrada: '{w}'  →  REJEITADA")
        print(f"  Ramos explorados: {stats['ramos_explorados']}  |  "
              f"Profundidade máxima: {stats['profundidade_max']}  |  "
              f"Ramos rejeitados: {stats['ramos_rejeitados']}")


# ──────────────────────────────────────────────────────────────────────────────
# 6. Ponto de Entrada
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    ndtm_palindrome.print_formal()
    print()
    ndtm_palindrome.print_delta()
    run_tests()
    run_trace_examples()
