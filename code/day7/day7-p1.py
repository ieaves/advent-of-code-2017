"""
--- Day 7: Recursive Circus ---

Wandering further through the circuits of the computer, you come upon a tower of programs that have gotten themselves into a bit of trouble. A recursive algorithm has gotten out of hand, and now they're balanced precariously in a large tower.

One program at the bottom supports the entire tower. It's holding a large disc, and on the disc are balanced several more sub-towers. At the bottom of these sub-towers, standing on the bottom disc, are other programs, each holding their own disc, and so on. At the very tops of these sub-sub-sub-...-towers, many programs stand simply keeping the disc below them balanced but with no disc of their own.

You offer to help, but first you need to understand the structure of these towers. You ask each program to yell out their name, their weight, and (if they're holding a disc) the names of the programs immediately above them balancing on that disc. You write this information down (your puzzle input). Unfortunately, in their panic, they don't do this in an orderly fashion; by the time you're done, you're not sure which program gave which information.

For example, if your list is the following:

pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
...then you would be able to recreate the structure of the towers that looks like this:

                gyxo
              /
         ugml - ebii
       /      \
      |         jptl
      |
      |         pbga
     /        /
tknk --- padx - havc
     \        \
      |         qoyq
      |
      |         ktlj
       \      /
         fwft - cntj
              \
                xhth
In this example, tknk is at the bottom of the tower (the bottom program), and is holding up ugml, padx, and fwft. Those programs are, in turn, holding up other programs; in this example, none of those programs are holding up any other programs, and are all the tops of their own towers. (The actual tower balancing in front of you is much larger.)

Before you're ready to help them, you need to make sure your information is correct. What is the name of the bottom program?

--- Part Two ---

The programs explain the situation: they can't get down. Rather, they could get down, if they weren't expending all of their energy trying to keep the tower balanced. Apparently, one program has the wrong weight, and until it's fixed, they're stuck here.

For any program holding a disc, each program standing on that disc forms a sub-tower. Each of those sub-towers are supposed to be the same weight, or the disc itself isn't balanced. The weight of a tower is the sum of the weights of the programs in that tower.

In the example above, this means that for ugml's disc to be balanced, gyxo, ebii, and jptl must all have the same weight, and they do: 61.

However, for tknk to be balanced, each of the programs standing on its disc and all programs above it must each match. This means that the following sums must all be the same:

ugml + (gyxo + ebii + jptl) = 68 + (61 + 61 + 61) = 251
padx + (pbga + havc + qoyq) = 45 + (66 + 66 + 66) = 243
fwft + (ktlj + cntj + xhth) = 72 + (57 + 57 + 57) = 243
As you can see, tknk's disc is unbalanced: ugml's stack is heavier than the other two. Even though the nodes above ugml are balanced, ugml itself is too heavy: it needs to be 8 units lighter for its stack to weigh 243 and keep the towers balanced. If this change were made, its weight would be 60.

Given that exactly one program is the wrong weight, what would its weight need to be to balance the entire tower?

"""
import collections


class program():
    def __init__(self, name, weight=None, root=None, connections=[]):
        self.name = name
        self.weight = weight
        self.weight_above = None
        self.total_weight = None
        self.root = root
        self.connections = connections
        self.is_balanced = None
        self.items = ['name', 'weight', 'root', 'connections']

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def attributes(self):
        return({item: getattr(self, item) for item in self.items if getattr(self, item)})


class tower():
    def __init__(self, org_list):
        self.structure = {}
        self.build_tower(org_list)
        self.root = self._find_root()
        self.check_total_weight(self.root)

    def build_tower(self, org_list):
        for prog in org_list:
            self.structure.setdefault(prog.name, prog)
            self.structure[prog.name].update(**prog.attributes())

            for connection in prog.connections:
                self.structure.setdefault(connection, program(connection))
                self.structure[connection].update(**{'root': prog.name})

    def _find_root(self):
        item = next((k for k in self.structure.keys()))
        root = self.structure[item].root
        while root is not None:
            prev_root = self.structure[root].name
            root = self.structure[root].root
        return(prev_root)

    def check_total_weight(self, node):
        if not self.structure[node].connections:
            update = {'weight_above': 0, 'total_weight': self.structure[node].weight, 'is_balanced': True}
            self.structure[node].update(**update)


        if self.structure[node].weight_above is None:
            weights_above = [self.check_total_weight(node) for node in self.structure[node].connections]
            self.structure[node].is_balanced = True if len(set(weights_above)) == 1 else False
            self.structure[node].weight_above = sum(weights_above)
            self.structure[node].total_weight = self.structure[node].weight + self.structure[node].weight_above

        total_weight = self.structure[node].total_weight
        return(total_weight)

    def find_imbalances(self, node=None):
        if not node:
            ret = self.find_imbalances(self.root)
            ret = [ret] if ret == self.root else ret
            return(ret)

        if not self.structure[node].is_balanced:
            imbalances = [self.find_imbalances(conn) for conn in self.structure[node].connections]
            imbalances = [imb for imb in imbalances if imb]
            if not imbalances:
                return(node)
            else:
                return(imbalances)

    def weight_corrections(self):
        imbalanced_nodes = self.find_imbalances()
        correct_weight = {}
        for node in imbalanced_nodes:
            prog = self.structure[node]
            weights = [self.structure[n].total_weight for n in prog.connections]
            counts = collections.Counter(weights)

            desired_weight = max(collections.Counter(weights), key=lambda k: counts[k])
            incorrect_weight = list(set(weights) - set([desired_weight]))[0]
            incorrect_node = prog.connections[weights.index(incorrect_weight)]
            incorrect_program = self.structure[incorrect_node]
            correct_weight[incorrect_node] = desired_weight - incorrect_program.weight_above
        return(correct_weight)


def line_reader(file):
    with open(file, 'r') as f:
        for line in f:
            vals = [w.strip('(), ') for w in line.strip().split()]
            name = vals[0]
            weight = int(vals[1])
            connections = [] if len(vals) <= 2 else vals[3:]
            ret = program(name, weight=weight, connections=connections)
            yield(ret)


if __name__ == "__main__":
    import timeit
    t = tower(line_reader('test_input.txt'))
    weight_corrects = t.weight_corrections()
    assert t.root == 'tknk'
    assert list(weight_corrects.keys())[0] == 'ugml'
    assert list(weight_corrects.values())[0] == 60

    print(timeit.timeit(lambda: tower(line_reader('input.txt')), number=100)/100)
    t = tower(line_reader('input.txt'))
    print(t.root)
    print(t.weight_corrections())
