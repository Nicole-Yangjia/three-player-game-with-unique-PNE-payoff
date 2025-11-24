
% strategies and players
s1(a1).
s1(a2).
s2(b1).
s2(b2).
s3(c1).
s3(c2).
player(1..3).

%Sigma G'
leq(I, X, Y, Z, X, Y, Z) :- s1(X), s2(Y), s3(Z), player(I).
 { leq(I, X1, Y1, Z1, X2, Y2, Z2) } :-
      s1(X1), s2(Y1), s3(Z1), 
      s1(X2), s2(Y2), s3(Z2), 
      player(I),
      X1 != X2; Y1 != Y2; Z1 != Z2.
:- not leq(I, X1, Y1, Z1, X2, Y2, Z2), not leq(I, X2, Y2, Z2, X1, Y1, Z1),
   s1(X1), s2(Y1), s3(Z1), 
   s1(X2), s2(Y2), s3(Z2), 
   player(I),
   X1 != X2; Y1 != Y2; Z1 != Z2.

leq(I, X1, Y1, Z1, X3, Y3, Z3) :- 
    leq(I, X1, Y1, Z1, X2, Y2, Z2), 
    leq(I, X2, Y2, Z2, X3, Y3, Z3),
    player(I).


%Omega'(a1,b1,c1) and Omega'(a2,b2,c2)
leq(2, X2, Y2, Z2, a1, b1, c1) :- not_leq(1, X1, Y1, Z1, a1, b1, c1), s1(X1), s2(Y1), s3(Z1), s1(X2), s2(Y2), s3(Z2).
leq(3, X3, Y3, Z3, a1, b1, c1) :- not_leq(1, X1, Y1, Z1, a1, b1, c1), s1(X1), s2(Y1), s3(Z1), s1(X3), s2(Y3), s3(Z3).
leq(1, X5, Y5, Z5, a1, b1, c1) :- not_leq(2, X4, Y4, Z4, a1, b1, c1), s1(X4), s2(Y4), s3(Z4), s1(X5), s2(Y5), s3(Z5).
leq(3, X6, Y6, Z6, a1, b1, c1) :- not_leq(2, X4, Y4, Z4, a1, b1, c1), s1(X4), s2(Y4), s3(Z4), s1(X6), s2(Y6), s3(Z6).
leq(1, X8, Y8, Z8, a1, b1, c1) :- not_leq(3, X7, Y7, Z7, a1, b1, c1), s1(X7), s2(Y7), s3(Z7), s1(X8), s2(Y8), s3(Z8).
leq(2, X9, Y9, Z9, a1, b1, c1) :- not_leq(3, X7, Y7, Z7, a1, b1, c1), s1(X7), s2(Y7), s3(Z7), s1(X9), s2(Y9), s3(Z9).
leq(2, X2, Y2, Z2, a2, b2, c2) :- not_leq(1, X1, Y1, Z1, a2, b2, c2), s1(X1), s2(Y1), s3(Z1), s1(X2), s2(Y2), s3(Z2).
leq(3, X3, Y3, Z3, a2, b2, c2) :- not_leq(1, X1, Y1, Z1, a2, b2, c2), s1(X1), s2(Y1), s3(Z1), s1(X3), s2(Y3), s3(Z3).
leq(1, X5, Y5, Z5, a2, b2, c2) :- not_leq(2, X4, Y4, Z4, a2, b2, c2), s1(X4), s2(Y4), s3(Z4), s1(X5), s2(Y5), s3(Z5).
leq(3, X6, Y6, Z6, a2, b2, c2) :- not_leq(2, X4, Y4, Z4, a2, b2, c2), s1(X4), s2(Y4), s3(Z4), s1(X6), s2(Y6), s3(Z6).
leq(1, X8, Y8, Z8, a2, b2, c2) :- not_leq(3, X7, Y7, Z7, a2, b2, c2), s1(X7), s2(Y7), s3(Z7), s1(X8), s2(Y8), s3(Z8).
leq(2, X9, Y9, Z9, a2, b2, c2) :- not_leq(3, X7, Y7, Z7, a2, b2, c2), s1(X7), s2(Y7), s3(Z7), s1(X9), s2(Y9), s3(Z9).



% PNE
ne(X,Y,Z) :- 
    leq(1, XE, Y, Z, X, Y, Z), 
    leq(2, X, YE, Z, X, Y, Z), 
    leq(3, X, Y, ZE, X, Y, Z),
    s1(XE), s2(YE), s3(ZE), s1(X), s2(Y), s3(Z).


sim(I, X1, Y1, Z1, X2, Y2, Z2) :- 
    leq(I, X1, Y1, Z1, X2, Y2, Z2), 
    leq(I, X2, Y2, Z2, X1, Y1, Z1).

% SIM'
ne(a1,b1,c1).
ne(a2,b2,c2).
:- sim(1,a1,b1,c1,a2,b2,c2), sim(2,a1,b1,c1,a2,b2,c2), sim(3,a1,b1,c1,a2,b2,c2).

%classical not 
not_leq(I,X,Y,Z,X1,Y1,Z1) :- not leq(I,X,Y,Z,X1,Y1,Z1), s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).
:- not_leq(I,X,Y,Z,X1,Y1,Z1), leq(I,X,Y,Z,X1,Y1,Z1), s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).
:- not not_leq(I,X,Y,Z,X1,Y1,Z1), not leq(I,X,Y,Z,X1,Y1,Z1), s1(X), s2(Y), s3(Z), s1(X1), s2(Y1), s3(Z1), player(I).
