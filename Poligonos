conectados(segmento(_,P2S1), segmento(P2S1,_)).

poligono([S1,S2]) :- conectados(S1,S2), !. % es un poligono si dos segmentos estan conectados 


poligono([S1,S2|Tail]) :-  % es un poligono si 2 o mas segmentos estan conectados entre ellos, uno detras de otro 
    conectados(S1,S2),
    append([S2], Tail, Laux),
    poligono(Laux).

% Verifica que todos los segmentos estén conectados en secuencia
poligono_cerrado([_]).
poligono_cerrado([S1, S2 | Resto]) :-
    conectados(S1, S2),
    poligono_cerrado([S2 | Resto]).

figura_cerrada([Primer | _] = Lista) :-
    last(Lista, Ultimo),
    conectados(Ultimo, Primer).


triangulo(Lsegs) :-
    proper_length(Lsegs, 3),
    poligono_cerrado(Lsegs).

alternan_horizontal_vertical([S1, S2, S3, S4]) :-
    es_horizontal(S1),
    es_vertical(S2),
    es_horizontal(S3),
    es_vertical(S4);
    es_vertical(S1),
    es_horizontal(S2),
    es_vertical(S3),
    es_horizontal(S4).


es_horizontal(segmento((X1,Y),(X2,Y))) :- X1 \= X2.
es_vertical(segmento((X,Y1),(X,Y2))) :- Y1 \= Y2.

longitud(segmento((X1,Y1),(X2,Y2)), L) :-
    DX is X2 - X1,
    DY is Y2 - Y1,
    L is sqrt(DX*DX + DY*DY).

% Regla general para cuadrado:
cuadrado([S1, S2, S3, S4]) :-
    poligono_cerrado([S1, S2, S3, S4]),
    figura_cerrada([S1, S2, S3, S4]),
    longitud(S1, L),
    longitud(S2, L),
    longitud(S3, L),
    longitud(S4, L),
    alternan_horizontal_vertical([S1, S2, S3, S4]).

rectangulo(Segs) :-
    poligono_cerrado(Segs),
    figura_cerrada(Segs),
    alternan_horizontal_vertical(Segs),
    \+ cuadrado(Segs).
