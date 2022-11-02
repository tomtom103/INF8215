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
var int: profit = sum(
    [
        revenu[p] | p in finished
    ]
) - sum(
    [
        % Sum of travel costs between projects
        travel_costs[schedule[w, d], schedule[w, d + 1]] 
        | w in WORKER, d in 1..P-1
    ]
);

% Variables
var set of PROJECT: finished;

% Constraints

% Not more than 1 worker per project for the same project
constraint forall(
    [
        alldifferent(
            [
                schedule[w, d] 
                | w in WORKER
            ]
        ) 
        | d in 1..P
    ]
);

% Make sure that the day matrix has the values coming from the schedule
constraint forall(
    [
        day[w, schedule[w, d]] = d 
        | w in WORKER, d in 1..P
    ]
);

% A worker cannot work on the same project twice
constraint forall(
    [
        alldifferent(
            [
                day[w, p] 
                | p in PROJECT where day[w, p] > 0
            ]
        ) 
        | w in WORKER
    ]
);

% Projects are finished if a day is assigned for every worker
constraint forall(
    [
        day[w, p] > 0
        | w in WORKER, p in finished
    ]
);

% Finished projects must at least contain the projects that must be done
constraint finished == finished union project_must_be_done;

% Workers on the projects must respect the prescendence
constraint forall(
    [
        day[precedences[p, 1], p] < day[precedences[p, 2], p] /\ day[precedences[p, 2], p] < day[precedences[p, 3], p]
        | p in project_with_precedences intersect finished
    ]
);

solve maximize profit;

output

["Horaire : \n"] 
++
[if p = 1 then show(w) ++ ":" else "" endif ++ show(schedule[w,p]) ++ if p = P then "\n" else "," endif | w in WORKER, p in 1..P]
++
["-----------\n"]
++
["Profit : " ++ show(profit)]
