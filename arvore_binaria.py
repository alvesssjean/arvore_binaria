import matplotlib.pyplot as plt
import networkx as nx
        
def criar_arvore(lista: list[int]):
    G = nx.DiGraph()
    if not lista:
        return G, {}
    
    def add_nos(lista_ordenada, x = 0, y = 0, horizontal = 4):
        if not lista_ordenada:
            return None
        lista_ordenada = sorted(lista_ordenada)
        
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
    nx.draw(G, pos, with_labels=True, node_size=800, node_color='lightgreen', font_size=10, ax=ax)
    
    if lista:
        lista_ordenada = sorted(lista)
        ax.set_title(f"Lista ordenada: {lista_ordenada}", fontsize=14, pad=20, color="darkblue")
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
    
    fig, ax = plt.subplots(figsize=(9,7))
    nx.draw(G, pos, with_labels=True, node_size=800, node_color=no_cores, font_size=10, ax=ax)
    
    if lista:
        lista_ordenada = sorted(lista)
        ax.set_title(f"Árvore atualizada!\n{mensagem}\nLista atual: {lista_ordenada}", 
                     fontsize=14, pad=20, color="darkblue")
    else:
        ax.set_title("Árvore atualizada!", fontsize=14, pad=20, color="darkblue")

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
    lista_ordenada = sorted(lista)
    
    if fim is None:
        fim = len(lista_ordenada)-1
    
    
    meio = (inicio + fim) // 2
    if lista_ordenada[meio] == n:
        
        print(f'O número {n} foi encontrado na posição {meio}! Removendo e recriando a árvore...')
        
        G, pos = criar_arvore(lista)
        atualizar_arvore(G, pos, f'Será removido o valor: {n}', lista, n)
        
        print(f'Removendo {n} e rebalanceando a árvore...')
        lista.remove(n)
        G, pos = criar_arvore(lista)
        atualizar_arvore(G, pos, f'Removido o valor {n} após ser encontrado' , lista, n)    
            
    elif lista_ordenada[meio] < n:
        return buscar(lista, n, meio + 1, fim)
    else:
        return buscar(lista, n, inicio, meio - 1)


# lista = [10, 9, 5, 45, 23, 1, 8, 65]

# Criar grafo
# G, pos = criar_arvore(lista)

# # Plotar grafo
# plotar_arvore(G, pos, lista=lista)
# buscar(lista, 10)
# inserir(lista, 22)
# excluir(lista, 45)


