"""
Core simulation module for the Infection Spread Simulation.
"""
import random
import numpy as np
from enum import Enum

class PersonState(Enum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2
    DECEASED = 3

class Person:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.state = PersonState.SUSCEPTIBLE
        self.infection_day = None
        self.recovery_time = 0
    
    def infect(self, day, recovery_time):
        if self.state == PersonState.SUSCEPTIBLE:
            self.state = PersonState.INFECTED
            self.infection_day = day
            self.recovery_time = recovery_time
    
    def update(self, day, mortality_rate):
        if self.state == PersonState.INFECTED:
            if day - self.infection_day >= self.recovery_time:
                if random.random() < mortality_rate:
                    self.state = PersonState.DECEASED
                else:
                    self.state = PersonState.RECOVERED

class Simulation:
    def __init__(self, population_size, width, height, infection_radius, 
                 infection_rate, recovery_time_range, mortality_rate):
        self.population = []
        self.width = width
        self.height = height
        self.infection_radius = infection_radius
        self.infection_rate = infection_rate
        self.recovery_time_range = recovery_time_range
        self.mortality_rate = mortality_rate
        self.day = 0
        
        # Initialize population
        for i in range(population_size):
            x = random.uniform(0, width)
            y = random.uniform(0, height)
            self.population.append(Person(i, x, y))
    
    def start_infection(self, initial_infected=1):
        """Randomly infect a number of people to start the simulation."""
        for i in range(min(initial_infected, len(self.population))):
            person = random.choice(self.population)
            if person.state == PersonState.SUSCEPTIBLE:
                recovery_time = random.randint(*self.recovery_time_range)
                person.infect(self.day, recovery_time)
    
    def update(self):
        """Run one day of the simulation."""
        # Move people randomly
        for person in self.population:
            if person.state != PersonState.DECEASED:
                person.x += random.uniform(-1, 1)
                person.y += random.uniform(-1, 1)
                
                # Keep within bounds
                person.x = max(0, min(self.width, person.x))
                person.y = max(0, min(self.height, person.y))
        
        # Spread infection
        for infected_person in [p for p in self.population if p.state == PersonState.INFECTED]:
            for person in self.population:
                if person.state == PersonState.SUSCEPTIBLE:
                    distance = np.sqrt((infected_person.x - person.x)**2 + 
                                       (infected_person.y - person.y)**2)
                    if distance < self.infection_radius:
                        if random.random() < self.infection_rate:
                            recovery_time = random.randint(*self.recovery_time_range)
                            person.infect(self.day, recovery_time)
        
        # Update states
        for person in self.population:
            person.update(self.day, self.mortality_rate)
        
        self.day += 1
    
    def get_statistics(self):
        """Return statistics about the current state of the simulation."""
        stats = {
            'day': self.day,
            'susceptible': sum(1 for p in self.population if p.state == PersonState.SUSCEPTIBLE),
            'infected': sum(1 for p in self.population if p.state == PersonState.INFECTED),
            'recovered': sum(1 for p in self.population if p.state == PersonState.RECOVERED),
            'deceased': sum(1 for p in self.population if p.state == PersonState.DECEASED),
        }
        stats['total'] = len(self.population)
        return stats
