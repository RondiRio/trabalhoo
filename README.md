# Problema dos Recipientes de Água

Uma aplicação interativa com interface gráfica para resolução do clássico problema dos recipientes de água utilizando algoritmos de busca em Inteligência Artificial.


## Equipe de Desenvolvimento

| Nome | Matrícula |
|------|-----------|
| Luiz Carlos Souza | 06003531 |
| Nathan de Brito Oliveira | 06003437 |
| Thiago Dutra da Silva | 06003665 |
| Rondineli da Silva Oliveira Moreira | 06005959 |
| Eduardo de Cunto | 06004790 |

## Sobre o Projeto

O **Problema dos Recipientes de Água** é um quebra-cabeça clássico de IA onde o objetivo é obter uma quantidade específica de água usando dois recipientes de capacidades diferentes através de operações de encher, esvaziar e transferir água entre eles.

Este projeto implementa três algoritmos de busca diferentes para resolver o problema:
- **Busca em Largura (BFS)** - Busca não informada que explora todos os níveis
- **Busca Gulosa (Greedy)** - Busca informada que usa heurística
- **Busca A*** - Busca informada ótima que combina custo + heurística

## Características

### Interface Gráfica Moderna
- Design limpo e profissional;
- Layout intuitivo
- Visualização animada dos recipientes com nível de água
- Feedback visual imediato do estado do problema

### Funcionalidades
-Configuração personalizável dos parâmetros (capacidades, objetivo, estado inicial)
-Três algoritmos de busca para comparação
-Animação passo a passo da solução
-Indicador visual quando o objetivo é alcançado
-Validação de entradas e tratamento de erros

## Tecnologias Utilizadas

- **Python 3.8+** - Linguagem de programação
- **Tkinter** - Biblioteca para interface gráfica
- **Threading** - Para animações não bloqueantes
- **AIMA Python** - Implementação dos algoritmos de busca

## Requisitos

```bash
Python 3.8 ou superior
```

### Dependências

```python
tkinter 
threading
```

### Módulo de Busca

O projeto requer o módulo `search.py` com as implementações dos algoritmos:
- `Problem` (classe base)
- `breadth_first_graph_search()`
- `best_first_graph_search()`
- `astar_search()`

