include "globals.mzn";

int: n = 5;

array[1..n] of int: t_b = [2,2,3,2,1]; % top to bottom
array[1..n] of int: b_t = [3,2,1,3,4]; % bottom to top
array[1..n] of int: l_r = [4,1,3,2,3]; % left to right
array[1..n] of int: r_l = [1,4,2,2,2]; % right to left

array[1..n, 1..n] of var 1..n: x;      % hauteur des tours à chaque position

output 

["Configuration : \n"]

++

[ show(x[i,j]) ++ if j = n then "\n" else "," endif | i in 1..n, j in 1..n]
