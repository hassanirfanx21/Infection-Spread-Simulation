"""
Visualization module for the Infection Spread Simulation.
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from simulation import PersonState

class Visualizer:
    def __init__(self, simulation):
        self.simulation = simulation
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(15, 7))
        self.scatter = None
        self.colors = {
            PersonState.SUSCEPTIBLE: 'blue',
            PersonState.INFECTED: 'red',
            PersonState.RECOVERED: 'green',
            PersonState.DECEASED: 'black'
        }
        self.history = {
            'susceptible': [],
            'infected': [],
            'recovered': [],
            'deceased': []
        }
    
    def update_plot(self, frame):
        """Update function for the animation."""
        self.simulation.update()
        stats = self.simulation.get_statistics()
        
        # Update history
        self.history['susceptible'].append(stats['susceptible'])
        self.history['infected'].append(stats['infected'])
        self.history['recovered'].append(stats['recovered'])
        self.history['deceased'].append(stats['deceased'])
        
        # Update scatter plot
        x = [person.x for person in self.simulation.population]
        y = [person.y for person in self.simulation.population]
        colors = [self.colors[person.state] for person in self.simulation.population]
        
        if self.scatter:
            self.scatter.set_offsets(np.column_stack((x, y)))
            self.scatter.set_color(colors)
        else:
            self.scatter = self.ax1.scatter(x, y, c=colors, s=10)
        
        self.ax1.set_xlim(0, self.simulation.width)
        self.ax1.set_ylim(0, self.simulation.height)
        self.ax1.set_title(f'Day {stats["day"]}: {stats["infected"]} infected')
        
        # Update line plot
        days = list(range(len(self.history['susceptible'])))
        self.ax2.clear()
        self.ax2.plot(days, self.history['susceptible'], 'b-', label='Susceptible')
        self.ax2.plot(days, self.history['infected'], 'r-', label='Infected')
        self.ax2.plot(days, self.history['recovered'], 'g-', label='Recovered')
        self.ax2.plot(days, self.history['deceased'], 'k-', label='Deceased')
        self.ax2.legend()
        self.ax2.set_xlabel('Days')
        self.ax2.set_ylabel('Population')
        self.ax2.set_title('Population Status Over Time')
        
        return self.scatter,
    
    def run_visualization(self, frames=100, interval=100):
        """Run the animation."""
        ani = animation.FuncAnimation(
            self.fig, self.update_plot, frames=frames,
            interval=interval, blit=False)
        plt.tight_layout()
        plt.show()
        return ani
