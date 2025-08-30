%Integrantes:

%Juan Esteban Albornoz Gil
%Karen Alejandra Jaramillo López
%Kevin Alejandro Londoño Murillo

%Punto 1

padre_de(abraham, herbert).
padre_de(abraham, homero).
padre_de(clancy, patty).
padre_de(clancy, selma).
padre_de(clancy, marge).
padre_de(homero, bart).
padre_de(homero, lisa).
padre_de(homero, maggie).
madre_de(mona, homero).
madre_de(jacqueline, patty).
madre_de(jacqueline, selma).
madre_de(jacqueline, marge).
madre_de(marge, bart).
madre_de(marge, lisa).
madre_de(marge, maggie).
madre_de(selma, ling).
es_mujer(mona).
es_mujer(jacqueline).
es_mujer(marge).
es_mujer(patty).
es_mujer(selma).
es_mujer(lisa).
es_mujer(maggie).
es_mujer(ling).
es_hombre(abraham).
es_hombre(herbert).
es_hombre(homero).
es_hombre(clancy).
es_hombre(bart).

%Reglas

abuelo_de(X, Y) :- X \= Y, es_hombre(X), padre_de(X,Z), (padre_de(Z,Y) ; madre_de(Z,Y)).
abuela_de(X, Y) :- X \= Y, es_mujer(X), madre_de(X,Z), (padre_de(Z,Y) ; madre_de(Z,Y)).

hermano_de(X, Y) :- X\=Y, es_hombre(X), ((madre_de(Z, X), madre_de(Z, Y)) ;(padre_de(W, X), padre_de(W, Y))).
hermana_de(X, Y) :- X\=Y, es_mujer(X), ((madre_de(Z, X), madre_de(Z, Y)) ;(padre_de(W, X), padre_de(W, Y))).

tio_de(X, Y) :- X\=Y, es_hombre(X), ((madre_de(M,Y), hermano_de(X,M)); (padre_de(P,Y), hermano_de(X,P); hermana_de(X,P))).
tia_de(X, Y) :- X\=Y, es_mujer(X), ((madre_de(M,Y), hermana_de(X, M)); (padre_de(P,Y), hermana_de(X,P))).

hijo_de(X, Y) :- X\=Y, es_hombre(X), (padre_de(Y, X); madre_de(Y, X)).
hija_de(X, Y) :- X\=Y, es_mujer(X), (padre_de(Y, X); madre_de(Y, X)).

primo_de(X, Y) :- X\=Y, es_hombre(X), ((padre_de(P, X), (tio_de(P, Y); tia_de(P, Y))) ; (madre_de(M, X), (tio_de(M, Y); tia_de(M, Y)))).
prima_de(X, Y) :- X\=Y, es_mujer(X),  ((padre_de(P, X), (tio_de(P, Y); tia_de(P, Y))) ; (madre_de(M, X), (tio_de(M, Y); tia_de(M, Y)))).

%----------------------------------------------------------------------------------------------------------------------------------------

%punto 2

es_estadounidense(west).
es_nacion(corea_sur).
es_enemigo(corea_sur, eeuu).
es_misil(m1).
pertenece(m1, corea_sur).       % corea del Sur tiene el misil m1
vendio(west, m1, corea_sur).    % West le vendió el misil a Corea del Sur

% Reglas
es_arma(X) :- es_misil(X).
es_hostil(X) :- es_enemigo(X, eeuu), es_nacion(X).

es_criminal(X):- es_estadounidense(X), vendio(X, Arma, Nacion), es_arma(Arma), es_hostil(Nacion).

