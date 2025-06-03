# collision.py

class CollisionHandler:
    def _init_(self, screen_width, screen_height, block_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size
        self.boundary_mode = "solid"  # can be "solid" or "wrap"
        self.obstacles = []

    def check_wall_collision(self, snake):
        """Detect if snake hits wall (if solid wall enabled)"""
        head_x, head_y = snake.get_head_position()
        if self.boundary_mode == "solid":
            return (
                head_x < 0 or
                head_x >= self.screen_width or
                head_y < 0 or
                head_y >= self.screen_height
            )
        return False

    def handle_wall_wrap(self, snake):
        """Wrap around screen edges (for wrap mode)"""
        head_x, head_y = snake.get_head_position()
        if head_x < 0:
            head_x = self.screen_width - self.block_size
        elif head_x >= self.screen_width:
            head_x = 0
        if head_y < 0:
            head_y = self.screen_height - self.block_size
        elif head_y >= self.screen_height:
            head_y = 0

        # Set wrapped head position
        body = snake.get_body()
        body[0] = (head_x, head_y)
        snake.body = body

    def check_self_collision(self, snake):
        """Detect if the head collides with its own body"""
        head = snake.get_head_position()
        return head in snake.get_body()[1:]

    def toggle_boundary_mode(self):
        """Toggle between wrap and solid wall"""
        self.boundary_mode = "wrap" if self.boundary_mode == "solid" else "solid"

    def add_obstacle(self, position):
        """Add a static obstacle"""
        self.obstacles.append(position)

    def clear_obstacles(self):
        self.obstacles = []

    def draw_obstacles(self, screen, color=(100, 100, 100)):
        import pygame
        for pos in self.obstacles:
            pygame.draw.rect(screen, color, (*pos, self.block_size, self.block_size))

    def check_obstacle_collision(self, snake):
        return snake.get_head_position() in self.obstacles

    def is_game_over(self, snake):
        """Combined check for wall, self, and obstacles"""
        return (
            self.check_wall_collision(snake)
            or self.check_self_collision(snake)
            or self.check_obstacle_collision(snake)
        )

    def get_boundary_mode(self):
        return self.boundary_mode

# Sample test
if _name_ == "_main_":
    from snake import Snake
    snake = Snake(20, 400, 300)
    collision = CollisionHandler(400, 300, 20)

    # Simulate self-collision
    snake.body = [(100, 100), (80, 100), (60, 100), (100, 100)]  # intentional collision
    print("Self collision?", collision.check_self_collision(snake))  # True

    # Simulate wall collision
    snake.body = [(-20, 100)]
    print("Wall collision?", collision.check_wall_collision(snake))  # True
