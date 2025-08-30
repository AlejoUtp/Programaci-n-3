%Integrantes:
%Juan Esteban Albornoz Gil
%Karen Alejandra Jaramillo López
%Kevin Alejandro Londoño Murillo

% Punto 1: Relaciones familiares

% Hechos: Relaciones de parentesco
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

% Hechos: Género de los personajes
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

% Reglas: Relaciones familiares derivadas
abuelo_de(X, Y) :-             % X es abuelo de Y si:
    X \= Y,                    % X y Y son diferentes
    es_hombre(X),              % X es hombre
    padre_de(X, Z),            % X es padre de Z
    (padre_de(Z, Y) ; madre_de(Z, Y)). % Z es padre o madre de Y

abuela_de(X, Y) :-             % X es abuela de Y si:
    X \= Y,                    % X y Y son diferentes
    es_mujer(X),               % X es mujer
    madre_de(X, Z),            % X es madre de Z
    (padre_de(Z, Y) ; madre_de(Z, Y)). % Z es padre o madre de Y

hermano_de(X, Y) :-            % X es hermano de Y si:
    X \= Y,                    % X y Y son diferentes
    es_hombre(X),              % X es hombre
    ((madre_de(Z, X), madre_de(Z, Y)) ; % Comparten madre
    (padre_de(W, X), padre_de(W, Y))). % O comparten padre

hermana_de(X, Y) :-            % X es hermana de Y si:
    X \= Y,                    % X y Y son diferentes
    es_mujer(X),               % X es mujer
    ((madre_de(Z, X), madre_de(Z, Y)) ; % Comparten madre
    (padre_de(W, X), padre_de(W, Y))). % O comparten padre

tio_de(X, Y) :-                % X es tío de Y si:
    X \= Y,                    % X y Y son diferentes
    es_hombre(X),              % X es hombre
    ((madre_de(M, Y), hermano_de(X, M)) ; % Hermano de la madre de Y
    (padre_de(P, Y), (hermano_de(X, P) ; hermana_de(X, P)))). % Hermano o hermana del padre de Y

tia_de(X, Y) :-                % X es tía de Y si:
    X \= Y,                    % X y Y son diferentes
    es_mujer(X),               % X es mujer
    ((madre_de(M, Y), hermana_de(X, M)) ; % Hermana de la madre de Y
    (padre_de(P, Y), hermana_de(X, P))). % Hermana del padre de Y

hijo_de(X, Y) :-               % X es hijo de Y si:
    X \= Y,                    % X y Y son diferentes
    es_hombre(X),              % X es hombre
    (padre_de(Y, X) ; madre_de(Y, X)). % Y es padre o madre de X

hija_de(X, Y) :-               % X es hija de Y si:
    X \= Y,                    % X y Y son diferentes
    es_mujer(X),               % X es mujer
    (padre_de(Y, X) ; madre_de(Y, X)). % Y es padre o madre de X

primo_de(X, Y) :-              % X es primo de Y si:
    X \= Y,                    % X y Y son diferentes
    es_hombre(X),              % X es hombre
    ((padre_de(P, X), (tio_de(P, Y) ; tia_de(P, Y))) ; % Padre de X es tío o tía de Y
    (madre_de(M, X), (tio_de(M, Y) ; tia_de(M, Y)))). % Madre de X es tío o tía de Y

prima_de(X, Y) :-              % X es prima de Y si:
    X \= Y,                    % X y Y son diferentes
    es_mujer(X),               % X es mujer
    ((padre_de(P, X), (tio_de(P, Y) ; tia_de(P, Y))) ; % Padre de X es tío o tía de Y
    (madre_de(M, X), (tio_de(M, Y) ; tia_de(M, Y)))). % Madre de X es tío o tía de Y

%----------------------------------------------------------------------------------------------------------------------------------------

% Punto 2: Relaciones internacionales

% Hechos
estadounidense(west).
vendio_a(west, m1, corea).
es_arma(m1).
es_hostil(corea).

% Ley: es un crimen para un estadounidense vender armas a naciones hostiles.
es_criminal(Persona) :-
    estadounidense(Persona),
    vendio_a(Persona, Arma, Nacion),
    es_arma(Arma),
    es_hostil(Nacion).