## Como Executar

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/recipientes-agua.git](https://github.com/RondiRio/trabalhoo.git)
cd recipientes-agua
```

2. **Certifique-se de ter o módulo search.py**
```
recipientes-agua/
├── trabalho.py
├── trabalho_com_interface.py
└── README.md


```
2.1 **Escolha como executar o projeto:**

    **Opção 1 - Via Terminal (trabalho.py)**
    - Mostra a sequência detalhada de passos de cada algoritmo
    - Permite executar os 3 algoritmos simultaneamente
    - Exibe análise comparativa dos resultados

    **Opção 2 - Interface Gráfica (trabalho_com_interface.py)**
    - Interface visual interativa
    - Animação do processo de solução
    - Execução individual de cada algoritmo


3. **Execute a aplicação**
```bash
python main.py
```

## Como Usar - trabalho.py

### 1. Configurar o Problema via Terminal

Ao executar `trabalho.py`, você verá um menu interativo. Digite:

1️⃣ **Para configurar o problema**
- Define capacidades máximas dos recipientes
- Define objetivo a ser alcançado
- Define estados iniciais dos recipientes

2️⃣ **Executar Busca em Largura (BFS)**
- Encontra a solução ótima explorando nível por nível

3️⃣ **Executar Busca Gulosa (Greedy)**
- Busca rápida usando heurística de distância ao objetivo

4️⃣ **Executar Busca A* (A Estrela)**
- Combina custo do caminho com heurística

5️⃣ **Comparar Algoritmos**
- Executa todas as buscas
- Compara tempo e número de passos
- Mostra análise comparativa

6️⃣ **Sair**
- Encerra o programa

> **Dica**: Configure o problema (opção 1) antes de executar qualquer busca

Clique em **"Configurar"** para aplicar as configurações.

### 2. Escolher um Algoritmo

Selecione um dos algoritmos de busca disponíveis:
- **Busca em Largura (BFS)** - Garante a solução mais curta
- **Busca Gulosa (Greedy)** - Rápida, mas não garante solução ótima
- **Busca A*** - Equilibra velocidade e otimalidade


## Como Usar - trabalho_com_interface.py

### 1. Configurar o Problema

Na seção **"Configuração do Problema"**, insira:
- **Capacidade Recipiente 1**: Capacidade máxima do primeiro recipiente (em litros)
- **Capacidade Recipiente 2**: Capacidade máxima do segundo recipiente (em litros)
- **Objetivo**: Quantidade de água desejada (em litros)
- **Inicial Recipiente 1**: Quantidade inicial de água no recipiente 1
- **Inicial Recipiente 2**: Quantidade inicial de água no recipiente 2

Clique em **"Configurar"** para aplicar as configurações.

### 2. Escolher um Algoritmo

Selecione um dos algoritmos de busca disponíveis:
- **Busca em Largura (BFS)** - Garante a solução mais curta
- **Busca Gulosa (Greedy)** - Rápida, mas não garante solução ótima
- **Busca A*** - Equilibra velocidade e otimalidade

### 3. Acompanhar a Solução

A aplicação irá:
- Animar visualmente cada passo da solução
- Mostrar a ação realizada em cada passo
- Registrar detalhes no log de execução
- Indicar quando o objetivo for alcançado

## Exemplo de Uso

**Problema Clássico (4L, 3L → 2L)**

1. Configure:
   - Capacidade 1: `4` litros
   - Capacidade 2: `3` litros
   - Objetivo: `2` litros
   - Ambos recipientes começam vazios: `0`, `0`

2. Execute qualquer algoritmo

3. Observe a solução (exemplo com BFS):
   - Passo 0: Estado inicial (0L, 0L)
   - Passo 1: Encher recipiente de 4L → (4L, 0L)
   - Passo 2: Transferir 4L para 3L → (1L, 3L)
   - Passo 3: Esvaziar recipiente de 3L → (1L, 0L)
   - Passo 4: Transferir 1L para 3L → (0L, 1L)
   - Passo 5: Encher recipiente de 4L → (4L, 1L)
   - Passo 6: Transferir 4L para 3L → (2L, 3L) 

## Algoritmos Implementados

### Busca em Largura (BFS)
- **Tipo**: Busca não informada
- **Completude**: Sim
- **Otimalidade**: Sim (menor número de passos)
- **Complexidade**: O(b^d)

### Busca Gulosa (Greedy)
- **Tipo**: Busca informada
- **Heurística**: Distância até o objetivo |objetivo - total_atual|
- **Completude**: Não
- **Otimalidade**: Não
- **Complexidade**: O(b^m)

### Busca A*
- **Tipo**: Busca informada
- **Função de Avaliação**: f(n) = g(n) + h(n)
- **Heurística**: Distância até o objetivo
- **Completude**: Sim
- **Otimalidade**: Sim (com heurística admissível)
- **Complexidade**: O(b^d)

## Design e UX

A interface foi desenvolvida seguindo princípios modernos de IHC:

### Princípios Aplicados
- **Visibilidade**: Todos os controles e informações estão claramente visíveis
- **Feedback**: Resposta imediata para todas as ações do usuário
- **Consistência**: Padrões visuais e comportamentais uniformes
- **Prevenção de erros**: Validação de entrada e desabilitação de botões durante execução
- **Reconhecimento**: Ícones e cores intuitivas para cada função
- **Flexibilidade**: Configuração completamente personalizável



## Resolução de Problemas

### A janela não abre
- Verifique se o Tkinter está instalado: `python -m tkinter`

### Erro "Module 'search' not found"
- Certifique-se de que o arquivo `search.py` está na mesma pasta

### Animação muito rápida/lenta
- Ajuste o valor em `time.sleep(1.2)` na função `_buscar()`

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Enviar pull requests




---

**Desenvolvido para a disciplina de Inteligência Artificial**
