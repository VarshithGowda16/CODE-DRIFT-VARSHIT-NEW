# main.py
import pygame
import sys
from snake import Snake
from food import Food
from collision import CollisionHandler
from scoreboard import Scoreboard

# Initialize Pygame
pygame.init()

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
FPS = 15

# Setup screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Initialize game components
snake = Snake(BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
food = Food(BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
scoreboard = Scoreboard()
collision_handler = CollisionHandler(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE)

def draw_background():
    """Draw the background (grid) on the screen"""
    screen.fill((0, 0, 0))  # black background
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            pygame.draw.rect(screen, (40, 40, 40), pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE), 1)

def handle_game_over():
    """Handles the game over state and gives the player an option to restart or quit"""
    font = pygame.font.SysFont("arial", 36)
    game_over_text = font.render("Game Over!", True, (255, 0, 0))
    restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

    screen.blit(game_over_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
    screen.blit(restart_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    restart_game()

def restart_game():
    """Restart the game after it ends"""
    snake.reset()
    scoreboard.reset()
    food.spawn()
    collision_handler.clear_obstacles()
    main_game_loop()

def main_game_loop():
    """Main game loop"""
    running = True
    while running:
        draw_background()

        # Check for events (key presses, quit, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.set_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.set_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.set_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction("RIGHT")

        # Move snake and update game state
        snake.move()
        collision_handler.handle_wall_wrap(snake)
        
        if collision_handler.is_game_over(snake):
            handle_game_over()

        # Check if snake ate food
        if food.check_collision(snake.get_head_position()):
            snake.grow()
            scoreboard.increase_score(food.get_type())
            food.spawn(is_special=food.is_special())

        # Update and draw the food and snake
        food.update()
        snake.draw(screen)
        food.draw(screen)
        scoreboard.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Start the game
if _name_ == "_main_":
    main_game_loop()
