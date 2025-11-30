import matplotlib.pyplot as plt
import networkx as nx
        
def criar_arvore(lista: list[int]):
    G = nx.DiGraph()
    if not lista:
        return G, {}
    
    def add_nos(lista_ordenada, x = 0, y = 0, horizontal = 4):
        if not lista_ordenada:
            return None
        
        meio = len(lista_ordenada)//2
        no_valor = lista_ordenada[meio]
        
        G.add_node(no_valor, pos=(x,y))
        esquerda = add_nos(
            lista_ordenada[:meio],
            x - horizontal,
            y - 1,
            horizontal / 2)
        
        if esquerda is not None:
            G.add_edge(no_valor, esquerda)
        direita = add_nos(
            lista_ordenada[meio+1:],
            x + horizontal,
            y - 1,
            horizontal / 2)
        
        if direita is not None:
            G.add_edge(no_valor, direita)
        return no_valor
    
    add_nos(lista)
    pos = nx.get_node_attributes(G, 'pos')
    return G, pos



def plotar_arvore(G, pos, lista=None):
    fig, ax = plt.subplots(figsize=(9, 7))
    nx.draw(G, pos, with_labels=True, node_size=800, node_color='lightgreen', font_size=8, ax=ax)
    
    if lista:
        lista_ordenada = sorted(lista)
        ax.set_title(f"Lista ordenada: {lista_ordenada}", fontsize=12, pad=20, color="darkblue")
    else:
        ax.set_title(fontsize=14, pad=20, color="darkblue")
    
    ax.axis('off')
    plt.show()  


def atualizar_arvore(G, pos, mensagem=None, lista=None, no_destaque=None):
    
    no_cores = []
    
    for no in G.nodes():
        if no == no_destaque:
            no_cores.append('red')
        else:
            no_cores.append('lightblue')    
    
    fig, ax = plt.subplots(figsize=(10,7))
    nx.draw(G, pos, with_labels=True, node_size=800, node_color=no_cores, font_size=12, ax=ax)
    
    if lista:
        lista_ordenada = sorted(lista)
        ax.set_title(f"Árvore atualizada!\n{mensagem}\nLista atual: {lista_ordenada}", 
                     fontsize=10, pad=20, color="darkblue")
    else:
        ax.set_title("Árvore atualizada!", fontsize=8, pad=20, color="darkblue")

    plt.axis('off')
    plt.show()
    
    return G, pos

def inserir(lista, n):
    lista.append(n)
    
    G, pos = criar_arvore(lista)
            
    print(f'Adicionado o valor {n}\nRebalanceando a árvore...')
    
    atualizar_arvore(G, pos, f'Inserido o valor: {n}', lista, no_destaque=n)        
    


def excluir(lista, n):
    G, pos = criar_arvore(lista)

    atualizar_arvore(G, pos, f'Será removido o valor: {n}', lista=lista, no_destaque=n) 

    if n in lista:
        lista.remove(n)
        print(f'Removendo o valor {n}\nRebalanceando a árvore...')
        G, pos = criar_arvore(lista) 
        atualizar_arvore(G, pos, f'Removido o valor: {n}', lista)
    else:
        print(f'O valor {n} não está na lista!')
        
  
    
    
    
def buscar(lista, n, inicio = 0, fim = None):
    if n not in lista:
        return
    lista_ordenada = sorted(lista)
    
    if fim is None:
        fim = len(lista_ordenada)-1
    
    
    meio = (inicio + fim) // 2
    if lista_ordenada[meio] == n:
        
        print(f'O número {n} foi encontrado na posição {meio}! Removendo e recriando a árvore...')
        
        G, pos = criar_arvore(lista)
        atualizar_arvore(G, pos, f'Será removido o valor: {n}', lista, no_destaque=n)
        
        print(f'Removendo {n} e rebalanceando a árvore...\n')
        lista.remove(n)
        G, pos = criar_arvore(lista)
        atualizar_arvore(G, pos, f'Removido o valor {n} após ser encontrado' , lista, no_destaque=n)    
            
    elif lista_ordenada[meio] < n:
        return buscar(lista, n, meio + 1, fim)
    else:
        return buscar(lista, n, inicio, meio - 1)




lista_valores = input('Digite números separados por vírgula ou espaço: \n\n')
lista_valores = lista_valores.replace(',', ' ')
lista = [int(x) for x in lista_valores.split()]

if len(lista) != len(set(lista)):
    print("Atenção: você digitou números repetidos. Eles serão removidos.\n\n")
    lista = list(set(lista))


G, pos = criar_arvore(lista)

plotar_arvore(G, pos, lista)


while True:
    menu = int(input(
        '\nO que deseja fazer? Digite APENAS o número de uma das opões abaixo:\n \n1 - ENCONTRAR UM ELEMENTO\n2 - INSERIR UM ELEMENTO\n3 - EXCLUIR UM ELEMENTO\n0 - SAIR/ENCERRAR\n\nR: '))
    
    if menu == 1:
        numero = int(input('\nQual o número que deseja encontrar?\n'))
        if numero in lista:
            buscar(lista, numero)
        else:
            print(f'\nO número {numero} não existe na lista informada!\n\n')
            plotar_arvore(G, pos, lista)
            continue
        
    elif menu == 2:
        elemento = int(input('\nDigite o número que deseja inserir na árvore:\n'))
        if elemento not in lista:
            inserir(lista, elemento)
        else:
            print(f'\nO número {elemento} já existe na lista! Não é possível adicionar números repetidos.\n\n')
            plotar_arvore(G, pos, lista)
            continue
        
    elif menu == 3:
        n_excluir = int(input('\nDigite o número que deseja excluir da árvore: \n'))
        if n_excluir in lista:
            excluir(lista, n_excluir)
        else:
            print(f'\nO número {n_excluir} não existe na lista informada!\n\n')
            plotar_arvore(G, pos, lista)
            continue
        
    elif menu == 0:
        print('Programa encerrado.')
        break
    
    else:
        print('Opção inválida! Digite o NÚMERO correto da ação que pretende executar!\n')
        continue
