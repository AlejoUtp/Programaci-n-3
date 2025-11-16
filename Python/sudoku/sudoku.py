import itertools as it

# ---------------------------
# CONFIGURACIÓN INICIAL
# ---------------------------

cols = "ABCDEFGHI"
keys = list(it.product(range(1, 10), cols))
strKeys = [f"{key[1]}{key[0]}" for key in keys]
var_doms = {key: set(range(1, 10)) for key in strKeys}

# ---------------------------
# CARGAR TABLERO
# ---------------------------

boardname="board"
try:
    with open(boardname, 'r') as f:
        for key in var_doms.keys():
            valor = f.readline().strip()
            if valor.isdigit() and len(valor) == 1:
                var_doms[key] = {int(valor)}
except FileNotFoundError:
    print(f"⚠️ No se encontró el archivo '{boardname}'. Se usará un tablero vacío.")


# ---------------------------
# FUNCIONES DE CONSTRAINTS
# ---------------------------

def DefRowsConstraints(cols, rows):
    return [[f"{id}{i}" for id in cols] for i in rows]

def DefColsConstraints(cols, rows):
    return [[f"{id}{i}" for i in rows] for id in cols]

def DefBoxesConstraints(cols, rows):
    boxes = []
    for i in range(3):
        for j in range(3):
            group = [f"{cols[i*3 + x]}{rows[j*3 + y]}" for x in range(3) for y in range(3)]
            boxes.append(group)
    return boxes


# ---------------------------
# REGLAS DEL SUDOKU
# ---------------------------

def AllDif(var_doms, vars):
    anyChange = False
    for var in vars:
        if len(var_doms[var]) == 1:
            valor = list(var_doms[var])[0]
            for var2 in vars:
                if var != var2 and valor in var_doms[var2]:
                    var_doms[var2].discard(valor)
                    anyChange = True
    return anyChange

def HiddenSingle(var_doms, vars):
    """Si un número solo aparece en una celda del grupo, se asigna."""
    anyChange = False
    for n in range(1, 10):
        celdas_con_n = [v for v in vars if n in var_doms[v]]
        if len(celdas_con_n) == 1:
            # Solo marca cambio si la celda no está ya asignada
            if var_doms[celdas_con_n[0]] != {n}:
                var_doms[celdas_con_n[0]] = {n}
                anyChange = True
    return anyChange


def NakedPairs(var_doms, vars):
    """Si dos celdas tienen el mismo par de valores, se eliminan de las demás."""
    anyChange = False
    pares = [v for v in vars if len(var_doms[v]) == 2]
    for i in range(len(pares)):
        for j in range(i + 1, len(pares)):
            if var_doms[pares[i]] == var_doms[pares[j]]:
                pair_values = var_doms[pares[i]]
                for var in vars:
                    if var not in (pares[i], pares[j]):
                        before = set(var_doms[var])
                        var_doms[var] -= pair_values
                        # Solo marca cambio si algo fue eliminado
                        if var_doms[var] != before:
                            anyChange = True
    return anyChange

def PointingPairs(doms, box):
    """
    doms: dict de dominios (valores int)
    box: lista de 9 celdas de la caja (ej. ["A1","A2",...])
    Devuelve True si modificó algún dominio, False si no.
    """
    anyChange = False

    for n in range(1, 10):  # n es entero
        posiciones = [v for v in box if n in doms[v]]
        if len(posiciones) < 2:
            continue

        filas = {v[1:] for v in posiciones}  # '1'..'9'
        columnas = {v[0] for v in posiciones}

        # todas en la misma fila dentro de la caja
        if len(filas) == 1:
            fila = next(iter(filas))
            for c in "ABCDEFGHI":
                celda = f"{c}{fila}"
                if celda not in box and n in doms[celda]:
                    doms[celda].discard(n)   # discard es más seguro que remove
                    anyChange = True

        # todas en la misma columna dentro de la caja
        if len(columnas) == 1:
            col = next(iter(columnas))
            for r in map(str, range(1, 10)):
                celda = f"{col}{r}"
                if celda not in box and n in doms[celda]:
                    doms[celda].discard(n)
                    anyChange = True

    return anyChange

# ---------------------------
# Comenzamos con el Backtracking
# ---------------------------

def esta_completo(var_doms):
    return all(len(var_doms[v]) == 1 for v in var_doms)

def elegir_variable(var_doms):
    sin_asignar = [v for v in var_doms if len(var_doms[v]) > 1]
    return min(sin_asignar, key=lambda v: len(var_doms[v]), default=None)

def hay_conflicto(var_doms):
    return any(len(var_doms[v]) == 0 for v in var_doms)

def copiar_estado(var_doms):
    return {k: set(v) for k, v in var_doms.items()}

def aplicar_restricciones(var_doms, constraints):
    cambio = True
    while cambio:
        cambio = False
        for func, group in constraints:
            if func(var_doms, group):
                cambio = True
    return var_doms

def backtracking(var_doms, constraints):

     # Propagar restricciones
    var_doms = aplicar_restricciones(var_doms, constraints)
    
    if esta_completo(var_doms):
        return var_doms
    
    if hay_conflicto(var_doms):
        return None
    
     # Elegir variable por MRV
    var = elegir_variable(var_doms)

    # Intentar cada valor
    for valor in list(var_doms[var]):
        nuevo_estado = copiar_estado(var_doms)
        nuevo_estado[var] = {valor}
        resultado = backtracking(nuevo_estado, constraints)
        if resultado is not None:
            return resultado
    
    # Si ninguno funcionó → backtrack
    return None

    


# ---------------------------
# DEFINIR GRUPOS Y RESTRICCIONES
# ---------------------------

rows = range(1, 10)

varsGroups = (
    DefRowsConstraints(cols, rows)
    + DefColsConstraints(cols, rows)
    + DefBoxesConstraints(cols, rows)
)


boxes = DefBoxesConstraints(cols, rows)

constraints = []
for group in varsGroups:
    constraints.append((AllDif, group))
    constraints.append((HiddenSingle, group))
    constraints.append((NakedPairs, group))
    for group in boxes:
       constraints.append((PointingPairs, group))
    
   


# ---------------------------
# FUNCIÓN PARA IMPRIMIR TABLERO
# ---------------------------

def mostrar_tablero(var_doms):
    print("\nTABLERO ACTUAL:\n")
    for r in range(1, 10):
        fila = ""
        for c in cols:
            val = var_doms[f"{c}{r}"]
            if len(val) == 1:
                fila += str(list(val)[0]) + " "
            else:
                fila += ". "
            if c in "CF": 
                fila += "| "
        print(fila)
        if r in (3, 6):
            print("- " * 11)
    print()


# ---------------------------
# PROCESO ITERATIVO
# ---------------------------

print("\n🔍 Ejecutando solver completo...\n")
solucion = backtracking(var_doms, constraints)

if solucion:
    print("✅ Sudoku resuelto con éxito:")
    mostrar_tablero(solucion)
else:
    print("❌ No tiene solución.")

