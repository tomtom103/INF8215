include "globals.mzn";

int: n = 5;

array[1..n] of int: t_b = [2,2,3,2,1]; % top to bottom
array[1..n] of int: b_t = [3,2,1,3,4]; % bottom to top
array[1..n] of int: l_r = [4,1,3,2,3]; % left to right
array[1..n] of int: r_l = [1,4,2,2,2]; % right to left

array[1..n, 1..n] of var 1..n: x;      % hauteur des tours à chaque position

% Nombre de grandeurs differentes pour chaque ligne et colone
constraint forall([alldifferent([x[i, j] | j in 1..n]) | i in 1..n]);
constraint forall([alldifferent([x[i, j] | i in 1..n]) | j in 1..n]);

% Contrainte nombre de tours visibles
%% Gauche vers droite
constraint forall(
    [sum(
        [1 
        | j in 2..n where forall(
            [x[i, j] >= x[i, k] 
            | k in 1..j-1]
        )]
    ) + 1 = l_r[i] 
    | i in 1..n]
);
%% Droite vers gauche
constraint forall(
    [sum(
        [1 
        | j in 2..n where forall(
            [x[i, n - j + 1] >= x[i, n - k + 1] 
            | k in 1..j-1]
        )]
    ) + 1 = r_l[i] 
    | i in 1..n]
);
%% Top vers bottom
constraint forall(
    [sum(
        [1 
        | i in 2..n where forall(
            [x[i, j] >= x[k, j] 
            | k in 1..i-1]
        )]
    ) + 1 = t_b[j] 
    | j in 1..n]
);
%% Bottom vers top
constraint forall(
    [sum(
        [1 
        | i in 2..n where forall(
            [x[n - i + 1, j] >= x[n - k + 1, j] 
            | k in 1..i-1]
        )]
    ) + 1 = b_t[j] 
    | j in 1..n]
);

output 

["Configuration : \n"]

++

[ show(x[i,j]) ++ if j = n then "\n" else "," endif | i in 1..n, j in 1..n]
