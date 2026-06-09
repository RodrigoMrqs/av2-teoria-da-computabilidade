# Declaração de Uso de Inteligência Artificial

**Equipe:** João Pedro Silva da Silva · Rodrigo Marques Matos da Silva · Noagem Geraldo Ismael Coelho  
**Disciplina:** Teoria da Computabilidade — Prof. Daniel Leal Souza  
**Semestre:** 01/2026

---

## 1. Ferramentas Utilizadas

| Ferramenta | Período Aproximado de Uso |
|-----------|--------------------------|
| Claude (Anthropic) | Junho de 2026 |
| GitHub Copilot (autocomplete) | Ocasionalmente durante implementação |

---

## 2. Finalidade do Uso

| Atividade | Uso de IA? | Descrição |
|-----------|-----------|-----------|
| Estudo conceitual (NDTM, λ-Cálculo) | Parcial | Consultada para tirar dúvidas pontuais sobre formalização; a compreensão principal veio das referências bibliográficas |
| Implementação NDTM | Auxiliar | Estrutura inicial da classe NTM discutida; delta e lógica de estados definidos manualmente pela equipe |
| Implementação λ-Cálculo | Auxiliar | Parser e AST revisados com auxílio; regras de substituição e β-redução implementadas manualmente |
| Revisão textual do README | Sim | Revisão ortográfica e de formatação markdown |
| Organização dos slides | Sim | Sugestão de estrutura; conteúdo técnico preenchido pela equipe |
| Rastreamentos de execução | Não | Gerados pela execução real dos programas |

---

## 3. Resumo dos Prompts Utilizados e Trechos Aproveitados

### 3.1 Estudo Conceitual

**Prompt (paráfrase):** "Explique a diferença entre NDTM e DTM em termos de função de transição e critério de aceitação."

**Aproveitado:** A distinção entre δ determinístico e δ não-determinístico como função multivalorada; confirmou a compreensão da equipe sobre simulação por BFS.

**Modificado:** A explicação foi adaptada para o formalismo do livro DIVERIO & MENEZES usado na disciplina.

---

### 3.2 Implementação da NDTM

**Prompt (paráfrase):** "Como estruturar uma classe Python para simular uma NDTM usando BFS?"

**Aproveitado:** A ideia de usar `deque` para BFS e armazenar histórico por cópia no campo `history` da configuração.

**Modificado pela equipe:**
- A função de transição `delta_palindrome` foi totalmente projetada pelos integrantes
- Os estados e a lógica de não-determinismo para palíndromos (ramo par + ramo centro) foram criados pelos integrantes
- A condição de término e a marcação com X foram definidas pela equipe
- Os testes foram elaborados e verificados manualmente

**Rejeitado:** Sugestão inicial de usar recursão profunda para explorar ramos — substituída por BFS iterativo para evitar estouro de pilha.

---

### 3.3 Implementação do λ-Cálculo

**Prompt (paráfrase):** "Como implementar substituição captura-evitante em Python para λ-Cálculo?"

**Aproveitado:** A técnica de gerar variáveis frescas com contador global para evitar captura na substituição.

**Modificado pela equipe:**
- O parser recursivo-descendente foi analisado linha a linha pelos integrantes
- As funções `free_vars`, `bound_vars` e `alpha_equiv` foram revisadas e corrigidas
- Todos os exemplos de Church foram construídos e verificados manualmente
- A estratégia de ordem normal (leftmost-outermost) foi escolhida conscientemente pela equipe após estudo da teoria

**Rejeitado:** Sugestão de usar uma biblioteca de λ-Cálculo pronta (e.g. `lambda-calculus` PyPI) — substituída por implementação própria para satisfazer os requisitos da atividade.

---

## 4. O Que Foi Modificado, Corrigido ou Rejeitado

| Item | Ação |
|------|------|
| Estrutura BFS com recursão | **Rejeitada** — substituída por BFS iterativo |
| Biblioteca λ-Cálculo pronta | **Rejeitada** — implementação própria obrigatória |
| Definição dos estados NDTM gerada por IA | **Rejeitada** — estados projetados pela equipe |
| Exemplos de Church gerados por IA | **Revisados e verificados** — equipe confirmou cada passo manualmente |
| Texto do README | **Revisado** — formatação sugerida pela IA, conteúdo técnico pela equipe |

---

## 5. Declaração dos Integrantes

**Declaramos que:**

1. Todos os integrantes revisaram e compreendem os trechos gerados com auxílio de IA incorporados ao projeto.
2. A IA foi usada como ferramenta de apoio, não como substituta do estudo, da implementação ou da análise.
3. A lógica central de ambas as implementações (função de transição NDTM e regras de β-redução) foi desenvolvida e verificada manualmente pela equipe.
4. Todos os integrantes são capazes de explicar qualquer parte do código, dos rastreamentos e dos conceitos formais apresentados.
5. Nenhum trecho de código externo foi copiado sem compreensão e adaptação.

---

*João Pedro Silva da Silva*  
*Rodrigo Marques Matos da Silva*  
*Noagem Geraldo Ismael Coelho*  

**Data:** Junho de 2026
