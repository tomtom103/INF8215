include "globals.mzn";

var int: nombre = chiffres[1]*1000 + chiffres[2]*100 + chiffres[3]*10 + chiffres[4];
array[1..4] of var 1..9: chiffres;

% Containtes
constraint chiffres[4] mod 2 = 0;
constraint alldifferent(chiffres);
constraint chiffres[1] > chiffres[2];
constraint chiffres[3] < chiffres[4];
constraint chiffres[2] > chiffres[4];
constraint chiffres[4] + chiffres[3] + chiffres[2] + chiffres[1] > 15;

% Solver
solve minimize chiffres[3] * chiffres[2] * chiffres[1];

output [
  show(nombre)
];

% Result
% chiffres = [6, 5, 1, 4]
% nombre = 6514

