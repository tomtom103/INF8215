#!/usr/bin/env python3
"""
Avalam agent.
Copyright (C) 2022, <<<<<<<<<<< YOUR NAMES HERE >>>>>>>>>>>
Polytechnique Montréal

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
import math
from avalam import *
from typing import Callable, Tuple, List, Optional
import numpy as np

Action = Tuple[int, int, int, int]

def euclidian_distance(x1: int, x2: int, y1: int, y2: int) -> int:
    return round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


def player_scores(board: Board, player: int) -> Tuple[int, int]:
    my_score = 0
    other_score = 0
    flat_arr = [item for sublist in board.m for item in sublist if item != 0]
    for value in flat_arr:
        if value * player > 0:
            my_score += abs(value)
        else:
            other_score += abs(value)
    return (my_score, other_score)

class MinMaxAgent(Agent):

    """Agent implementing a basic min-max algorithm."""

    def initialize(
        self, 
        percepts: List[List[int]], 
        players: List[Agent], 
        time_left: Optional[float] = None
    ) -> None:
        """Begin a new game.
        The computation done here also counts in the time credit.
        Arguments:
        percepts -- the initial board in a form that can be fed to the Board
            constructor.
        players -- sequence of players this agent controls
        time_left -- a float giving the number of seconds left from the time
            credit for this agent (all players taken together). If the game is
            not time-limited, time_left is None.
        """
        pass

    def play(
        self, 
        percepts: List[List[int]], 
        player: int, 
        step: int, 
        time_left: Optional[float] = None
    ) -> Action:
        """
        This function is used to play a move according
        to the percepts, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        :param percepts: dictionary representing the current board
            in a form that can be fed to `dict_to_board()` in avalam.py.
        :param player: the player to control in this step (-1 or 1)
        :param step: the current step number, starting from 1
        :param time_left: a float giving the number of seconds left from the time
            credit. If the game is not time-limited, time_left is None.
        :return: an action
            eg; (1, 4, 1 , 3) to move tower on cell (1,4) to cell (1,3)
        """
        print("percept:", percepts)
        print("player:", player)
        print("step:", step)
        print("time left:", time_left if time_left else '+inf')

        board = dict_to_board(percepts)
        print("Board: ", board)

        next_action = self.alpha_beta_search(board, player, time_left, self.cutoff, self.heuristic)[1]
        print("Action played: ", next_action)
        return next_action

    def cutoff(self, depth: int, board: Board, player: int, time_left: Optional[float]) -> bool:
        if time_left is not None and time_left == 0:
            return True
        return depth > 2


    def heuristic(self, board: Board, player: int) -> int:
        return self._pairs_heuristic(board, player)

    def _pairs_heuristic(self, board: Board, player: int) -> int:
        score = 0
        
        clone = board.clone()
        for action in clone.get_actions():
            #getting the score
            if not clone.is_action_valid(action):
                continue
            temp = clone.play_action(action)
            _, pre_score = player_scores(clone, player)
            _, next_score = player_scores(temp, player)
            if abs(next_score) - abs(pre_score) < 0:
                score += 5

            
            x, y, dx, dy = action
            origin, dest = clone.m[x][y], clone.m[dx][dy]

            # Enemy has tower of 4 and we want to top it off
            if origin * dest == -4 and origin == player:
                return 10000
            # Complete our own tower if possible (save our own tower) (dont return)
            elif origin * dest == 4 and origin == player:
                score += 50
            
            # 2v3
            if origin * dest == -6 and origin == 2*player:
                score += 40
            elif origin * dest == 6 and origin == 2*player :
                score += 35

             # 3v2
            if origin * dest == -6 and origin == 3*player:
                score += 40
            elif origin * dest == 6 and origin == 3*player :
                score += 35

            
            # if (origin * player < 0) and (dest * player < 0):
            #     score += 5
            #     if abs(origin) + abs(dest) == 2:
            #         score += 30
            #         distance = euclidian_distance(dx, 5, dy, 5)
            #         # Group furthest towers together
            #         score += distance ** 100
            #     elif 3 <= abs(origin) + abs(dest) < 5:
            #         score += 100

        return score

    def _has_remaining_pairs(self, board: Board, player: int) -> bool:
        clone = board.clone()
        for action in clone.get_actions():
            if not clone.is_action_valid(action):
                continue
            x, y, dx, dy = action
            origin, dest = clone.m[x][y], clone.m[dx][dy]
            if (
                origin * player < 0 and 
                dest * player < 0 and 
                (abs(origin) + abs(dest)) == 2
            ):
                return True
        return False

    def alpha_beta_search(
        self,
        board: Board,
        player: int,
        time_left: Optional[float],
        cutoff: Callable[[int], bool],
        heuristic: Callable[[Board], int]
    ) -> Tuple[int, Action]:
        def max_value(
            board: Board,
            player: int,
            time_left: Optional[float],
            alpha: float,
            beta: float,
            depth: int,
            # action: Optional[Action] = None
        ) -> Tuple[int, Optional[Action]]:
            if cutoff(depth, board, player, time_left):
                return (heuristic(board, player), None)
            if board.is_finished():
                return (board.get_score(), None)


            v_star = -math.inf
            m_star = None

            for action in board.get_actions():
                if not board.is_action_valid(action):
                    continue
                _board = board.clone()
                v_child = min_value(_board, player, time_left, alpha, beta, depth + 1)[0]
                if v_child > v_star:
                    v_star = v_child
                    m_star = action
                    alpha = max(alpha, v_star)
                if v_star >= beta:
                    break
            return (v_star, m_star)

        def min_value(
            board: Board,
            player: int,
            time_left: Optional[float],
            alpha: float,
            beta: float,
            depth: int,
            # action: Optional[Action] = None
        ) -> Tuple[int, Optional[Action]]:
            if cutoff(depth, board, player, time_left):
                return (heuristic(board, player), None)
            if board.is_finished():
                return (board.get_score(), None)

            
            v_star = math.inf
            m_star = None

            for action in board.get_actions():
                if not board.is_action_valid(action):
                    continue
                _board = board.clone()
                v_child = max_value(_board, player, time_left, alpha, beta, depth + 1)[0]
                if v_child < v_star:
                    v_star = v_child
                    m_star = action
                    beta = min(beta, v_star)
                if v_star <= alpha:
                    break
            return (v_star, m_star)
        return max_value(board, player, time_left, -math.inf, math.inf, 0)

if __name__ == "__main__":
    agent_main(MinMaxAgent())

