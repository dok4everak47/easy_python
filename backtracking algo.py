from TreeNode import TreeNode


class backtracking():

    def __init__(self):
        pass

    def is_solution(state: list[TreeNode]) -> bool:
        return state and state[-1].val == 7

    def record_solution(state: list[TreeNode], res: list[list[TreeNode]]):
        res.append(list(state))

    def is_valid(state: list[TreeNode], choice: TreeNode) -> bool:
        return choice is not None and choice.val != 3

    def make_choice(state: list[TreeNode], choice: TreeNode):
        state.append(choice)

    def undo_choice(state: list[TreeNode], choice: TreeNode):
        state.pop()

    def backtrack(state: list[TreeNode], choices: list[TreeNode],
                  res: list[list[TreeNode]]):
        if is_solution(state):
            record_solution(state, res)

        for choice in choices:
            if is_valid(state, choice):
                make_choice(state, choice)

                backtrack(state, [choice.left, choice, right], res)

                undo_choice(state, choice)
