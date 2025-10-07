% Hechos (conexiones con costo)
conexion(s, v1, 16).
conexion(s, v2, 13).
conexion(v1, v3, 12).
conexion(v2, v1, 4).
conexion(v2, v4, 14).
conexion(v3, t, 20).
conexion(v3, v2, 9).
conexion(v4, t, 4).
conexion(v4, v3, 7).

% Regla: ¿Está conectado?
hay_conexion(X, Y) :- conexion(X, Y, _).
%Existe una conexión entre Saskatoon y Vancouver?
%Llamada en Terminal : hay_conexion(v3,s) 
%Devuelve =False


% Regla: ¿Un nodo tiene alguna arista?
tiene_arista(Origen) :- conexion(Origen, _, _).


% Regla: Costo total de X a Z pasando por Y
costo_por(X, Y, Z, CT) :- conexion(X, Y, C1), conexion(Y, Z, C2),  CT is C1 + C2.
%Llamada en terminal : costo_por(s,v1,v2,Costo)
%devuelve: Costo = 20


%Con qué nodos está conectado Regina y cual es el costo de cada conexión?
%Llamada en terminal : conexion(v4,Destino,Costo).
%Costo = 4,
%Destino = t
%Costo = 7,
%Destino = v3


% Regla:  ¿Posible Viajar de X a Z?
viajar_por(X, Y, Z) :- conexion(X,Y,_), conexion(Y,Z,_).
%Es posible viajar desde Edmonton a Calgary?
%Llamada en Terminal : viajar_por(v1,D,v2). 
%Devuelve : D=v3   Es posible


% --- Regla principal: se puede viajar de X a Y? ---

% Caso base: existe una conexión directa
viajar(X, Y, _) :-
    conexion(X, Y, _).

% Caso recursivo con límite
viajar(X, Y, N) :-
    N > 0,
    conexion(X, Z, _),
    N1 is N - 1,
    viajar(Z, Y, N1).

% Predicado principal: por defecto limita a 10 pasos para que con por ejemplo viajar(v2,s). devuelva false y no se quede en bucle 
viajar(X, Y) :- viajar(X, Y, 10).
