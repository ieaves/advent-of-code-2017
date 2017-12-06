"""
--- Day 5: A Maze of Twisty Trampolines, All Alike ---

An urgent interrupt arrives from the CPU: it's trapped in a maze of jump instructions, and it would like assistance from any programs with spare cycles to help find the exit.

The message includes a list of the offsets for each jump. Jumps are relative: -1 moves to the previous instruction, and 2 skips the next one. Start at the first instruction in the list. The goal is to follow the jumps until one leads outside the list.

In addition, these instructions are a little strange; after each jump, the offset of that instruction increases by 1. So, if you come across an offset of 3, you would move three instructions forward, but change it to a 4 for the next time it is encountered.

For example, consider the following list of jump offsets:

0
3
0
1
-3
Positive jumps ("forward") move downward; negative jumps move upward. For legibility in this example, these offset values will be written all on one line, with the current instruction marked in parentheses. The following steps would be taken before an exit is found:

(0) 3  0  1  -3  - before we have taken any steps.
(1) 3  0  1  -3  - jump with offset 0 (that is, don't jump at all). Fortunately, the instruction is then incremented to 1.
 2 (3) 0  1  -3  - step forward because of the instruction we just modified. The first instruction is incremented again, now to 2.
 2  4  0  1 (-3) - jump all the way to the end; leave a 4 behind.
 2 (4) 0  1  -2  - go back to where we just were; increment -3 to -2.
 2  5  0  1  -2  - jump 4 steps forward, escaping the maze.
In this example, the exit is reached in 5 steps.

How many steps does it take to reach the exit?

--- Part Two ---

Now, the jumps are even stranger: after each jump, if the offset was three or more, instead decrease it by 1. Otherwise, increase it by 1 as before.

Using this rule with the above example, the process now takes 10 steps, and the offset values after finding the exit are left as 2 3 2 3 -1.

How many steps does it now take to reach the exit?

"""


def line_reader(file):
    with open(file, 'r') as f:
        for line in f:
            res = [int(item) for item in line.strip().split()]
            assert len(res) == 1
            yield(res[0])


class maze_searcher():
    def __init__(self, instructions, instruction_updater):
        self.original_instructions = instructions
        self.instructions = [i for i in self.original_instructions]
        self.instruction_size = len(self.instructions)
        self.instruction_updater = instruction_updater

        self.step_count = 0
        self.current_location = 0
        self.escaped = False

    def step(self):
        if not self.escaped:
            step_size = self.instructions[self.current_location]
            self.instructions[self.current_location] = self.instruction_updater(step_size)
            self.current_location += step_size
            self.step_count += 1

        if self.current_location >= self.instruction_size:
            self.escaped = True

    def reset_maze(self):
        self.instructions = [i for i in self.original_instructions]
        self.escaped = False
        self.current_location = 0
        self.step_count = 0

    def escape_time(self):
        while not self.escaped:
            self.step()
        final_step_count = self.step_count
        final_instructions = self.instructions
        self.reset_maze()

        return([final_step_count, final_instructions])


def update_rules1(x):
    return(x + 1)


def update_rules2(x):
    return(x - 1 if x >= 3 else x + 1)


if __name__ == "__main__":
    instructions = list(line_reader('input.txt'))
    test_rules = [0, 3,  0,  1,  -3]
    test_searcher_1 = maze_searcher(test_rules, update_rules1)
    test_searcher_2 = maze_searcher(test_rules, update_rules2)

    assert test_searcher_1.escape_time()[0] == 5
    assert test_searcher_2.escape_time()[0] == 10
    assert test_searcher_2.escape_time()[1] == [2, 3, 2, 3, -1]

    searcher_1 = maze_searcher(instructions, update_rules1)
    searcher_2 = maze_searcher(instructions, update_rules2)

    escape_time_1 = searcher_1.escape_time()
    escape_time_2 = searcher_2.escape_time()

    print(escape_time_1[0])
    print(escape_time_2[0])
