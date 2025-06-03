# snake.py
import pygame

class Snake:
    def __init__(self, block_size, screen_width, screen_height):
        self.block_size = block_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.direction = "RIGHT"
        self.body = [(screen_width // 2, screen_height // 2)]
        self.color = (0, 255, 0)
        self.change_to = self.direction
        self.grow_pending = False
        self.speed = 1

    def set_direction(self, direction):
        """Avoid reversing direction"""
        opposites = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }
        if direction != opposites.get(self.direction):
            self.change_to = direction

    def move(self):
        """Move the snake based on direction"""
        self.direction = self.change_to
        head_x, head_y = self.body[0]

        if self.direction == "UP":
            head_y -= self.block_size
        elif self.direction == "DOWN":
            head_y += self.block_size
        elif self.direction == "LEFT":
            head_x -= self.block_size
        elif self.direction == "RIGHT":
            head_x += self.block_size

        new_head = (head_x, head_y)
        self.body.insert(0, new_head)

        if self.grow_pending:
            self.grow_pending = False
        else:
            self.body.pop()

    def grow(self):
        self.grow_pending = True

    def draw(self, screen):
        for i, segment in enumerate(self.body):
            color = (0, 200, 0) if i == 0 else self.color
            pygame.draw.rect(screen, color, pygame.Rect(segment[0], segment[1], self.block_size, self.block_size))

    def reset(self):
        self.body = [(self.screen_width // 2, self.screen_height // 2)]
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.grow_pending = False

    def get_head_position(self):
        return self.body[0]

    def get_body(self):
        return self.body

    def length(self):
        return len(self.body)

    def increase_speed(self, factor=0.2):
        self.speed += factor

    def get_speed(self):
        return self.speed

    def hit_wall(self):
        head_x, head_y = self.body[0]
        return (
            head_x < 0 or head_x >= self.screen_width or
            head_y < 0 or head_y >= self.screen_height
        )

    def hit_self(self):
        return self.body[0] in self.body[1:]
