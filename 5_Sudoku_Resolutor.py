'''Utiliza la biblioteca pygame (consulta las instrucciones de instalación de pip) para implementar una 
interfaz gráfica (GUI) que resuelve automáticamente los rompecabezas de Sudoku.
Para resolver un rompecabezas de Sudoku, puedes crear un programa que utilice un algoritmo de retroceso 
(backtracking) que verifica incrementalmente soluciones, adoptando o abandonando la solución actual si no es viable.
Este paso de abandonar una solución es la característica definitoria de un enfoque de retroceso, ya que el programa 
retrocede para probar una nueva solución hasta que encuentra una válida. Este proceso se lleva a cabo 
de manera incremental hasta que todo el tablero se haya completado correctamente.'''

import pygame
import time

# Inicializar pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 600, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SudokuMaster - Resolver Automático")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (220, 220, 220)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# Fuente
FONT = pygame.font.SysFont("Segoe UI", 40)
SMALL_FONT = pygame.font.SysFont("Segoe UI", 30)

# Tablero de ejemplo (0 = vacío)
board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

class SudokuSolver:
    def __init__(self):
        self.board = [row[:] for row in board]  # copia del tablero
        self.screen = SCREEN
        self.running = True

    def draw_board(self):
        self.screen.fill(WHITE)
        
        # Dibujar líneas del tablero
        for i in range(10):
            thickness = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, BLACK, (30, 50 + i*60), (570, 50 + i*60), thickness)
            pygame.draw.line(self.screen, BLACK, (30 + i*60, 50), (30 + i*60, 590), thickness)
        
        # Dibujar números
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    color = BLACK if board[i][j] != 0 else BLUE  # azul = insertado por el solver
                    text = FONT.render(str(self.board[i][j]), True, color)
                    self.screen.blit(text, (30 + j*60 + 20, 50 + i*60 + 8))

        # Botón Resolver
        pygame.draw.rect(self.screen, GREEN, (50, 620, 200, 60))
        text = SMALL_FONT.render("Resolver", True, WHITE)
        self.screen.blit(text, (90, 632))

        # Botón Limpiar
        pygame.draw.rect(self.screen, RED, (350, 620, 200, 60))
        text = SMALL_FONT.render("Limpiar", True, WHITE)
        self.screen.blit(text, (405, 632))

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def is_valid(self, num, pos):
        row, col = pos

        # Verificar fila
        for j in range(9):
            if self.board[row][j] == num and col != j:
                return False

        # Verificar columna
        for i in range(9):
            if self.board[i][col] == num and row != i:
                return False

        # Verificar caja 3x3
        box_x = col // 3
        box_y = row // 3
        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def solve(self):
        find = self.find_empty()
        if not find:
            return True  # resuelto
        row, col = find

        for num in range(1, 10):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num

                self.draw_board()
                pygame.display.update()
                pygame.time.delay(50)  # animación

                if self.solve():
                    return True

                self.board[row][col] = 0  # backtracking
                self.draw_board()
                pygame.display.update()
                pygame.time.delay(50)

        return False

    def run(self):
        while self.running:
            self.draw_board()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 50 <= x <= 250 and 620 <= y <= 680:
                        self.solve()
                    if 350 <= x <= 550 and 620 <= y <= 680:
                        self.board = [row[:] for row in board]
                        self.draw_board()

        pygame.quit()

# Ejecutar
if __name__ == "__main__":
    solver = SudokuSolver()
    solver.run()