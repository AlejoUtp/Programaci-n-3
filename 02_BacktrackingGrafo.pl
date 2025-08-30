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


% Regla:  ¿Posible Viajar de X a Z?
viajar_por(X, Y, Z) :- conexion(X,Y,_), conexion(Y,Z,_).
%Es posible viajar desde Edmonton a Calgary?
%Llamada en Terminal : viajar_por(v1,D,v2). Devuelve : D=v3   Es posible
