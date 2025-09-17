from search import Problem, breadth_first_graph_search, best_first_graph_search, astar_search
import os

class RecipientesAgua(Problem):
    """Problema dos recipientes de água configurável"""
    
    def __init__(self, cap1, cap2, objetivo, inicial1=0, inicial2=0):
        self.cap1 = cap1
        self.cap2 = cap2
        self.objetivo = objetivo
        super().__init__((inicial1, inicial2))
    
    def actions(self, state):
        """Ações possíveis: encher, esvaziar, transferir"""
        x, y = state
        acoes = []
        
        # Encher recipientes
        if x < self.cap1: acoes.append(f'encher_{self.cap1}L')
        if y < self.cap2: acoes.append(f'encher_{self.cap2}L')
        
        # Esvaziar recipientes
        if x > 0: acoes.append(f'esvaziar_{self.cap1}L')
        if y > 0: acoes.append(f'esvaziar_{self.cap2}L')
        
        # Transferir entre recipientes
        if x > 0 and y < self.cap2: acoes.append(f'{self.cap1}L_para_{self.cap2}L')
        if y > 0 and x < self.cap1: acoes.append(f'{self.cap2}L_para_{self.cap1}L')
        
        return acoes
    
    def result(self, state, action):
        """Retorna novo estado após ação"""
        x, y = state
        
        if action == f'encher_{self.cap1}L':
            return (self.cap1, y)
        elif action == f'encher_{self.cap2}L':
            return (x, self.cap2)
        elif action == f'esvaziar_{self.cap1}L':
            return (0, y)
        elif action == f'esvaziar_{self.cap2}L':
            return (x, 0)
        elif action == f'{self.cap1}L_para_{self.cap2}L':
            transfer = min(x, self.cap2 - y)
            return (x - transfer, y + transfer)
        elif action == f'{self.cap2}L_para_{self.cap1}L':
            transfer = min(y, self.cap1 - x)
            return (x + transfer, y - transfer)
    
    def goal_test(self, state):
        """Verifica se atingiu objetivo"""
        return sum(state) == self.objetivo
    
    def h(self, node):
        """Heurística: distância até objetivo"""
        return abs(self.objetivo - sum(node.state))

def imprimir_solucao(node, nome_busca, problema):
    """Imprime os passos da solução"""
    if not node:
        print(f"{nome_busca}: Nenhuma solução encontrada")
        return
    
    caminho = node.path()
    print(f"\n{nome_busca} - Solução encontrada em {len(caminho)-1} passos:")
    
    for i, no in enumerate(caminho):
        x, y = no.state
        if i == 0:
            print(f"Passo {i}: Estado inicial - {problema.cap1}L={x}L, {problema.cap2}L={y}L, Total={x+y}L")
        else:
            print(f"Passo {i}: Ação '{no.action}' - {problema.cap1}L={x}L, {problema.cap2}L={y}L, Total={x+y}L")

def configurar_problema():
    """Configura os parâmetros do problema"""
    print("\n" + "="*40)
    print("CONFIGURAÇÃO DO PROBLEMA")
    print("="*40)
    
    cap1 = int(input("Capacidade do recipiente 1 (L): "))
    cap2 = int(input("Capacidade do recipiente 2 (L): "))
    objetivo = int(input("Objetivo (litros desejados): "))
    
    print("\nEstado inicial dos recipientes:")
    inicial1 = int(input(f"Recipiente 1 ({cap1}L) - quantidade inicial: "))
    inicial2 = int(input(f"Recipiente 2 ({cap2}L) - quantidade inicial: "))
    
    return RecipientesAgua(cap1, cap2, objetivo, inicial1, inicial2)

def menu():
    """Menu principal para escolher tipo de busca"""
    problema = None
    
    while True:
        if problema:
            print("\n" + "="*50)
            print(f"PROBLEMA DOS RECIPIENTES ({problema.cap1}L, {problema.cap2}L)")
            print(f"Objetivo: Obter {problema.objetivo} litros")
            print(f"Estado inicial: {problema.initial}")
        else:
            print("\n" + "="*50)
            print("PROBLEMA DOS RECIPIENTES DE ÁGUA")
        print("="*50)
        print("1. Configurar problema")
        print("2. Busca em Largura (BFS)")
        print("3. Busca Gulosa (Greedy)")
        print("4. Busca A*")
        print("5. Comparar todas as buscas")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        
        if opcao == '1':
            problema = configurar_problema()
            print("Problema configurado com sucesso!")
            
        elif opcao in ['2', '3', '4', '5'] and not problema:
            print("Configure o problema primeiro (opção 1)!")
            
        elif opcao == '2':
            resultado = breadth_first_graph_search(problema)
            imprimir_solucao(resultado, "BUSCA EM LARGURA", problema)
            
        elif opcao == '3':
            resultado = best_first_graph_search(problema, lambda n: problema.h(n))
            imprimir_solucao(resultado, "BUSCA GULOSA", problema)
            
        elif opcao == '4':
            resultado = astar_search(problema, lambda n: problema.h(n))
            imprimir_solucao(resultado, "BUSCA A*", problema)
            
        elif opcao == '5':
            print("\n" + "="*60)
            print("COMPARAÇÃO DE TODAS AS BUSCAS")
            print("="*60)
            
            resultado_bfs = breadth_first_graph_search(problema)
            imprimir_solucao(resultado_bfs, "BUSCA EM LARGURA", problema)
            
            resultado_greedy = best_first_graph_search(problema, lambda n: problema.h(n))
            imprimir_solucao(resultado_greedy, "BUSCA GULOSA", problema)
            
            resultado_astar = astar_search(problema, lambda n: problema.h(n))
            imprimir_solucao(resultado_astar, "BUSCA A*", problema)
            
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()