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

Action = Tuple[int, int, int, int] 

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
        player: Agent, 
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

        next_action = self.alpha_beta_search(board, self.cutoff, self.heuristic)[1]
        print("Action played: ", next_action)
        return next_action

    def cutoff(self, depth: int) -> bool:
        return depth > 1

    def heuristic(self, board: Board) -> int:
        # isolation_score = self._iso_score(board)
        isolation_score = 0
        return isolation_score + board.get_score()

    def _iso_score(self, board: Board) -> int:
        score = 0
        for action in board.get_actions():
            if board.is_action_valid(action):
                i, j, _, _ = action
                neighbors = list(board.get_tower_actions(i, j))
                N = len(neighbors)
                if N % 2 == 0:
                    continue
                ours = 0
                theirs = 0
                for neighbor in neighbors:
                    _, _, k, l = neighbor
                    if board.m[k][l] > 0:
                        theirs += 1
                    elif board.m[k][l] < 0:
                        ours += 1
                
                if ours > theirs:
                    score += 1 / N
                else:
                    score -= 1 / N
        return score
                    

    def alpha_beta_search(
        self,
        board: Board,
        cutoff: Callable[[int], bool],
        heuristic: Callable[[Board], int]
    ) -> Tuple[int, Action]:
        def max_value(
            board: Board,
            alpha: float,
            beta: float,
            depth: int,
            # action: Optional[Action] = None
        ) -> Tuple[int, Optional[Action]]:
            if cutoff(depth):
                return (heuristic(board), None)
            if board.is_finished():
                return (board.get_score(), None)


            v_star = -math.inf
            m_star = None

            for action in board.get_actions():
                _board = board.clone()
                v_child = min_value(_board, alpha, beta, depth + 1)[0]
                if v_child > v_star:
                    v_star = v_child
                    m_star = action
                    alpha = max(alpha, v_star)
                if v_star >= beta:
                    break
            return (v_star, m_star)

        def min_value(
            board: Board,
            alpha: float,
            beta: float,
            depth: int,
            # action: Optional[Action] = None
        ) -> Tuple[int, Optional[Action]]:
            if cutoff(depth):
                return (heuristic(board), None)
            if board.is_finished():
                return (board.get_score(), None)

            
            v_star = math.inf
            m_star = None

            for action in board.get_actions():
                _board = board.clone()
                v_child = max_value(_board, alpha, beta, depth + 1)[0]
                if v_child < v_star:
                    v_star = v_child
                    m_star = action
                    beta = min(beta, v_star)
                if v_star <= alpha:
                    break
            return (v_star, m_star)
        return max_value(board, -math.inf, math.inf, 0)

if __name__ == "__main__":
    agent_main(MinMaxAgent())

