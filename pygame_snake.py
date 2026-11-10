"""
PYGAME SNAKE
Proyek Edukasi Gratis

Hanya untuk penggunaan edukasi pribadi dan non-komersial.
Disediakan "SEBAGAIMANA ADANYA" (AS IS), tanpa jaminan.
Lihat README untuk ketentuan penggunaan dan perizinan.

© 2026 Ikayama Education (PT IKAYAMA MANUSA SOLUSI)
"""

import pygame
import sys
import random

def main():
    # Initialize Pygame
    pygame.init()

    # Screen settings
    WIDTH = 600
    HEIGHT = 400
    CELL_SIZE = 20

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 35)

    # Starting snake position (head comes first)
    snake = [(15, 10), (14, 10), (13, 10)]

    # Snake's starting direction
    direction = (1, 0)
    next_direction = direction
    can_turn = True

    # Create food at a random position
    food = (random.randrange(WIDTH // CELL_SIZE),
            random.randrange(HEIGHT // CELL_SIZE))

    # Game variables
    score = 0
    game_over = False
    running = True

    # Snake movement speed (milliseconds)
    move_delay = 120
    last_move = pygame.time.get_ticks()


    # Main game loop
    while running:

        # Check player input
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                # Restart the game after Game Over
                if game_over:
                    if event.key == pygame.K_r:
                        snake = [(15, 10), (14, 10), (13, 10)]
                        direction = (1, 0)
                        score = 0
                        game_over = False

                        food = (random.randrange(WIDTH // CELL_SIZE),
                                random.randrange(HEIGHT // CELL_SIZE))

                        last_move = pygame.time.get_ticks()

                    elif event.key == pygame.K_ESCAPE:
                        running = False

                elif event.type == pygame.KEYDOWN and not game_over:
                    if can_turn:

                        if event.key == pygame.K_UP and direction != (0, 1):
                            next_direction = (0, -1)
                            can_turn = False

                        elif event.key == pygame.K_DOWN and direction != (0, -1):
                            next_direction = (0, 1)
                            can_turn = False

                        elif event.key == pygame.K_LEFT and direction != (1, 0):
                            next_direction = (-1, 0)
                            can_turn = False

                        elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                            next_direction = (1, 0)
                            can_turn = False

        # Move the snake
        current_time = pygame.time.get_ticks()

        if not game_over and current_time - last_move >= move_delay:

            last_move = current_time

            # Apply the new direction
            direction = next_direction
            can_turn = True

            # Calculate the snake's new head position
            head_x = snake[0][0] + direction[0]
            head_y = snake[0][1] + direction[1]
            new_head = (head_x, head_y)

            # Check whether the snake eats the food
            ate_food = new_head == food

            # Check collision with the wall
            hit_wall = (head_x < 0 or head_x >= WIDTH // CELL_SIZE or
                        head_y < 0 or head_y >= HEIGHT // CELL_SIZE)

            # Check collision with the snake's body
            if ate_food:
                hit_body = new_head in snake
            else:
                hit_body = new_head in snake[:-1]

            # Check Game Over
            if hit_wall or hit_body:
                game_over = True

            else:
                # Add the new head to the snake
                snake.insert(0, new_head)

                if ate_food:
                    score += 1

                    # Generate new food
                    food = (random.randrange(WIDTH // CELL_SIZE),
                            random.randrange(HEIGHT // CELL_SIZE))

                    # Make sure food does not appear inside the snake
                    while food in snake:
                        food = (random.randrange(WIDTH // CELL_SIZE),
                                random.randrange(HEIGHT // CELL_SIZE))

                else:
                    # Remove the last body part
                    snake.pop()

        # Draw everything on the screen
        screen.fill((0, 0, 0))

        # Draw the food
        food_rect = pygame.Rect(
            food[0] * CELL_SIZE,
            food[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(screen, (255, 0, 0), food_rect)

        # Draw the snake
        for part in snake:
            snake_rect = pygame.Rect(
                part[0] * CELL_SIZE,
                part[1] * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, (0, 200, 0), snake_rect)

        # Display the score
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Display Game Over message
        if game_over:
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            restart_text = font.render("Press R to Restart", True, (255, 255, 255))

            screen.blit(game_over_text, (220, 160))
            screen.blit(restart_text, (190, 200))

        # Update the display
        pygame.display.update()

        # Limit the game to 60 frames per second
        clock.tick(60)


    # Close Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()