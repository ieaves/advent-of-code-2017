"""
--- Day 21: Fractal Art ---

You find a program trying to generate some art. It uses a strange process that involves repeatedly enhancing the detail of an image through a set of rules.

The image consists of a two-dimensional square grid of pixels that are either on (#) or off (.). The program always begins with this pattern:

.#.
..#
###

Because the pattern is both 3 pixels wide and 3 pixels tall, it is said to have a size of 3.

Then, the program repeats the following process:

    If the size is evenly divisible by 2, break the pixels up into 2x2 squares, and convert each 2x2 square into a 3x3 square by following the corresponding enhancement rule.
    Otherwise, the size is evenly divisible by 3; break the pixels up into 3x3 squares, and convert each 3x3 square into a 4x4 square by following the corresponding enhancement rule.

Because each square of pixels is replaced by a larger one, the image gains pixels and so its size increases.

The artist's book of enhancement rules is nearby (your puzzle input); however, it seems to be missing rules. The artist explains that sometimes, one must rotate or flip the input pattern to find a match. (Never rotate or flip the output pattern, though.) Each pattern is written concisely: rows are listed as single units, ordered top-down, and separated by slashes. For example, the following rules correspond to the adjacent patterns:

../.#  =  ..
          .#

                .#.
.#./..#/###  =  ..#
                ###

                        #..#
#..#/..../#..#/.##.  =  ....
                        #..#
                        .##.

When searching for a rule to use, rotate and flip the pattern as necessary. For example, all of the following patterns match the same rule:

.#.   .#.   #..   ###
..#   #..   #.#   ..#
###   ###   ##.   .#.

Suppose the book contained the following two rules:

../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#

As before, the program begins with this pattern:

.#.
..#
###

The size of the grid (3) is not divisible by 2, but it is divisible by 3. It divides evenly into a single square; the square matches the second rule, which produces:

#..#
....
....
#..#

The size of this enhanced grid (4) is evenly divisible by 2, so that rule is used. It divides evenly into four squares:

#.|.#
..|..
--+--
..|..
#.|.#

Each of these squares matches the same rule (../.# => ##./#../...), three of which require some flipping and rotation to line up with the rule. The output for the rule is the same in all four cases:

##.|##.
#..|#..
...|...
---+---
##.|##.
#..|#..
...|...

Finally, the squares are joined into a new grid:

##.##.
#..#..
......
##.##.
#..#..
......

Thus, after 2 iterations, the grid contains 12 pixels that are on.

How many pixels stay on after 5 iterations?

--- Part Two ---

How many pixels stay on after 18 iterations?

"""


def load_enhancement_rules(file):
    rules = {}
    with open(file, 'r') as f:
        for i, line in enumerate(f.readlines()):
            key, value = [l.strip() for l in line.split(' => ')]
            rules[key] = value
    return(rules)


class painter():
    def __init__(self, enhancement_rules):
        self.painting = ".#./..#/###"
        self.enhancement_rules = enhancement_rules

        self.size = len(self.painting.split("/")[0])
        self.rule_size = 2 if self.size % 2 == 0 else 3
        self.n_subpaintings = self.size / self.rule_size

    def update_painting(self, new_painting):
        self.painting = new_painting
        self.size = len(self.painting.split("/")[0])
        self.rule_size = 2 if self.size % 2 == 0 else 3
        self.n_subpaintings = self.size / self.rule_size

    def _generate_subpaintings(self):
        painting = self.painting.split('/')
        if self.n_subpaintings == 1:
            yield painting
            return

        for i in xrange(self.n_subpaintings):
            rows = painting[(self.rule_size * i):(self.rule_size * (i+1))]
            for j in xrange(self.n_subpaintings):
                subpainting = [row[(self.rule_size * j):(self.rule_size * (j+1))] for row in rows]
                yield subpainting

    def _recombine_subpaintings(self, subpainting_iter):
        if self.n_subpaintings == 1:
            return list(subpainting_iter)[0]
        subpainting_iter = (i for i in subpainting_iter)
        new_painting = [[next(subpainting_iter) for i in range(self.n_subpaintings)]
                        for j in range(self.n_subpaintings)]

        final_painting = []
        for i in xrange(len(new_painting)):
            subpainting = new_painting[i]
            final_sp = zip(*[sp.split('/') for sp in subpainting])
            final_painting.extend(final_sp)
        final_painting = ["".join(sp) for sp in final_painting]
        final_painting = "/".join(final_painting)
        return(final_painting)

    def _rotate(self, painting):
        return [line[::-1] for line in painting]

    def _flip(self, painting):
        return [''.join(x) for x in zip(*painting)[::-1]]

    def _get_painting_permutations(self, painting):
        for i in range(4):
            yield '/'.join(painting)
            rotated = self._rotate(painting)
            yield '/'.join(rotated)
            painting = self._flip(painting)

    def _enhance_subpainting(self, painting):
        for permutation in self._get_painting_permutations(painting):
            if permutation in self.enhancement_rules:
                return self.enhancement_rules[permutation]

    def _split_enhance(self):
        subpaintings = self._generate_subpaintings()
        for subpainting in self._generate_subpaintings():
            yield self._enhance_subpainting(subpainting)

    def print_painting(self, painting=None):
        if not painting:
            painting = self.painting
        print("-------")
        for line in painting.split("/"):
            print(line)

    def enhance_painting(self, n=1):
        for i in range(n):
            enhanced_subpaintings = self._split_enhance()
            new_painting = self._recombine_subpaintings(enhanced_subpaintings)
            self.update_painting(new_painting)

        return(self.painting)

    def get_filled_values(self, filled_char="#"):
        return len([c for c in self.painting if c == filled_char])


if __name__ == "__main__":
    p = painter(load_enhancement_rules('test_input.txt'))
    assert p.enhance_painting(2) == "##.##./#..#../....../##.##./#..#../......"
    assert p.get_filled_values() == 12

    p2 = painter(load_enhancement_rules('input.txt'))
    p2.enhance_painting(5)
    print(p2.get_filled_values())
    p2.enhance_painting(13)
    print(p2.get_filled_values())
