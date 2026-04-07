import time
import matplotlib.pyplot as plt
from passeio_cavalo import PasseioDoCavalo

def realizar_benchmark():
    # Tamanhos que vamos testar
    tamanhos_warnsdorff = [5, 6, 8, 10, 16, 20, 24, 32]
    tamanhos_backtrack = [5, 6, 7, 8] # Backtrack trava se passar de 6x6
    
    tempos_w, operacoes_w = [], []
    tempos_b, operacoes_b = [], []
    
    print("Iniciando bateria de testes...")
    
    # 1. Testando Warnsdorff
    for n in tamanhos_warnsdorff:
        passeio = PasseioDoCavalo(n, 0, 0)
        inicio = time.perf_counter()
        passeio.resolver(algoritmo="warnsdorff")
        fim = time.perf_counter()
        
        tempos_w.append(fim - inicio)
        operacoes_w.append(passeio.avaliacoes)
        print(f"Warnsdorff {n}x{n} concluído.")
        
    # 2. Testando Backtracking (Atenção: o 6x6 pode levar alguns segundos/minutos)
    for n in tamanhos_backtrack:
        passeio = PasseioDoCavalo(n, 0, 0)
        inicio = time.perf_counter()
        passeio.resolver(algoritmo="backtracking")
        fim = time.perf_counter()
        
        tempos_b.append(fim - inicio)
        operacoes_b.append(passeio.avaliacoes)
        print(f"Backtracking {n}x{n} concluído.")


    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos_warnsdorff, tempos_w, marker='o', color='blue', label='Warnsdorff (Polinomial)')
    plt.plot(tamanhos_backtrack, tempos_b, marker='o', color='red', label='Backtracking (Exponencial)')
    
    # Usando escala logarítmica (igual o professor fez no PDF) para mostrar a explosão
    plt.yscale('log') 
    
    plt.title("Comparativo de Tempo de Execução (Escala Logarítmica)")
    plt.xlabel("Tamanho do Tabuleiro (N)")
    plt.ylabel("Tempo (Segundos)")
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.savefig("grafico_tempo.png") # Salva a imagem
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos_warnsdorff, operacoes_w, marker='o', color='green', label='Warnsdorff')
    plt.plot(tamanhos_backtrack, operacoes_b, marker='o', color='orange', label='Backtracking')
    
    plt.yscale('log')
    plt.title("Comparativo de Operações Matemáticas (Crescimento de Complexidade)")
    plt.xlabel("Tamanho do Tabuleiro (N)")
    plt.ylabel("Número de Avaliações")
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.savefig("grafico_operacoes.png") # Salva a imagem
    plt.close()

    print("Testes finalizados! As imagens 'grafico_tempo.png' e 'grafico_operacoes.png' foram salvas na pasta.")

if __name__ == "__main__":
    realizar_benchmark()