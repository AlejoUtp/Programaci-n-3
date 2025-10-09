%Integrantes:
%Kevin Alejandro Londoño Murillo


% ====================================================
% Punto 1: Backtracking Calles Canada
% ====================================================

% Hechos (conexiones con costo) LISTAS
	   % Nodo,  [ Aristas o Conexiones Directas ] . 
conexiones(s, [ (v1,16), (v2,13) ]).
conexiones(v1, [ (v3,12) ]).
conexiones(v2, [ (v1,4), (v4,14) ]).
conexiones(v3, [ (t,20), (v2,9) ]).
conexiones(v4, [ (t,4), (v3,7) ]).
conexiones(t, []).

% Regla: ¿Está conectado?
hay_conexion(X, Y) :- 
    conexiones(X,Aristas),
    member((Y,_),Aristas).

%Existe una conexión entre Saskatoon y Vancouver?
%Llamada en Terminal : hay_conexion(v3,s) 
%Devuelve =False


% Regla: ¿Un nodo tiene alguna arista?
tiene_arista(Nodo) :- 
    conexiones(Nodo, Aristas),
    Aristas \= []. 


% Regla: Costo total de X a Z pasando por Y
costo_por(X,Y,Z, CostoTotal) :-
    conexiones(X, AristasX),
    member((Y,C1), AristasX),
    conexiones(Y, AristasY),
    member((Z,C2), AristasY),
    CostoTotal is C1 + C2.

% Costo Total de X a Z pasando por VARIOS CAMINOS.

% Caso base: conexión directa               % camino(X, Y, Camino, Costo)  es como preguntar si se puede viajar de X a Y 
camino(X, Y, Visitados, [X, Y], Costo) :-   % pero tambien nos dice el costo de ese viaje, todos los posibles viajes
    conexiones(X, Lista),					% y los caminos exactos por los que pasaria.
    member((Y, Costo), Lista),
    \+ member(Y, Visitados).

% Caso recursivo: buscar conexión indirecta
camino(X, Y, Visitados, [X | Camino], CostoTotal) :-
    conexiones(X, Lista),
    member((Z, C1), Lista),
    \+ member(Z, Visitados),           % evitar repetir nodos
    camino(Z, Y, [Z | Visitados], Camino, C2),
    CostoTotal is C1 + C2.

% Predicado principal (interfaz sencilla)
camino(X, Y, Camino, Costo) :-
    camino(X, Y, [X], Camino, Costo).


%Con qué nodos está conectado Regina y cual es el costo de cada conexión?
%Llamada en terminal : conexiones(v4,Conexiones).

%Conexiones = [(t,4), (v3,7)]



%Es posible viajar desde Edmonton a Calgary?
%Llamada en Terminal : camino(v1,v2,Camino,Costo). 
%Devuelve : Camino = [v1, v3, v2],
%           Costo = 21
% si es posible pasando por v3 con un costo total de 21
