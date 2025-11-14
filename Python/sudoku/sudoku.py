# -*- coding: utf-8 -*-
"""Versión mejorada del modelo Sudoku en Python"""

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


def ExcValue(var_doms, vars):
    anyChange = False
    for var in vars:
        if len(var_doms[var]) > 1:
            A = var_doms[var]
            U = set()
            for var2 in vars:
                if var != var2:
                    U = U.union(var_doms[var2])
            Ex = A - U
            if len(Ex) == 1:
                var_doms[var] = Ex
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

# ---------------------------
# DEFINIR GRUPOS Y RESTRICCIONES
# ---------------------------

rows = range(1, 10)
varsGroups = (
    DefRowsConstraints(cols, rows)
    + DefColsConstraints(cols, rows)
    + DefBoxesConstraints(cols, rows)
)

constraints = []
for group in varsGroups:
    constraints.append(("AllDif", group))
    constraints.append(("ExcValue", group))
    constraints.append(("HiddenSingle", group))
    constraints.append(("NakedPairs", group))
   


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
            if c in "CF":  # divisiones verticales
                fila += "| "
        print(fila)
        if r in (3, 6):
            print("- " * 11)
    print()


# ---------------------------
# PROCESO ITERATIVO
# ---------------------------

iteration=1
while(True):
  anyChange=False
  for constraint in constraints:
    anyChangeAux=eval(f"{constraint[0]}(var_doms,{constraint[1]})")
    anyChange=anyChangeAux if anyChange==False else anyChange
  print(f"Iteracion {iteration}")
  iteration+=1
  #input()
  if anyChange==False:
    break

print(var_doms)

print("✅ Proceso terminado. Estado final del Sudoku:")

