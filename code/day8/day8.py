"""
--- Day 8: I Heard You Like Registers ---

You receive a signal directly from the CPU. Because of your recent assistance with jump instructions, it would like you to compute the result of a series of unusual register instructions.

Each instruction consists of several parts: the register to modify, whether to increase or decrease that register's value, the amount by which to increase or decrease it, and a condition. If the condition fails, skip the instruction without modifying the register. The registers all start at 0. The instructions look like this:

b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10

These instructions would be processed as follows:

    Because a starts at 0, it is not greater than 1, and so b is not modified.
    a is increased by 1 (to 1) because b is less than 5 (it is 0).
    c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
    c is increased by -20 (to -10) because c is equal to 10.

After this process, the largest value in any register is 1.

You might also encounter <= (less than or equal to) or != (not equal to). However, the CPU doesn't have the bandwidth to tell you what all the registers are named, and leaves that to you to determine.

What is the largest value in any register after completing the instructions in your puzzle input?

--- Part Two ---

To be safe, the CPU also needs to know the highest value held in any register during this process so that it can decide how much
memory to allocate to these operations. For example, in the above instructions, the highest value ever held was 10
(in register c after the third instruction was evaluated).

"""


def line_reader(file):
    action_map = {'inc': lambda x, y: x + y, 'dec': lambda x, y: x - y}
    with open(file, 'r') as f:
        for line in f:
            vals = line.strip().split()
            ret = {'register': vals[0], 'action': action_map[vals[1]], 'action_amt': int(vals[2]),
                   'cond_register': vals[4], 'condition': vals[5], 'cond_amt': int(vals[6])}
            yield(ret)


def eval_conditional(a, b, condition):
    cond_string = " ".join(['True if a', condition, 'b else False'])
    return(eval(cond_string))


def evaluate_instructions(instructions):
    values = {}
    abs_max_val = 0
    for instruction in instructions:
        reg1 = instruction['register']

        values.setdefault(reg1, 0)
        values.setdefault(instruction['cond_register'], 0)

        if eval_conditional(values[instruction['cond_register']], instruction['cond_amt'], instruction['condition']):
            values[reg1] = instruction['action'](values[reg1], instruction['action_amt'])
            abs_max_val = values[reg1] if values[reg1] > abs_max_val else abs_max_val

    final_max_val = max(values.values())
    return((final_max_val, abs_max_val))


if __name__ == "__main__":
    import timeit
    assert evaluate_instructions(line_reader('test_input.txt'))[0] == 1
    assert evaluate_instructions(line_reader('test_input.txt'))[1] == 10

    print(evaluate_instructions(line_reader('input.txt')))
