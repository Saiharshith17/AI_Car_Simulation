import math
import pygame
import neat
import pickle

# Constants
WIDTH = 1920
HEIGHT = 1080
CAR_SIZE_X = 60
CAR_SIZE_Y = 60
BORDER_COLOR = (255, 255, 255, 255)
START_POSITION = [830, 920]
GOAL_RADIUS = 30

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

        # User-defined parameters (using default values from training)
        self.initial_speed = 20
        self.acceleration = 2
        self.deceleration = 2
        self.max_speed = 30
        self.turning_angle = 10

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

    def rotate_center(self, image, angle):
        # Rotate The Rectangle
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image

def run_best_genome():
    # Load the best genome
    with open("best_genome.pkl", "rb") as f:
        best_genome = pickle.load(f)
    
    # Load the config file
    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                               neat.DefaultReproduction,
                               neat.DefaultSpeciesSet,
                               neat.DefaultStagnation,
                               config_path)
    
    # Create the neural network from the best genome
    net = neat.nn.FeedForwardNetwork.create(best_genome, config)
    
    # Initialize PyGame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30)
    
    # Load the map
    game_map = pygame.image.load('road_map.png').convert()
    
    # Create the car
    car = Car()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Get the network's output and control the car
        output = net.activate(car.get_data())
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
        
        # Update the car
        if car.is_alive():
            car.update(game_map)
            completed = car.check_loop_completion()
            if completed:
                print("Car completed the loop!")
        
        # Draw everything
        screen.blit(game_map, (0, 0))
        if car.is_alive():
            car.draw(screen)
        
        # Display info
        text = font.render(f"Distance: {int(car.distance)}", True, (0, 0, 0))
        screen.blit(text, (50, 50))
        
        if car.completed_loop:
            text = font.render("LOOP COMPLETED!", True, (0, 255, 0))
            screen.blit(text, (WIDTH//2 - 100, 50))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    run_best_genome()