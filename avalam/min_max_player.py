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
from typing import Tuple, List, Optional

Action = Tuple[int, int, int, int]

def max_value(
    board: Board,
    depth: int,
) -> Tuple[int, Optional[Action]]:
    if board.is_finished():
        return (board.get_score(),None)

    if depth > 1:
        return (board.get_score(), None)
    
    v_star = math.inf
    m_star = None

    for action in board.get_actions():
        _board = board.clone()
        v_child, action_child = min_value(_board, depth + 1)
        if v_child > v_star and action_child is not None:
            v_star = v_child
            m_star = action
    return (v_star, m_star)

def min_value(
    board: Board,
    depth: int,
) -> Tuple[int, Optional[Action]]:
    if board.is_finished():
        return (board.get_score(), None)

    if depth > 2:
        return (board.get_score(), None)
    
    v_star = -math.inf
    m_star = None

    for action in board.get_actions():
        _board = board.clone()
        v_child, action_child = max_value(_board, depth + 1)
        if v_child < v_star and action_child is not None:
            v_star = v_child
            m_star = action
    return (v_star, m_star) 

class MinMaxAgent(Agent):

    """Agent implementing a basic min-max algorithm."""

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
        board = dict_to_board(percepts)

        next_action = max_value(board, 0)[1]
        print("Action played: ", next_action)
        return max_value(board, 0)[1]


if __name__ == "__main__":
    agent_main(MinMaxAgent())
