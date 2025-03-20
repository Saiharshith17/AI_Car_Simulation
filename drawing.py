import pygame

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw Smooth Roads")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create a blank white canvas
screen.fill(WHITE)

# Mark the start point
pygame.draw.circle(screen, RED, (820, 930), 5)

drawing = False  # Track if the user is drawing
road_width = 35  # Radius of the circles to form roads
points_set=set()

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
            x,y=event.pos
            points_set.add((x,y))
            pygame.draw.circle(screen, BLACK, event.pos, road_width)  # Draw roads using circles

    pygame.display.update()

pygame.quit()


print(points_set)
print(len(points_set))