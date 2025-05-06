import math
import sys
import pygame
import neat
import pickle

# Constants
WIDTH = 1920
HEIGHT = 1080
CAR_SIZE_X = 60
CAR_SIZE_Y = 60
BORDER_COLOR = (255, 255, 255, 255)
best_genome = None
best_fitness = -1
current_generation = 0
START_POSITION = [830, 920]
GOAL_RADIUS = 30

# User-defined configurations
def get_user_configurations():
    print("Enter the following configurations:")
    initial_speed = float(input("Initial Speed (default 20): ") or 20)
    acceleration = float(input("Acceleration Rate (default 2): ") or 2)
    deceleration = float(input("Deceleration Rate (default 2): ") or 2)
    max_speed = float(input("Maximum Speed (default 30): ") or 30)
    turning_angle = float(input("Turning Angle (default 10): ") or 10)
    simulation_time = int(input("Simulation Time per Generation (default 20 seconds): ") or 20)
    num_generations = int(input("Number of Generations (default 50): ") or 50)

    return {
        "initial_speed": initial_speed,
        "acceleration": acceleration,
        "deceleration": deceleration,
        "max_speed": max_speed,
        "turning_angle": turning_angle,
        "simulation_time": simulation_time,
        "num_generations": num_generations,
    }

user_config = get_user_configurations()



class Car:
    def __init__(self):
        # Load Car Sprite and Rotate
        self.sprite = pygame.image.load('car.png').convert()  # Convert Speeds Up A Lot
        self.sprite = pygame.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite
        self.start_position = START_POSITION
        self.completed_loop = False

        # Starting Position
        self.position = [830, 920]
        self.angle = 0
        self.speed = 0
        self.speed_set = False  # Flag For Default Speed Later on

        # User-defined parameters
        self.initial_speed = user_config["initial_speed"]
        self.acceleration = user_config["acceleration"]
        self.deceleration = user_config["deceleration"]
        self.max_speed = user_config["max_speed"]
        self.turning_angle = user_config["turning_angle"]

        self.center = [self.position[0] + CAR_SIZE_X / 2, self.position[1] + CAR_SIZE_Y / 2]  # Calculate Center
        self.radars = []  # List For Sensors / Radars
        self.drawing_radars = []  # Radars To Be Drawn
        self.alive = True  # Boolean To Check If Car is Crashed
        self.distance = 0  # Distance Driven
        self.time = 0  # Time Passed

    def check_loop_completion(self):
        distance = math.sqrt((self.center[0] - self.start_position[0]) ** 2 +
                            (self.center[1] - self.start_position[1]) ** 2)
        if distance <= GOAL_RADIUS and self.distance > 100:
            self.completed_loop = True
        return self.completed_loop

    def draw(self, screen):
        screen.blit(self.rotated_sprite, self.position)  # Draw Sprite
        self.draw_radar(screen)  

    def draw_radar(self, screen):
        
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    def check_collision(self, game_map):
        self.alive = True
        for point in self.corners:
            
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                break

    def check_radar(self, degree, game_map):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # While We Don't Hit BORDER_COLOR AND length < 300 (just a max) -> go further and further
        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Calculate Distance To Border And Append To Radars List
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])

    def update(self, game_map):
        # Set The Speed To Initial Speed For The First Time
        if not self.speed_set:
            self.speed = self.initial_speed
            self.speed_set = True

        # Get Rotated Sprite And Move Into The Right X-Direction
        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], WIDTH - 120)

        # Increase Distance and Time
        self.distance += self.speed
        self.time += 1

        # Same For Y-Position
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], WIDTH - 120)

        # Calculate New Center
        self.center = [int(self.position[0]) + CAR_SIZE_X / 2, int(self.position[1]) + CAR_SIZE_Y / 2]

        # Calculate Four Corners
        length = 0.5 * CAR_SIZE_X
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length,
                    self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length,
                     self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length,
                       self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length,
                        self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        # Check Collisions And Clear Radars
        self.check_collision(game_map)
        self.radars.clear()

        # From -90 To 120 With Step-Size 45 Check Radar
        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)

    def get_data(self):
        # Get Distances To Border
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    def is_alive(self):
        # Basic Alive Function
        return self.alive

    def get_reward(self):
        # Calculate Reward (Maybe Change?)
        return self.distance / (CAR_SIZE_X / 2)

    def rotate_center(self, image, angle):
        # Rotate The Rectangle
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image


def run_simulation(genomes, config):
    global best_genome, best_fitness

    nets = []
    cars = []

    # Initialize PyGame And The Display
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    # For All Genomes Passed Create A New Neural Network
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        cars.append(Car())

    # Clock Settings
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    game_map = pygame.image.load('map4.png').convert()  # Convert Speeds Up A Lot

    global current_generation
    current_generation += 1

    # Simple Counter To Roughly Limit Time
    counter = 0
    simulation_time = user_config["simulation_time"]

    while True:
        # Exit On Quit Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # For Each Car Get The Action It Takes
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())
            choice = output.index(max(output))
            if choice == 0:
                car.angle += car.turning_angle  # Left
            elif choice == 1:
                car.angle -= car.turning_angle  # Right
            elif choice == 2:
                if car.speed - car.deceleration >= 12:
                    car.speed -= car.deceleration  # Slow Down
            else:
                car.speed = min(car.speed + car.acceleration, car.max_speed)  # Speed Up

        # Check If Car Is Still Alive
        still_alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                still_alive += 1
                car.update(game_map)
                genomes[i][1].fitness += car.get_reward()

                # Check if the car completed the loop
                if car.check_loop_completion():
                    print(f"Car {i} completed the loop!")
                    # Update best genome if this car has the highest fitness
                    if genomes[i][1].fitness > best_fitness:
                        best_fitness = genomes[i][1].fitness
                        best_genome = genomes[i][1]

        if still_alive == 0:
            break

        counter += 1
        if counter == 30 * simulation_time:  # Stop After User-Defined Time
            break

        # Draw Map And All Cars That Are Alive
        screen.blit(game_map, (0, 0))
        for car in cars:
            if car.is_alive():
                car.draw(screen)

        # Display Info
        text = generation_font.render("Generation: " + str(current_generation), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        screen.blit(text, text_rect)

        text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    # Save the best genome only if the loop was completed
    if best_genome is not None and any(car.completed_loop for car in cars):
        with open("best_genome.pkl", "wb") as f:
            pickle.dump(best_genome, f)
        print(f"Best genome saved with fitness: {best_fitness}")
    else:
        print("No car completed the loop. Best genome not saved.")


if __name__ == "__main__":
    # Load Config
    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                               neat.DefaultReproduction,
                               neat.DefaultSpeciesSet,
                               neat.DefaultStagnation,
                               config_path)

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Run Simulation For A Maximum of User-Defined Generations
    population.run(run_simulation, user_config["num_generations"])