"""
--- Day 20: Particle Swarm ---

Suddenly, the GPU contacts you, asking for help. Someone has asked it to simulate too many particles, and it won't be able to finish them all in time to render the next frame at this rate.

It transmits to you a buffer (your puzzle input) listing each particle in order (starting with particle 0, then particle 1, particle 2, and so on). For each particle, it provides the X, Y, and Z coordinates for the particle's position (p), velocity (v), and acceleration (a), each in the format <X,Y,Z>.

Each tick, all particles are updated simultaneously. A particle's properties are updated in the following order:

    Increase the X velocity by the X acceleration.
    Increase the Y velocity by the Y acceleration.
    Increase the Z velocity by the Z acceleration.
    Increase the X position by the X velocity.
    Increase the Y position by the Y velocity.
    Increase the Z position by the Z velocity.

Because of seemingly tenuous rationale involving z-buffering, the GPU would like to know which particle will stay closest to position <0,0,0> in the long term. Measure this using the Manhattan distance, which in this situation is simply the sum of the absolute values of a particle's X, Y, and Z position.

For example, suppose you are only given two particles, both of which stay entirely on the X-axis (for simplicity). Drawing the current states of particles 0 and 1 (in that order) with an adjacent a number line and diagram of current X positions (marked in parenthesis), the following would take place:

p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>                         (0)(1)

p=< 4,0,0>, v=< 1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 2,0,0>, v=<-2,0,0>, a=<-2,0,0>                      (1)   (0)

p=< 4,0,0>, v=< 0,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-2,0,0>, v=<-4,0,0>, a=<-2,0,0>          (1)               (0)

p=< 3,0,0>, v=<-1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-8,0,0>, v=<-6,0,0>, a=<-2,0,0>                         (0)

At this point, particle 1 will never be closer to <0,0,0> than particle 0, and so, in the long run, particle 0 will stay closest.

Which particle will stay closest to position <0,0,0> in the long term?

-- Part Two ---

To simplify the problem further, the GPU would like to remove any particles that collide. Particles collide if their positions ever exactly match. Because particles are updated simultaneously, more than two particles can collide at the same time and place. Once particles collide, they are removed and cannot collide with anything else after that tick.

For example:

p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>    (0)   (1)   (2)            (3)
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=<-3,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-1,0,0>, v=< 1,0,0>, a=< 0,0,0>             (0)(1)(2)      (3)
p=< 2,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=< 0,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=< 0,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=< 0,0,0>, v=< 1,0,0>, a=< 0,0,0>                       X (3)
p=< 1,0,0>, v=<-1,0,0>, a=< 0,0,0>

------destroyed by collision------
------destroyed by collision------    -6 -5 -4 -3 -2 -1  0  1  2  3
------destroyed by collision------                      (3)
p=< 0,0,0>, v=<-1,0,0>, a=< 0,0,0>

In this example, particles 0, 1, and 2 are simultaneously destroyed at the time and place marked X. On the next tick, particle 3 passes through unharmed.

How many particles are left after all collisions are resolved?
"""
from math import isclose


def load_particles(file):
    particles = []
    with open(file, 'r') as f:
        for i, line in enumerate(f.readlines()):
            pva = [item.strip(',') for item in line.split()]
            pva[0] = [int(x) for x in pva[0].strip('p=<>').split(',')]
            pva[1] = [int(x) for x in pva[1].strip('v=<>').split(',')]
            pva[2] = [int(x) for x in pva[2].strip('a=<>').split(',')]
            particles.append(particle(*pva))
    return(particles)


def get_closest_to_origin(particles):
    min_measure = None
    closest_particles = []
    for i, particle in enumerate(particles):
        particle_measure = particle.abs_acceleration()
        if min_measure is None:
            min_measure = particle_measure
        elif particle_measure == min_measure:
            closest_particles.append(i)
        elif particle_measure < min_measure:
            min_measure = particle_measure
            closest_particles = [i]

    min_measure = None
    for i in closest_particles:
        particle_measure = particles[i].abs_velocity()

        if min_measure is None:
            min_measure = particle_measure
        elif particle_measure == min_measure:
            closest_particles.append(i)
        elif particle_measure < min_measure:
            min_measure = particle_measure
            closest_particles = [i]

    return closest_particles


class particle():
    def __init__(self, p, v, a):
        self.position = p
        self.velocity = v
        self.acceleration = a
        self.ndims = len(self.position)

    def abs_acceleration(self):
        return sum(abs(x) for x in self.acceleration)

    def abs_velocity(self):
        return sum(abs(x) for x in self.velocity)

    def abs_distance(self):
        return sum(abs(x) for x in self.position)

    def get_position(self, t):
        loc = [self.position[i] + self.velocity[i] * t + .5 * (self.acceleration[i] * t * (t + 1))
               for i in range(self.ndims)]
        return loc

    def intersects(self, particle2):
        possible_solutions = [set(), set(), set()]
        for i in range(self.ndims):
            # p1 + v1*t + .5*a1*t*(t+1) = p2 + v2*t + .5*a2*t*(t+1)
            # (p1 - p2) + ((v1 - v2) + .5*(a1 - a2))*t + .5*(a1 - a2)*t^2 = 0
            # dp + dv*t + da *t^2 = 0
            dp = self.position[i] - particle2.position[i]
            da = (self.acceleration[i] - particle2.acceleration[i]) * 0.5
            dv = self.velocity[i] - particle2.velocity[i] + da
            solns = []
            if self.acceleration[i] != particle2.acceleration[i]:
                D = dv * dv - 4 * da * dp
                if D >= 0:
                    D = (D ** .5)
                    denom = 2 * da
                    solns = [(-dv + D) / denom, (-dv - D) / denom]
            elif dv != 0:
                solns = [float(-dp / dv)]

            solns = [int(soln) for soln in solns if soln >= 0 and isclose(soln, round(soln))]
            if not solns:
                break
            possible_solutions[i] = set(solns)
        final_solutions = list(set.intersection(*possible_solutions))
        return final_solutions


def get_particle_intersections(particles):
    num_particles = len(particles)
    survivors = set(range(num_particles))
    intersections = {}
    for i in range(num_particles - 1):
        for j in range(i + 1, num_particles):
            intersection_times = particles[i].intersects(particles[j])
            if intersection_times:
                for intersection_time in intersection_times:
                    intersections.setdefault(intersection_time, set())
                    intersections[intersection_time].add((i, j))

    for time in sorted(intersections):
        collisions = set()
        for colliding_particles in intersections[time]:
            if all(particle in survivors for particle in colliding_particles):
                collisions |= set(colliding_particles)
        survivors -= collisions

    return(survivors)


if __name__ == "__main__":
    particles = load_particles('input.txt')
    print(get_closest_to_origin(particles)[0])
    survivors = get_particle_intersections(particles)
    print(len(survivors))
