#Disease spread Model [ by Prabhakar Kr. Mahto ]



#**ALGORITHM**

#If T i j(t) = 0, the site (i j) is Susceptible (S)
#If TI > T i j(t)  > 1, it is Infected (I)
#If T i j(t) > TI it is in the Refractory stage (R)
#T i j(t + 1) = T i j(t)+1 if 1 <= T i j(t) <= T0- 1 
#T i j(t + 1) = 0 if T i j(t) = T0



import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
grid_size = 50  # Size of the grid
infection_rate = 0.3  # Probability of infection
recovery_rate = 0.2  # Probability of recovery
vaccination_rate = 0.02  # Probability of vaccination
mortality_rate = 0.01  # Probability of death
time_steps = 200  # Number of time steps

# States
SUSCEPTIBLE = 0
INFECTIOUS = 1
RECOVERED = 2
VACCINATED = 3
DECEASED = 4

# Initialize the grid
grid = np.random.choice([SUSCEPTIBLE, INFECTIOUS, RECOVERED, VACCINATED, DECEASED], 
                        size=(grid_size, grid_size), 
                        p=[0.7, 0.1, 0.1, 0.05, 0.05])

# Plot setup
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
im = ax1.imshow(grid, cmap='viridis', vmin=0, vmax=4)
ax1.set_title("SIRVD Cellular Automata")
cbar = plt.colorbar(im, ax=ax1, ticks=[SUSCEPTIBLE + 0.5, INFECTIOUS + 0.5, RECOVERED + 0.5, VACCINATED + 0.5, DECEASED + 0.5])
cbar.ax.set_yticklabels(['Susceptible', 'Infected', 'Recovered', 'Vaccinated', 'Deceased'])

# Data storage
susceptible_counts = []
infectious_counts = []
recovered_counts = []
vaccinated_counts = []
deceased_counts = []

# Set up the lines for the graph
line_s, = ax2.plot([], [], label='Susceptible', color='blue')
line_i, = ax2.plot([], [], label='Infectious', color='red')
line_r, = ax2.plot([], [], label='Recovered', color='green')
line_v, = ax2.plot([], [], label='Vaccinated', color='orange')
line_d, = ax2.plot([], [], label='Deceased', color='black')

ax2.set_xlim(0, time_steps)
ax2.set_ylim(0, grid_size * grid_size)
ax2.set_title("Population Counts Over Time")
ax2.set_xlabel('Time [Days]')
ax2.set_ylabel('Population size')
ax2.legend()

# Add text box for displaying exact counts
infected_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes, color='blue', fontsize=12, bbox=dict(facecolor='white', alpha=0.6))
vaccinated_text = ax1.text(0.02, 0.90, '', transform=ax1.transAxes, color='orange', fontsize=12, bbox=dict(facecolor='white', alpha=0.6))

def update(frame):
    global grid
    new_grid = grid.copy()

    for x in range(grid_size):
        for y in range(grid_size):
            if grid[x, y] == SUSCEPTIBLE:
                # Check if any neighbor is infectious
                neighbors = [
                    grid[(x - 1) % grid_size, y],
                    grid[(x + 1) % grid_size, y],
                    grid[x, (y - 1) % grid_size],
                    grid[x, (y + 1) % grid_size],
                ]
                if INFECTIOUS in neighbors and np.random.rand() < infection_rate:
                    new_grid[x, y] = INFECTIOUS
                elif np.random.rand() < vaccination_rate:
                    new_grid[x, y] = VACCINATED

            elif grid[x, y] == INFECTIOUS:
                if np.random.rand() < recovery_rate:
                    new_grid[x, y] = RECOVERED
                elif np.random.rand() < mortality_rate:
                    new_grid[x, y] = DECEASED

    grid[:] = new_grid
    im.set_array(grid)

    # Update population counts
    susceptible_count = np.sum(grid == SUSCEPTIBLE)
    infectious_count = np.sum(grid == INFECTIOUS)
    recovered_count = np.sum(grid == RECOVERED)
    vaccinated_count = np.sum(grid == VACCINATED)
    deceased_count = np.sum(grid == DECEASED)

    susceptible_counts.append(susceptible_count)
    infectious_counts.append(infectious_count)
    recovered_counts.append(recovered_count)
    vaccinated_counts.append(vaccinated_count)
    deceased_counts.append(deceased_count)

    # Update lines for the plot
    line_s.set_data(range(len(susceptible_counts)), susceptible_counts)
    line_i.set_data(range(len(infectious_counts)), infectious_counts)
    line_r.set_data(range(len(recovered_counts)), recovered_counts)
    line_v.set_data(range(len(vaccinated_counts)), vaccinated_counts)
    line_d.set_data(range(len(deceased_counts)), deceased_counts)

    # Update text box with current counts of infectious and vaccinated individuals
    infected_text.set_text(f'Infected: {infectious_count}')
    vaccinated_text.set_text(f'Vaccinated: {vaccinated_count}')

    return im, line_s, line_i, line_r, line_v, line_d, infected_text, vaccinated_text

ani = animation.FuncAnimation(fig, update, frames=time_steps, interval=200, blit=True)
plt.tight_layout()
plt.show()


##Summary
# Highest no. of infected population : 543
# Total no. of vaccinated population at end of cycle : 569
