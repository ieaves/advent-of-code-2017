"""
--- Day 13: Packet Scanners ---

You need to cross a vast firewall. The firewall consists of several layers, each with a security scanner that moves back and forth across the layer. To succeed, you must not be detected by a scanner.

By studying the firewall briefly, you are able to record (in your puzzle input) the depth of each layer and the range of the scanning area for the scanner within it, written as depth: range. Each layer has a thickness of exactly 1. A layer at depth 0 begins immediately inside the firewall; a layer at depth 1 would start immediately after that.

For example, suppose you've recorded the following:

0: 3
1: 2
4: 4
6: 4
This means that there is a layer immediately inside the firewall (with range 3), a second layer immediately after that (with range 2), a third layer which begins at depth 4 (with range 4), and a fourth layer which begins at depth 6 (also with range 4). Visually, it might look like this:

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]
Within each layer, a security scanner moves back and forth within its range. Each security scanner starts at the top and moves down until it reaches the bottom, then moves up until it reaches the top, and repeats. A security scanner takes one picosecond to move one step. Drawing scanners as S, the first few picoseconds look like this:


Picosecond 0:
 0   1   2   3   4   5   6
[S] [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 1:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 2:
 0   1   2   3   4   5   6
[ ] [S] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

Picosecond 3:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]
Your plan is to hitch a ride on a packet about to move through the firewall. The packet will travel along the top of each layer, and it moves at one layer per picosecond. Each picosecond, the packet moves one layer forward (its first move takes it into layer 0), and then the scanners move one step. If there is a scanner at the top of the layer as your packet enters it, you are caught. (If a scanner moves into the top of its layer while you are there, you are not caught: it doesn't have time to notice you before you leave.) If you were to do this in the configuration above, marking your current position with parentheses, your passage through the firewall would look like this:

Initial state:
 0   1   2   3   4   5   6
[S] [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 0:
 0   1   2   3   4   5   6
(S) [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
( ) [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 1:
 0   1   2   3   4   5   6
[ ] ( ) ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] (S) ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]


Picosecond 2:
 0   1   2   3   4   5   6
[ ] [S] (.) ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] (.) ... [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]


Picosecond 3:
 0   1   2   3   4   5   6
[ ] [ ] ... (.) [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

 0   1   2   3   4   5   6
[S] [S] ... (.) [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]


Picosecond 4:
 0   1   2   3   4   5   6
[S] [S] ... ... ( ) ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... ( ) ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 5:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] (.) [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [S] ... ... [S] (.) [S]
[ ] [ ]         [ ]     [ ]
[S]             [ ]     [ ]
                [ ]     [ ]


Picosecond 6:
 0   1   2   3   4   5   6
[ ] [S] ... ... [S] ... (S)
[ ] [ ]         [ ]     [ ]
[S]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... ( )
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]
In this situation, you are caught in layers 0 and 6, because your packet entered the layer when its scanner was at the top when you entered it. You are not caught in layer 1, since the scanner moved into the top of the layer once you were already there.

The severity of getting caught on a layer is equal to its depth multiplied by its range. (Ignore layers in which you do not get caught.) The severity of the whole trip is the sum of these values. In the example above, the trip severity is 0*3 + 6*4 = 24.

Given the details of the firewall you've recorded, if you leave immediately, what is the severity of your whole trip?
"""
from fractions import gcd
from functools import reduce

def load_firewall_paramaters(file):
    params = []
    with open(file, 'r') as f:
        for line in f.readlines():
            depth, range = [int(i.strip()) for i in line.split(":")]
            params.append((depth, range))
    return(params)


