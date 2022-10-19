include "globals.mzn";

enum PROJECT;
enum WORKER = { ARCHI, ING, ELEC };

int: P; % nombre de jours (et de projets à choisir)

array[PROJECT, PROJECT] of int: travel_costs;     % Couts de deplacements entre projets

set of PROJECT: project_with_precedences;         % Ensemble des projets ayant des contraintes de précédences
array[PROJECT, 1..3] of WORKER: precedences;      % Précédences (pour les projets n'ayant pas de contraintes de précédences, ignorez la rangée)

set of PROJECT: project_must_be_done;             % Ensemble des projets qui DOIVENT êtres faits

array[PROJECT] of int: revenu;                    % Revenu des projets

array[WORKER, 1..P] of var PROJECT: schedule;     % Pour chaque employé, pour chaque jour, on assigne un projet
array[WORKER, PROJECT] of var 0..P: day;          % Pour chaque employé, pour chaque projet, on détermine le jour 

% Profit (gain - dépenses) a maximiser
var int: profit;

output

["Horaire : \n"] 
++
[if p = 1 then show(w) ++ ":" else "" endif ++ show(schedule[w,p]) ++ if p = P then "\n" else "," endif | w in WORKER, p in 1..P]
++
["-----------\n"]
++
["Profit : " ++ show(profit)]



