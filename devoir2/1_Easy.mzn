include "globals.mzn";

enum ATTRACTION;

% Il faut sélectionner entre l et u attractions
int: l;
int: u;

% Attrait touristique total minimum
int: m;

% Attrait touristique par paire d'attraction
array[ATTRACTION, ATTRACTION] of int: pair_attraction;

% Coût de construction par attraction
array[ATTRACTION] of int: cost;

% Ensemble d'attractions à construire
var set of ATTRACTION: x;

% Coût total
var int: tot_cost = sum([cost[i] | i in x]);

% Constaints
constraint card(x) >= l /\ card(x) <= u;

constraint sum([pair_attraction[i, j] | i, j in x where i < j]) >= m;

solve minimize tot_cost;

output [
  "Attractions : ", show(x), "\n",
  "Cost : ", show(tot_cost)
];