class firewall_layer():
    def __init__(self, _range=None, initial_scanner_location=0):
        self.range = _range
        self.scanner_location = initial_scanner_location
        self.forwards = True

    def set_range(self, _range):
        self.range = _range

    def reset_layer(self):
        self.forwards = True
        self.scanner_location = 0

    def advance_scanner(self):
        if self.forwards:
            self.scanner_location += 1
        else:
            self.scanner_location -= 1

        if self.scanner_location == 0:
            self.forwards = True
        elif self.scanner_location + 1 == self.range:
            self.forwards = False

    def reverse_scanner(self):
        if self.scanner_location + 1 == self.range:
            self.forwards = True
        elif self.scanner_location == 0:
            self.forwards = False

        if self.forwards:
            self.scanner_location -= 1
        else:
            self.scanner_location += 1

    def intruder_detected(self, location):
        if not self.range:
            return False
        else:
            return location == self.scanner_location


class firewall():
    def __init__(self, firewall_parameters):
        num_layers = max(param[0] for param in firewall_parameters) + 1
        self.layers = [firewall_layer() for i in range(0, num_layers)]
        for depth, _range in firewall_parameters:
            self.layers[depth].set_range(_range)

        self.depth = len(self.layers)

    def get_layer_range(self, layer):
        return(self.layers[layer].range)

    def advance_time(self):
        for layer in self.layers:
            layer.advance_scanner()

    def regress_time(self):
        for layer in self.layers:
            layer.reverse_scanner()

    def check_for_detection(self, layer, location):
        if layer < self.depth:
            return self.layers[layer].intruder_detected(location)
        else:
            return False

    def reset_firewall(self):
        for layer in self.layers:
            layer.reset_layer()


class packet():
    def __init__(self, firewall, starting_index=0):
        self.packet_depth_loc = 0
        self.packet_layer_loc = starting_index
        self.firewall = firewall

        self.packet_detections = []

    def advance_time(self):
        self.packet_depth_loc += 1
        self.firewall.advance_time()

    def reverse_time(self):
        self.packet_depth_loc -= 1
        self.firewall.regress_time()

    def wait(self):
        self.firewall.advance_time()

    def check_for_detection(self):
        layer = self.packet_depth_loc
        detected = self.firewall.check_for_detection(layer, self.packet_layer_loc)
        if detected:
            detection = {'layer': layer, 'range': self.firewall.get_layer_range(layer)}
            self.packet_detections.append(detection)
        return(detected)

    def find_shortest_wait(self):
        wait_counter = 0
        escaped = False
        self.reset()
        while not escaped:
            detected = False
            while self.packet_depth_loc < self.firewall.depth:
                if self.check_for_detection() and self.packet_depth_loc > 0:
                    detected = True
                    break
                self.advance_time()

            if not detected:
                escaped = True
            else:
                self.reset()
                wait_counter += 1
                [self.wait() for i in range(0, wait_counter)]

            if wait_counter % 50 == 0:
                print('attempt', wait_counter)
        return(wait_counter)

    def reset(self):
        self.packet_detections = []
        self.packet_depth_loc = 0
        self.firewall.reset_firewall()

    def advance_through_firewall(self):
        while self.packet_depth_loc < self.firewall.depth:
            self.check_for_detection()
            self.advance_time()

    def get_packet_trip_severity(self):
        self.advance_through_firewall()
        severity = sum(detec['layer'] * detec['range'] for detec in self.packet_detections)
        return severity


def set_gcd(items):
    return reduce(gcd, items)


def get_wait_time(firewall_parameters):
    params = [[layer, width, 2 * (width - 1)] for layer, width in firewall_parameters]

    w = 0
    while True:
        i = 0
        for layer, width, cycle_time in params:
            if ((w + layer) % cycle_time) == 0:
                break
            i += 1

        if i == len(params):
            break
        w += 1
    return(w)


if __name__ == "__main__":
    test_firewall_parameters = [(0, 3), (1, 2), (4, 4), (6, 4)]
    test_firewall = firewall(test_firewall_parameters)
    test_packet = packet(test_firewall)
    assert test_packet.get_packet_trip_severity() == 24

    firewall_parameters = load_firewall_paramaters('input.txt')
    _firewall = firewall(firewall_parameters)
    _packet = packet(_firewall)
    print('Severity:', _packet.get_packet_trip_severity())
    print('Wait Time:', get_wait_time(firewall_parameters))
