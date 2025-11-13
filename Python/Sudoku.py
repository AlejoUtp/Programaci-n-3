# =======================================
# Modelo estructural de Sudoku como CSP
# =======================================

# Cada celda del Sudoku es una variable (fila, columna)
# Cada variable puede tomar valores del 1 al 9

class SudokuCSP:
    def __init__(self):
        # 1️ Variables: representamos las 81 celdas
        # Usamos tuplas (fila, columna)
        self.variables = [(r, c) for r in range(9) for c in range(9)]
        
        # 2️ Dominios: cada variable puede tener valores del 1 al 9
        self.domains = {var: set(range(1, 10)) for var in self.variables}
        
        # 3️ Restricciones: pares de celdas que no pueden tener el mismo valor
        self.constraints = self.generar_restricciones()

    def generar_restricciones(self):
        restricciones = []
        
        for r in range(9):
            for c in range(9):
                # Mismo valor no puede repetirse en fila, columna o subcuadro
                for k in range(9):
                    if k != c:
                        restricciones.append(((r, c), (r, k)))  # misma fila
                    if k != r:
                        restricciones.append(((r, c), (k, c)))  # misma columna
                
                # Bloques 3x3
                bloque_fila = (r // 3) * 3
                bloque_col = (c // 3) * 3
                for i in range(bloque_fila, bloque_fila + 3):
                    for j in range(bloque_col, bloque_col + 3):
                        if (i, j) != (r, c):
                            restricciones.append(((r, c), (i, j)))
        
        return restricciones

    def __str__(self):
        return f"SudokuCSP con {len(self.variables)} variables y {len(self.constraints)} restricciones."


# =======================================
# Mostrar El dominio de cada casilla
# =======================================
if __name__ == "__main__":
    sudoku = SudokuCSP()
    print(sudoku)
    # Mostrar dominio de la celda (0,0)
    print("Dominio de (0,0):", sudoku.domains[(0, 0)])  #como el sudoku está vacio cada casilla puede contener cualquier numero del 1 al 9 
#Luego haremos las verificaciones para un sudoku con valores asignados
