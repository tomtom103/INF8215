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
import random


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
        print("player:", player)
        print("step:", step)
        print("time left:", time_left if time_left else '+inf')

        board = dict_to_board(percepts)

        next_action = self.alpha_beta_search(board, player, time_left, self.cutoff, self.heuristic)[1]
        print("Action played: ", next_action)
        return next_action
    

    def cutoff(self, depth: int, time_left: Optional[float]) -> bool:
        if time_left is not None and time_left == 0:
            return True
        return depth == 0
    

    def _compute_tower_score(self, origin: int, dest: int, player: int) -> int:        
        score = 0

        #1v4
        if origin * dest == -4 and origin == player:
            return 160
        # Complete our own tower if possible (save our own tower) 
        elif origin * dest == 4 and origin == player:
            return 150
        
        #4v1
        if origin * dest == -4 and origin == 4*player:
            return 160
        # Complete our own tower if possible (save our own tower) 
        elif origin * dest == 4 and origin == 4*player:
            return 150

        # 2v3
        if origin * dest == -6 and origin == 2*player:
            return 140
        elif origin * dest == 6 and origin == 2*player :
            return 135

        # 3v2
        if origin * dest == -6 and origin == 3*player:
            return 140
        elif origin * dest == 6 and origin == 3*player :
            return 135

        return score

    def _make_pairs(self, origin: int, dest: int, player: int) :
        score = 0

        #randomly choose between making our pairs or opponents pairs
        p = random.random()

        if p >=0.9 and (origin*dest == 1 and origin == player) : # our pairs
            score += 20
        elif p <= 0.85 and (origin*dest == 1 and origin != player): #opps pairs
            score += 20
        
        return score

    def _stack_pairs(self, origin: int, dest: int, player: int) :
        score = 0

        if  (origin*dest == 4 and origin == -2*player) : 
            score += 15
        
        return score
        
    def heuristic(self, board: Board, player: int, action : Action, depth: int) -> int :
        score = 0

        #Get the score for the board
        score = board.get_score()

        clone = board.clone()
        x, y, dx, dy = action
        origin, dest = clone.m[x][y], clone.m[dx][dy]

        #Get score for making a tower
        score += self._compute_tower_score(origin,dest,player)

        #making pairs when possible
        score += self._make_pairs(origin,dest,player)

        #stack opps pairs
        score += self._stack_pairs(origin,dest,player)

        # Depth represents depth left to recurse into
        # The smaller it is, the deeper we are.
        # We add a 0.001 bonus to signify that higher score
        # in less turns is more valuable
        score *= (1 + 0.001 * depth)

        return score * player
    

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
            action: Action
        ) -> Tuple[int, Optional[Action]]:
            if cutoff(depth, time_left):
                return (heuristic(board, player, action, depth), None)
            if board.is_finished():
                return (board.get_score(), None)

            v_star = -math.inf
            m_star = None

            for action in board.get_actions():
                v_child = min_value(board.clone().play_action(action), player, time_left, alpha, beta, depth - 1, action)[0]
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
            action : Action
        ) -> Tuple[int, Optional[Action]]:
            if cutoff(depth, time_left):
                return (heuristic(board, player, action, depth), None)
            if board.is_finished():
                return (board.get_score(), None)
            
            v_star = math.inf
            m_star = None

            for action in board.get_actions():
                v_child = max_value(board.clone().play_action(action), player, time_left, alpha, beta, depth - 1, action)[0]
                if v_child < v_star:
                    v_star = v_child
                    m_star = action
                    beta = min(beta, v_star)
                if v_star <= alpha:
                    break
            return (v_star, m_star)

        
        return max_value(board, player, time_left, -math.inf, math.inf, 4, [0,2,0,3])
    

if __name__ == "__main__":
    agent_main(MinMaxAgent())

