
def line_reader(file):

    with open(file, 'r') as f:
        for line in f:
            res = [int(item) for item in line.strip().split()]
            yield(res)


def checksum(file, func):
    total = sum(func(res) for res in line_reader(file))
    return(total)


class divisors():
    def __init__(self):
        self.cache = {}
        self.inv_cache = {}

    def set_divisors(self, x):
        if x not in self.cache:
            divs = set(i for i in range(2, x) if x % i == 0)
            self.cache[x] = divs

    def set_divisors_iter(self, iterable):
        for item in iterable:
            self.set_divisors(item)

    def get_divisors(self, x):
        self.set_divisors(x)
        return(self.cache[x])


class divisor_checker():
    def __init__(self):
        self.cache = divisors()

    def check_line(self, line):
        line_items = set(line)
        self.cache.set_divisors_iter(line_items)
        for item in line_items:
            other_items = line_items - set([item])
            divs = self.cache.get_divisors(item)
            divisor = divs.intersection(other_items)
            if len(divisor) > 0:
                return(item / list(divisor)[0])

        return(0)


if __name__ == "__main__":
    assert checksum("example.txt", lambda x: max(x) - min(x)) == 18

    checker = divisor_checker()
    result = checksum('input1.txt', checker.check_line)
    print(result)
