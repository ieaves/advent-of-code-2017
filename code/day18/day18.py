"""
--- Day 18: Duet ---

You discover a tablet containing some strange assembly code labeled simply "Duet". Rather than bother the sound card with it, you decide to run the code yourself. Unfortunately, you don't see any documentation, so you're left to figure out what the instructions mean on your own.

It seems like the assembly is meant to operate on a set of registers that are each named with a single letter and that can each hold a single integer. You suppose each register should start with a value of 0.

There aren't that many instructions, so it shouldn't be hard to figure out what they do. Here's what you determine:

    snd X plays a sound with a frequency equal to the value of X.
    set X Y sets register X to the value of Y.
    add X Y increases register X by the value of Y.
    mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
    mod X Y sets register X to the remainder of dividing the value contained in register X by the value of Y (that is, it sets X to the result of X modulo Y).
    rcv X recovers the frequency of the last sound played, but only when the value of X is not zero. (If it is zero, the command does nothing.)
    jgz X Y jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)

Many of the instructions can take either a register (a single letter) or a number. The value of a register is the integer it contains; the value of a number is that number.

After each jump instruction, the program continues with the instruction to which the jump jumped. After any other instruction, the program continues with the next instruction. Continuing (or jumping) off either end of the program terminates it.

For example:

set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2

    The first four instructions set a to 1, add 2 to it, square it, and then set it to itself modulo 5, resulting in a value of 4.
    Then, a sound with frequency 4 (the value of a) is played.
    After that, a is set to 0, causing the subsequent rcv and jgz instructions to both be skipped (rcv because a is 0, and jgz because a is not greater than 0).
    Finally, a is set to 1, causing the next jgz instruction to activate, jumping back two instructions to another jump, which jumps again to the rcv, which ultimately triggers the recover operation.

At the time the recover operation is executed, the frequency of the last sound played is 4.

What is the value of the recovered frequency (the value of the most recently played sound) the first time a rcv instruction is executed with a non-zero value?

--- Part Two ---

As you congratulate yourself for a job well done, you notice that the documentation has been on the back of the tablet this entire time. While you actually got most of the instructions correct, there are a few key differences. This assembly code isn't about sound at all - it's meant to be run twice at the same time.

Each running copy of the program has its own set of registers and follows the code independently - in fact, the programs don't even necessarily run at the same speed. To coordinate, they use the send (snd) and receive (rcv) instructions:

    snd X sends the value of X to the other program. These values wait in a queue until that program is ready to receive them. Each program has its own message queue, so a program can never receive a message it sent.
    rcv X receives the next value and stores it in register X. If no values are in the queue, the program waits for a value to be sent to it. Programs do not continue to the next instruction until they have received a value. Values are received in the order they are sent.

Each program also has its own program ID (one 0 and the other 1); the register p should begin with this value.

For example:

snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d

Both programs begin by sending three values to the other. Program 0 sends 1, 2, 0; program 1 sends 1, 2, 1. Then, each program receives a value (both 1) and stores it in a, receives another value (both 2) and stores it in b, and then each receives the program ID of the other program (program 0 receives 1; program 1 receives 0) and stores it in c. Each program now sees a different value in its own copy of register c.

Finally, both programs try to rcv a fourth time, but no data is waiting for either of them, and they reach a deadlock. When this happens, both programs terminate.

It should be noted that it would be equally valid for the programs to run at different speeds; for example, program 0 might have sent all three values and then stopped at the first rcv before program 1 executed even its first instruction.

Once both of your programs have terminated (regardless of what caused them to do so), how many times did program 1 send a value?

"""
import string


class music_player():
    def __init__(self, instructions):
        self.instructions = list(instructions)
        self.current_instruction = 0
        self.registers = {}
        self.last_played_sound = None

    def snd(self, register, *args):
        self.last_played_sound = self.registers[register]

    def set(self, register, value):
        self.registers[register] = value

    def add(self, register, value):
        self.registers[register] += value

    def mul(self, register, value):
        self.registers[register] *= value

    def mod(self, register, value):
        self.registers[register] = self.registers[register] % value

    def rcv(self, register, *args):
        if self.registers[register] != 0:
            return self.last_played_sound

    def jgz(self, register, offset):
        if self.registers[register] != 0:
            self.current_instruction += (offset - 1)

    def play_instruction(self, instruc_type, register, value=None):
        self.registers.setdefault(register, 0)
        instruc_type, register, value = self.instructions[self.current_instruction]

        if isinstance(value, str):
            value = self.registers[value]

        if instruc_type == 'snd':
            ret = self.snd(register, value)
        elif instruc_type == 'set':
            ret = self.set(register, value)
        elif instruc_type == 'add':
            ret = self.add(register, value)
        elif instruc_type == 'mul':
            ret = self.mul(register, value)
        elif instruc_type == 'mod':
            ret = self.mod(register, value)
        elif instruc_type == 'rcv':
            ret = self.rcv(register, value)
        elif instruc_type == 'jgz':
            ret = self.jgz(register, value)

        return(ret)

    def reset(self):
        self.current_instruction = 0
        self.registers = {}
        self.last_played_sound = None

    def play_instructions(self):

        while self.current_instruction < len(self.instructions):
            instruc_type, register, value = self.instructions[self.current_instruction]
            ret = self.play_instruction(instruc_type, register, value)
            if ret:
                break
            self.current_instruction += 1

        self.reset()
        return(ret)


