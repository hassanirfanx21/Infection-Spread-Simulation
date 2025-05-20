"""
Configuration parameters for the Infection Spread Simulation.
"""

# Simulation space
WIDTH = 100
HEIGHT = 100

# Population
POPULATION_SIZE = 200

# Infection parameters
INFECTION_RADIUS = 3.0
INFECTION_RATE = 0.5
RECOVERY_TIME_RANGE = (7, 14)  # Min and max days to recover
MORTALITY_RATE = 0.02

# Simulation settings
INITIAL_INFECTED = 5
SIMULATION_DAYS = 100
ANIMATION_INTERVAL = 100  # Milliseconds between frames
