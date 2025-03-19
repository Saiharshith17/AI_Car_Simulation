import pygame

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw Roads")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create a blank white canvas
screen.fill(WHITE)

# Mark the start point
pygame.draw.circle(screen, RED, (820, 930), 5)

drawing = False  # Track if the user is drawing
points_set = set()  # Store unique points of the drawn road

running = True
saved = False  # Ensure saving happens only once

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Start drawing
            drawing = True
        
        elif event.type == pygame.MOUSEBUTTONUP:  # Stop drawing, save & exit
            drawing = False
            if not saved:
                pygame.image.save(screen, "road_map.png")  # Save only once
                saved = True
                running = False  # Exit the loop

        elif event.type == pygame.MOUSEMOTION and drawing:  # Continue drawing
            x, y = event.pos
            points_set.add((x, y))  # Store unique (x, y) points
            pygame.draw.circle(screen, BLACK, (x, y), 4)  # Draw road

    pygame.display.update()

pygame.quit()

# Print and return the set of drawn (x, y) points
print(points_set)
print(len(points_set))