class player():
    def __init__(self, instructions, prog_id):
        self.instructions = list(instructions)
        self.current_instruction = 0
        self.received_messages = []
        self.registers = {'p': prog_id}
        self.deadlocked = False
        self.finished_playing = False

    def snd(self, register, value=None):
        self.current_instruction += 1
        ret = self.registers[register] if isinstance(register, str) else register
        return ret

    def set(self, register, value):
        value = self.registers[value] if isinstance(value, str) else value
        self.registers[register] = value
        self.current_instruction += 1

    def add(self, register, value):
        value = self.registers[value] if isinstance(value, str) else value
        self.registers[register] += value
        self.current_instruction += 1

    def mul(self, register, value):
        value = self.registers[value] if isinstance(value, str) else value
        self.registers[register] *= value
        self.current_instruction += 1

    def mod(self, register, value):
        value = self.registers[value] if isinstance(value, str) else value
        self.registers[register] = self.registers[register] % value
        self.current_instruction += 1

    def rcv(self, register, *args):
        if self.received_messages:
            self.registers[register] = self.received_messages.pop(0)
            self.current_instruction += 1
            self.deadlocked = False
        else:
            self.deadlocked = True

    def jgz(self, value, offset):
        offset = self.registers[offset] if isinstance(offset, str) else offset
        value = self.registers[value] if isinstance(value, str) else value
        if value > 0:
            self.current_instruction += offset
        else:
            self.current_instruction += 1

    def play_instruction(self):
        if self.finished_playing:
            return

        instruc_type, register, value = self.instructions[self.current_instruction]
        if isinstance(register, str):
            self.registers.setdefault(register, 0)

        if instruc_type == 'snd':
            ret = self.snd(register, value)
        elif instruc_type == 'set':
            ret = self.set(register, value)
        elif instruc_type == 'add':
            ret = self.add(register, value)
        elif instruc_type == 'mul':
            ret = self.mul(register, value)
        elif instruc_type == 'mod':
            ret = self.mod(register, value)
        elif instruc_type == 'rcv':
            ret = self.rcv(register, value)
        elif instruc_type == 'jgz':
            ret = self.jgz(register, value)

        if self.current_instruction >= len(self.instructions) or self.current_instruction < 0:
            self.finished_playing = True

        return(ret)


class duet_player():
    def __init__(self, instructions):
        self.instructions = list(instructions)
        self.players = [player(self.instructions, i) for i in range(2)]

    def play_instructions(self):
        finished = False
        counter = 0
        while not finished:
            for i, player in enumerate(self.players):
                ret = player.play_instruction()
                if ret is not None:
                    self.players[(i + 1) % len(self.players)].received_messages.append(ret)
                    counter += 1 if i == 1 else 0

            finished = all((player.deadlocked or player.finished_playing) for player in self.players)
        return(counter)


def process_instructions(file):
    possible_registers = set(list(string.ascii_lowercase))
    with open(file, 'r') as f:
        for line in f.readlines():
            instruction = [i for i in line.strip().split()]

            assert len(instruction) <= 3
            if len(instruction) < 3:
                instruction.append(None)
            elif instruction[2] not in possible_registers:
                instruction[2] = int(instruction[2])

            if instruction[1] not in possible_registers:
                instruction[1] = int(instruction[1])
            yield instruction


if __name__ == "__main__":
    test_instructions = list(process_instructions('test_input.txt'))
    test_instructions2 = list(process_instructions('test_input2.txt'))
    instructions = list(process_instructions('input.txt'))

    assert music_player(test_instructions).play_instructions() == 4
    assert duet_player(test_instructions2).play_instructions() == 3

    music = music_player(instructions)
    first_sound = music.play_instructions()
    print(first_sound)

    duet = duet_player(instructions)
    sent_instructions = duet.play_instructions()
    print(sent_instructions)
