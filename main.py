import time

class PasseioDoCavalo:
    def __init__(self, n, start_x, start_y):
        self.n = n
        self.tabuleiro = [[-1 for _ in range(n)] for _ in range(n)]
        
        self.movimentos_x = [2, 1, -1, -2, -2, -1, 1, 2]
        self.movimentos_y = [1, 2, 2, 1, -1, -2, -2, -1]
        
        self.pos_atual_x = start_x
        self.pos_atual_y = start_y
        
        self.tabuleiro[self.pos_atual_x][self.pos_atual_y] = 0

        self.avaliacoes = 0

    def movimento_valido(self, x, y):
        self.avaliacoes += 1
        return (0 <= x < self.n) and (0 <= y < self.n) and (self.tabuleiro[x][y] == -1)

    def contar_movimentos_futuros(self, x, y):
        # Warnsdorff: conta quantas casas válidas existem a partir da futura casa (x, y)
        count = 0
        for i in range(8):
            prox_x = x + self.movimentos_x[i]
            prox_y = y + self.movimentos_y[i]
            if self.movimento_valido(prox_x, prox_y):
                count += 1
        return count

    def proximo_movimento(self, passo):
        # 9 atua como "infinito", pois o máximo de opções futuras em um tabuleiro é 8
        min_futuros = 9 
        melhor_x = -1
        melhor_y = -1
        
        # Avalia todos os 8 movimentos possíveis a partir da posição atual
        for i in range(8):
            prox_x = self.pos_atual_x + self.movimentos_x[i]
            prox_y = self.pos_atual_y + self.movimentos_y[i]
            
            if self.movimento_valido(prox_x, prox_y):
                # Opções que o cavalo teria no salto SEGUINTE
                futuros = self.contar_movimentos_futuros(prox_x, prox_y)
                
                # Warnsdorff: escolhe sempre o caminho com MENOS opções futuras
                if futuros < min_futuros:
                    min_futuros = futuros
                    melhor_x = prox_x
                    melhor_y = prox_y
                    
        # Se não encontrou nenhum movimento válido (ficou preso)
        if min_futuros == 9:
            return False
            
        # Executa o salto definitivo
        self.pos_atual_x = melhor_x
        self.pos_atual_y = melhor_y
        self.tabuleiro[melhor_x][melhor_y] = passo
        return True

    def resolver(self):
        # O cavalo precisa dar (N * N) - 1 saltos para preencher todas as casas
        total_casas = self.n * self.n
        for passo in range(1, total_casas):
            if not self.proximo_movimento(passo):
                return False
        return True

    def imprimir_tabuleiro(self):
        print("\nCaminho do Cavalo:")
        for linha in self.tabuleiro:
            print(" ".join(str(celula).rjust(3, ' ') for celula in linha))
        print()

if __name__ == "__main__":
    print("=== Problema do Passeio do Cavalo (Warnsdorff) ===")
    
    try:
        n = int(input("Digite o tamanho do tabuleiro (N x N): "))
        
        if n <= 4 and n != 1:
            print(f"Não há solução possível para tabuleiros {n}x{n}. O cavalo não tem espaço para se movimentar livremente.")
        else:
            start_x = int(input(f"Digite a posição inicial X (0 até {n-1}): "))
            start_y = int(input(f"Digite a posição inicial Y (0 até {n-1}): "))
            
            if start_x < 0 or start_x >= n or start_y < 0 or start_y >= n:
                print("Posição inicial inválida!")
            else:
                passeio = PasseioDoCavalo(n, start_x, start_y)
                print("\nCalculando...")
                
                inicio_tempo = time.perf_counter()
                
                sucesso = passeio.resolver()
                
                fim_tempo = time.perf_counter()
                tempo_execucao = fim_tempo - inicio_tempo
                
                if sucesso:
                    print("Sucesso! Solução encontrada:")
                    passeio.imprimir_tabuleiro()
                else:
                    print("Não foi possível encontrar uma solução a partir desta posição inicial.")

                print("-" * 40)
                print("📊 RELATÓRIO DE DESEMPENHO")
                print("-" * 40)
                print(f"Tamanho do Tabuleiro : {n}x{n}")
                print(f"Posição Inicial      : ({start_x}, {start_y})")
                print(f"Tempo de Execução    : {tempo_execucao:.6f} segundos")
                print(f"Casas Avaliadas      : {passeio.avaliacoes} operações")
                print("-" * 40)
                
    except ValueError:
        print("Por favor, digite apenas números inteiros válidos.")