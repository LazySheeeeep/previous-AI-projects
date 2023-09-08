def max_turn_now(state: list[list[int]]) -> bool:
    """
    Tells whether it's max's turn now.
    Depending on the current state.
    """
    return sum([sum(i) for i in state]) == 0


def all_actions_of(state: list[list[int]]) -> list[tuple[int, int]]:
    """
    Gets all legal actions from the state by checking if it's 0.
    """
    actions = []
    for x, row in enumerate(state):
        for y, col in enumerate(row):
            if col == 0:
                actions.append((x, y))
    return actions


def result(state: list[list[int]], action: tuple[int, int], max_turn=True) -> list[list[int]]:
    """
    Returns the result after the action taken in the state.
    """
    x, y = action
    if max_turn:
        state[x][y] = 1
    else:
        state[x][y] = -1
    return state


def erase(state: list[list[int]], action: tuple[int, int]) -> None:
    """
    undo the action.
    """
    state[action[0]][action[1]] = 0


def is_terminal(state: list[list[int]]) -> bool:
    """
    Tells whether the state is a terminal state. 
    """
    # in a row
    if any([abs(sum(row)) == 3 for row in state]):
        return True

    # in a column
    elif any([abs(sum([row[i] for row in state])) == 3 for i in range(3)]):
        return True

    # diagonal
    elif abs(sum([state[i][i] for i in range(3)])) == 3 or abs(sum([state[-i - 1][i] for i in range(3)])) == 3:
        return True

    # calculate the amount of 0. A terminal state has no 0 or one 0.
    return sum([i == 0 for row in state for i in row]) == 1 or 0


def score(state: list[list[int]]) -> float:
    """
    If max player wins, he scores 1 point. While in the flip side, min player wins would score -1 point.
    If there's a draw the score would be 0.
    """
    # in a row or in a column
    three_sums = set([sum(row) for row in state]) | set([sum([row[i] for row in state]) for i in range(3)])

    # in a diagonal line
    three_sums.add(sum([state[i][i] for i in range(3)]))
    three_sums.add(sum([state[-i - 1][i] for i in range(3)]))

    if 3 in three_sums:
        # player max win
        return 1
    elif -3 in three_sums:
        # player min win
        return -1
    # if there's only one place left, the player have no other choice, let's help him
    elif sum([i == 0 for row in state for i in row]) == 1:
        action = all_actions_of(state)[0]
        result(state, action, max_turn=max_turn_now(state))
        point = score(state)
        erase(state, action)  # remember to undo the action
        return point
    else:
        return 0


def min_value(state: list[list[int]],
              former_max_of_peers: tuple[float, tuple[int, int] | None])\
        -> tuple[float, tuple[int, int] | None]:
    """
    Returns the optimum action which taken by the current state and the minimum value caused
    """
    if is_terminal(state):
        # terminal state has no actions
        return score(state), None

    # the first max-child has no former actions, later it would be the first outcome
    min_of_max_child = (100, None)

    for action in all_actions_of(state):
        # gets value from every children by applying action
        current_value, _ = max_value(result(state, action, max_turn=False), min_of_max_child)
        # undo the action, restore the state
        erase(state, action)
        # undermine each step's weight, so that it weights more when the terminal state is closer to current state.
        current_value *= 0.8
        if current_value <= former_max_of_peers[0]:
            """
            then this min-node would choose a number no bigger than the former maximum value of peers,
            which means the parent max-node shouldn't consider it anymore.
            """
            return former_max_of_peers  # Beta pruning

        # Keeps the minimum value of all max-children
        if min_of_max_child[0] > current_value:
            min_of_max_child = (current_value, action)

    return min_of_max_child


def max_value(state: list[list[int]],
              former_min_of_peers: tuple[float, tuple[int, int] | None])\
        -> tuple[float, tuple[int, int] | None]:
    """
    Returns the optimum action which taken by the current state and the maximum value caused
    """
    if is_terminal(state):
        return score(state), None

    # the first min-child has no former actions, later it would be the first outcome
    max_of_min_child = (-100, None)

    for action in all_actions_of(state):
        current_value, _ = min_value(result(state, action), max_of_min_child)
        erase(state, action)
        current_value *= 0.8
        if current_value >= former_min_of_peers[0]:
            """
            then this max-node would take a number no less than the former minimum value of peers,
            which means the parent min-node would ignore it.
            """
            return former_min_of_peers  # Alpha pruning

        # Keeps the maximum value of all min-children
        if max_of_min_child[0] < current_value:
            max_of_min_child = (current_value, action)

    return max_of_min_child


def display_board(bd: list[list[int]]) -> None:
    print()
    for row in bd:
        for i in row:
            if i == 0:
                print('*', end='')
            elif i == 1:
                print('X', end='')
            elif i == -1:
                print('O', end='')
        print()
    print()


def get_action() -> tuple[int, int]:
    """
    Gets action from input
    """
    text = input('text down the coordinate:')
    nums = text.split(',')
    return int(nums[0]), int(nums[1])


def finish(state: list[list[int]]) -> None:
    """
    tells who are the winner or it's a draw
    """
    point = score(state)
    if point == 1:
        print('you win!')
    elif point == -1:
        print('ai win!')
    else:
        print('draw!')


if __name__ == '__main__':
    board = []
    for _ in range(3):
        board.append([0] * 3)
    while True:
        display_board(board)
        # human player(the max-player)goes first
        if is_terminal(board) or is_terminal(result(board, get_action())):
            finish(board)
            break
        value_num, ai_action = min_value(board, (-100., None))
        if value_num < 0:
            print('you will lose!')
        elif value_num == 0:
            print("probably it's a draw")
        result(board, ai_action, max_turn=False)
