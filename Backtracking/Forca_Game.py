import string
from treelib import Tree
from graphviz import Digraph

resposta = input("Digite uma palavra:") #Pede para o user digitar uma palavra

class HangmanGame: #Classe do Jogo da forca
    def __init__(self, word):
        self.word = word #Recebe a palavra
        self.letras = list(word) #Separa cada char do string recebido
        self.positions = [] #Array vazio para guardar as posições das letras
        self.acertos = [] #Array vazio para guardar as letras certas
        self.erros = [] #Array vazio para guardar as letras erradas
        self.tree = Tree() #Cria a Tree
        self.root = f'{word}' #Define a raiz
        self.graph = Digraph(comment='Hangman Tree') #Nome do png

    def start(self):
        print(f'A palavra inserida tem {len(self.letras)} letras') #Diz quantas letras tem a palavra escolhida
        self.tree.create_node(self.root, self.root) #Cria o root principal
        self.game(self.root) #Inicia o jogo

    def game(self, root):
        tries = 0 #Número de tentativas

        for letter in string.ascii_lowercase + string.ascii_uppercase: #Vasculha todas as letras no ascii tanto lowercase quanto uppercase
            if (letter in self.acertos or letter in self.erros): #Verifica se a letra está em acertos ou erros
                continue

            if (letter in self.letras): #Verifica se a letra está na palavra
                for i, char in enumerate(self.letras): #Procura sua posição
                    if( (letter == char ) and (i not in self.positions)): #Verifica se é a primeira vez que a letra aparece
                        print(f'Tem a letra -{letter}- na posição {i}')
                        self.positions.append(i) #add a posição no array de posições
                        self.acertos.append(letter) #add a letra no array de letras certas
                        self.tree.create_node(letter, f'{letter}_{i}', parent=root) #Cria um nó para aquela letra indicando sua posição na palavra
                        self.graph.edge(root, f'{letter}_{i}', label=letter) #Plota o nó
                        break
            if(letter in self.acertos): #Verifica se a letra testada é pertencente a palavra
                for i, char in enumerate(self.letras): #Procura sua posição
                    if( (letter == char) and (i not in self.positions)): #Verifica se a letra pertence a alguma posição da palavra
                        print(f'Tem a letra -{letter}- na posição {i}')
                        self.positions.append(i) #add a posição no array de posições
                        self.tree.create_node(letter, f'{letter}_{i}', parent=root) #Cria um nó para aquela letra indicando sua posição na palavra
                        self.graph.edge(root, f'{letter}_{i}', label=letter) #Plota o nó
                        break
            else: # Letra não pertence a palavra
                tries += 1 #Aumenta o número de tentativas
                if tries >= len(string.ascii_lowercase + string.ascii_uppercase): #Verifica se o Número de tentativas extrapolou o alfabeto
                    print('Game over')
                    return

                self.erros.append(letter) #ADD a array de letra erradas
                self.tree.create_node(letter, f"{letter}_wrong", parent=root) #Cria um nó para aquela letra
                self.graph.edge(root, f"{letter}_wrong", label=letter) #Plota nó

        self.display_tree() #Mostra a tree
        if len(self.acertos) == len(set(self.letras)): #Verifica se todas as letras da palavra foram achadas
            print('Parabéns, você ganhou!')
        else: #Caso a palavra não pertença ele chama o def backtracking
            self.backtrack()
            self.game(root)

    def backtrack(self):#Usa o backtraking para tentar novamente
        if len(self.erros) > 0:
            last_error = self.erros.pop()
            self.tree.remove_node(f"{last_error}_wrong")
            #self.graph.remove_node(f"{last_error}_wrong")

    def display_tree(self): #Método para plotar imagem da tree
        print("Letras corretas:")
        print(self.tree.show(line_type="ascii", idhidden=True))

    def plot_tree(self): #Renderiza a tree
        self.graph.render('hangman_tree', format='png', cleanup=True)


teste = HangmanGame(resposta)
teste.start()
teste.plot_tree()















