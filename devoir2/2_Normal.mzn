include "globals.mzn";

% Nombre de segments horizontaux et verticaux
int: h; % nb de rows
int: v; % nb de cols

% La demande par segment horizontal et vertical
array[1..h] of int: demand_per_h;
array[1..v] of int: demand_per_v;

% Le coût du permis et de construction de maison associé à chaque carré
array[1..h, 1..v] of int: cost_per_house;
array[1..h, 1..v] of int: cost_per_permit;

% Le nombre max de maison qui peut être construit par carré
int: m;

% Le nombre de maisons à construire par carré
array[1..h, 1..v] of var int: x;

% Le coût total
var int: tot_cost;

%% Constraints

% Il ne doit pas avoir plus de m maisons dans une meme case
constraint forall([x[horiz, vert] <= m | horiz in 1..h, vert in 1..v]);

% Il ne faut pas depasser la demande pour chaque ligne
constraint forall([sum([x[horiz, vert] | vert in 1..v]) >= demand_per_h[horiz] | horiz in 1..h]);
constraint forall([sum([x[horiz, vert] | horiz in 1..h]) >= demand_per_v[vert] | vert in 1..v]);

constraint tot_cost = sum(
  [
  if x[horiz, vert] > 0 then 
    cost_per_permit[horiz, vert] + x[horiz, vert] * cost_per_house[horiz, vert] 
  else 0 
  endif 
  | horiz in 1..h, vert in 1..v
  ]
);

%% Solve

solve minimize tot_cost;

output
  
  ["Configuration : \n"]  
  
  ++
  
  [
    show(x[i,j]) ++ if j = v then "\n" else "," endif 
    | i in 1..h, j in 1..v
  ]
  
  ++
  
  ["----------------\n"]
  
  ++
  
  [
  "Cost : " ++ show(tot_cost)
  ]
  