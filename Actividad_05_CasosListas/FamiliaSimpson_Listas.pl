%Integrantes:
%Kevin Alejandro Londoño Murillo


% ====================================================
% Punto 1: Relaciones familiares Con Listas
% ====================================================

% Hechos En Lista: Nombre , Genero , Hijos.

persona(abraham, hombre, [herbert, homero]). 
persona(clancy, hombre, [patty, selma, marge]).
persona(homero, hombre, [bart, lisa, maggie]). 
persona(mona, mujer, [homero]).
persona(jacqueline, mujer, [patty, selma, marge]).
persona(marge, mujer, [bart, lisa, maggie]).
persona(selma, mujer, [ling]).

% Reglas: Relaciones familiares derivadas

abuelo_de(X, Y) :-             % X es abuelo de Y si:
    persona(X,hombre,Hijos),   % X es hombre y tiene hijos
    member(Z,Hijos),		   % Z es Hijo de X
    persona(Z,_,Nietos),		% Z tiene Hijos osea Nietos de X
    member(Y,Nietos).			% Y hace parte de esos Hijos de Z osea es Nieto de X
  
abuela_de(X, Y) :-             
   persona(X,mujer,Hijos),   
    member(Z,Hijos),		  
    persona(Z,_,Nietos),		
    member(Y,Nietos).			

%====================================================

hermano_de(X, Y) :-            % X es hermano de Y si:
     X \= Y,					% X y Y son diferentes, no puedes ser hermano de ti mismo
    persona(X,hombre,_), 		% X es Hombre
    persona(Z,_,Hijos),			% Z tiene Hijos	
    member(X,Hijos),			% X hace parte de esos Hijos
    member(Y,Hijos).			% y Y hace parte tambien de esos Hijos, osea tienen en mismo padre o madre y son hermanos X y Y.

hermana_de(X, Y) :-           
    X \= Y,					
    persona(X,mujer,_), 		
    persona(Z,_,Hijos),				
    member(X,Hijos),			
    member(Y,Hijos).			

%====================================================

tio_de(X, Y) :-                % X es tío de Y si:
    X \= Y,                    % X y Y son diferentes
    persona(X,hombre,_),		% si X es hombre
    persona(Z,_,Hijos),			% Z tiene Hijos
    member(Y,Hijos),			% Y hace parte de los Hijos de Z	
    hermano_de(X,Z).			% X y Z son hermanos, Osea que X es tio del hijo de su hermano, osea Y
    

tia_de(X, Y) :-               
    X \= Y,                    
    persona(X,mujer,_),
    persona(Z,_,Hijos),
    member(Y,Hijos),
    hermano_de(X,Z).

%====================================================

hijo_de(X, Y) :-               % X es hijo de Y si:
    X \= Y,                    % X y Y son diferentes
    persona(X,hombre,_),		%X es hombre
    persona(Y,_,Hijos),			% Y tiene Hijos
    member(X,Hijos).			% X hace parte de los Hijos de Y, Osea Y padre o madre de X

hija_de(X, Y) :-               
    X \= Y,
    persona(X,mujer,_),
    persona(Y,_,Hijos),
    member(X,Hijos).

%====================================================

% Una Forma de hacer esta Regla es preguntando si el Progenitor de X y el Progenitor de Y son hermanos, osea que X y Y son primos 
% Y asi no tenemos problemas de reversibilidad quee sucederia si usaramos tio_de u otras formas de hacerlo.

primo_de(X, Y) :-
    X \= Y,
    persona(ProgenitorX, _, HijosX), %ProgenitorX Tiene Hijos
    member(X, HijosX), 					% X hace parte de esos Hijos
    persona(ProgenitorY, _, HijosY),	%ProgenitorY Tiene Hijos
    member(Y, HijosY),					% Y hace parte de esos Hijos
    hermano_de(ProgenitorX, ProgenitorY), %ProgenitorX y ProgenitorY son Hermanos, osea que X y Y son primos.
    persona(X, hombre, _). %X es hombre.


prima_de(X, Y) :-
    X \= Y,
    persona(ProgenitorX, _, HijosX),
    member(X, HijosX),
    persona(ProgenitorY, _, HijosY),
    member(Y, HijosY),
    hermano_de(ProgenitorX, ProgenitorY),
    persona(X, mujer, _).
