"""
Main entry point for the Infection Spread Simulation.
"""
import argparse
import config
from simulation import Simulation
from visualizer import Visualizer

def parse_arguments():
    parser = argparse.ArgumentParser(description="Infection Spread Simulation")
    parser.add_argument('--population', type=int, default=config.POPULATION_SIZE,
                      help="Size of the population")
    parser.add_argument('--width', type=float, default=config.WIDTH,
                      help="Width of the simulation area")
    parser.add_argument('--height', type=float, default=config.HEIGHT,
                      help="Height of the simulation area")
    parser.add_argument('--infection-radius', type=float, default=config.INFECTION_RADIUS,
                      help="Radius within which infection can spread")
    parser.add_argument('--infection-rate', type=float, default=config.INFECTION_RATE,
                      help="Probability of infection within radius")
    parser.add_argument('--min-recovery', type=int, default=config.RECOVERY_TIME_RANGE[0],
                      help="Minimum days to recover")
    parser.add_argument('--max-recovery', type=int, default=config.RECOVERY_TIME_RANGE[1],
                      help="Maximum days to recover")
    parser.add_argument('--mortality', type=float, default=config.MORTALITY_RATE,
                      help="Probability of death after infection period")
    parser.add_argument('--initial-infected', type=int, default=config.INITIAL_INFECTED,
                      help="Number of initially infected people")
    parser.add_argument('--days', type=int, default=config.SIMULATION_DAYS,
                      help="Duration of simulation in days")
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Create simulation
    sim = Simulation(
        population_size=args.population,
        width=args.width,
        height=args.height,
        infection_radius=args.infection_radius,
        infection_rate=args.infection_rate,
        recovery_time_range=(args.min_recovery, args.max_recovery),
        mortality_rate=args.mortality
    )
    
    # Start with some infected people
    sim.start_infection(args.initial_infected)
    
    # Visualize the simulation
    viz = Visualizer(sim)
    viz.run_visualization(frames=args.days, interval=config.ANIMATION_INTERVAL)

if __name__ == "__main__":
    main()
