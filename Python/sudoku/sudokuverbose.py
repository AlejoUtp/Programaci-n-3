import itertools as it

# ---------------------------
# FUNCIONALIDAD VERBOSE
# ---------------------------

VERBOSE = True
VERBOSE_LEVEL = 2   # 0 = básico, 1 = detallado, 2 = muy detallado

def vprint(level, *args, **kwargs):
    """Imprime según el nivel deseado."""
    if VERBOSE and level <= VERBOSE_LEVEL:
        print(*args, **kwargs)

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
                    vprint(2, f"[AllDif] Eliminando {valor} de {var2} porque {var} = {valor}")
                    anyChange = True
    return anyChange

def HiddenSingle(var_doms, vars):
    anyChange = False
    for n in range(1, 10):
        celdas_con_n = [v for v in vars if n in var_doms[v]]
        if len(celdas_con_n) == 1:
            if var_doms[celdas_con_n[0]] != {n}:
                vprint(1, f"[HiddenSingle] Única opción: {celdas_con_n[0]} = {n}")
                var_doms[celdas_con_n[0]] = {n}
                anyChange = True
    return anyChange

def NakedPairs(var_doms, vars):
    anyChange = False
    pares = [v for v in vars if len(var_doms[v]) == 2]
    for i in range(len(pares)):
        for j in range(i + 1, len(pares)):
            if var_doms[pares[i]] == var_doms[pares[j]]:
                pair_values = var_doms[pares[i]]
                vprint(1, f"[NakedPairs] {pares[i]} y {pares[j]} comparten {pair_values}")
                for var in vars:
                    if var not in (pares[i], pares[j]):
                        before = set(var_doms[var])
                        var_doms[var] -= pair_values
                        if var_doms[var] != before:
                            vprint(2, f"    Eliminando {pair_values} de {var}")
                            anyChange = True
    return anyChange

def PointingPairs(doms, box):
    anyChange = False
    for n in range(1, 10):
        posiciones = [v for v in box if n in doms[v]]
        if len(posiciones) < 2:
            continue

        filas = {v[1:] for v in posiciones}
        columnas = {v[0] for v in posiciones}

        if len(filas) == 1:
            fila = next(iter(filas))
            vprint(1, f"[PointingPairs] En box → {n} solo en fila {fila}")
            for c in "ABCDEFGHI":
                celda = f"{c}{fila}"
                if celda not in box and n in doms[celda]:
                    doms[celda].discard(n)
                    vprint(2, f"    → Eliminado {n} de {celda}")
                    anyChange = True

        if len(columnas) == 1:
            col = next(iter(columnas))
            vprint(1, f"[PointingPairs] En box → {n} solo en col {col}")
            for r in map(str, range(1, 10)):
                celda = f"{col}{r}"
                if celda not in box and n in doms[celda]:
                    doms[celda].discard(n)
                    vprint(2, f"    → Eliminado {n} de {celda}")
                    anyChange = True

    return anyChange

# ---------------------------
# BACKTRACKING
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
                vprint(1, f"[Restricción] {func.__name__} produjo cambios")
                cambio = True
    return var_doms

def backtracking(var_doms, constraints, depth=0):
    indent = "  " * depth
    vprint(0, f"{indent}↳ Nivel {depth}")

    var_doms = aplicar_restricciones(var_doms, constraints)

    if esta_completo(var_doms):
        vprint(0, f"{indent}✔ Solución completa")
        return var_doms
    
    if hay_conflicto(var_doms):
        vprint(0, f"{indent}✘ Conflicto → backtrack")
        return None

    var = elegir_variable(var_doms)
    vprint(0, f"{indent}Eligiendo {var} con dominio {var_doms[var]}")

    for valor in list(var_doms[var]):
        vprint(0, f"{indent}Intentando {var} = {valor}")
        nuevo = copiar_estado(var_doms)
        nuevo[var] = {valor}
        result = backtracking(nuevo, constraints, depth + 1)
        if result is not None:
            return result
        vprint(0, f"{indent}Falló {var} = {valor}, retrocediendo...")

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
# IMPRIMIR
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
# PROCESO
# ---------------------------

print("\n🔍 Ejecutando solver completo...\n")
solucion = backtracking(var_doms, constraints)

if solucion:
    print("✅ Sudoku resuelto con éxito:")
    mostrar_tablero(solucion)
else:
    print("❌ No tiene solución.")
