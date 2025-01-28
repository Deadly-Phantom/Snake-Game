import pygame
import random
import time
import math

# Initialize Pygame and set up fullscreen
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH = screen.get_width()
WINDOW_HEIGHT = screen.get_height()
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 191, 255)
BLOOD_RED = (139, 0, 0)
GOO_GREEN = (80, 200, 120)
DARK_GOO = (40, 150, 80)

# Update Colors with neon/cyber theme
NEON_GREEN = (0, 255, 162)
NEON_BLUE = (0, 195, 255)
NEON_PINK = (255, 0, 153)
NEON_PURPLE = (187, 0, 255)
CYBER_BLACK = (10, 15, 20)
GRID_COLOR = (30, 40, 50)

# Replace RAINBOW_COLORS with CYBER_COLORS
CYBER_COLORS = [
    NEON_GREEN,
    NEON_BLUE,
    NEON_PINK,
    NEON_PURPLE,
    (0, 255, 255),  # Cyan
    (255, 0, 255),  # Magenta
    (255, 255, 0)   # Yellow
]

# Replace PASTEL_BACKGROUNDS with CYBER_BACKGROUNDS
CYBER_BACKGROUNDS = [
    (0, 5, 20),      # Deep space blue
    (20, 0, 20),     # Dark cyberpunk purple
    (5, 20, 15),     # Dark matrix green
    (20, 5, 15),     # Neo-noir red
    (15, 0, 25),     # Deep tech violet
]

# Add to colors section
GLOW_COLORS = [
    (0, 255, 162),    # Neon Green
    (0, 195, 255),    # Neon Blue
    (255, 0, 153),    # Neon Pink
    (187, 0, 255),    # Neon Purple
    (0, 255, 255),    # Cyan
    (255, 0, 255)     # Magenta
]

# Add to colors section
GOLD = (255, 215, 0)
BRIGHT_GOLD = (255, 230, 100)
NEON_GOLD = (255, 240, 150)

# Add fruit colors with cyber twist
CYBER_FRUITS = [
    {
        'name': 'apple',
        'main': (255, 50, 50),    # Bright red
        'highlight': (255, 150, 150),
        'leaf': (50, 255, 100)
    },
    {
        'name': 'orange',
        'main': (255, 140, 0),    # Bright orange
        'highlight': (255, 200, 100),
        'detail': (255, 160, 50)
    },
    {
        'name': 'lemon',
        'main': (255, 255, 50),   # Bright yellow
        'highlight': (255, 255, 150),
        'detail': (255, 255, 100)
    },
    {
        'name': 'kiwi',
        'main': (150, 255, 50),   # Bright green
        'highlight': (200, 255, 150),
        'seeds': (50, 50, 50)
    },
    {
        'name': 'banana',
        'main': (255, 255, 100),  # Bright yellow
        'highlight': (255, 255, 200),
        'detail': (255, 200, 50)
    },
    {
        'name': 'pineapple',
        'main': (255, 200, 50),   # Golden yellow
        'highlight': (255, 255, 150),
        'detail': (100, 255, 100)
    },
    {
        'name': 'cherries',
        'main': (255, 0, 50),     # Deep red
        'highlight': (255, 100, 150),
        'stem': (100, 255, 100)
    }
]

# Set up the display
pygame.display.set_caption('Rainbow Snake Game')

GOLD_COLOR = (255, 215, 0)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1
        self.rainbow_index = 0
        self.special_effect_start = 0
        self.regular_gold_end = 0

    def set_special_effect(self):
        self.special_effect_start = time.time()

    def set_regular_gold(self, duration):
        self.regular_gold_end = time.time() + duration

    def get_special_color(self, current_time):
        if self.special_effect_start == 0:
            return None
            
        time_since_effect = current_time - self.special_effect_start
        if time_since_effect > 3:  # Total duration of 3 seconds
            self.special_effect_start = 0
            return None
            
        # Determine which color phase we're in
        if time_since_effect < 1:
            return NEON_GREEN
        elif time_since_effect < 2:
            return NEON_PINK
        else:
            return NEON_BLUE

    def is_segment_gold(self, current_time):
        return current_time < self.regular_gold_end

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        
        if new in self.positions[2:]:
            return False
        
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1
        self.rainbow_index = 0
        self.special_effect_start = 0
        self.regular_gold_end = 0

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.fruit_index = 0
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1),
                        random.randint(0, GRID_HEIGHT-1))
        self.fruit_index = (self.fruit_index + 1) % len(CYBER_FRUITS)

class SpecialFood:
    def __init__(self):
        self.position = (0, 0)
        self.active = False
        self.spawn_time = 0
        self.value = 5

    def randomize_position(self, obstacles):
        self.position = (random.randint(0, GRID_WIDTH-1),
                        random.randint(0, GRID_HEIGHT-1))
        while self.position in obstacles:
            self.position = (random.randint(0, GRID_WIDTH-1),
                           random.randint(0, GRID_HEIGHT-1))
        self.active = True
        self.spawn_time = time.time()

def flash_milestone():
    class MilestoneFlash:
        def __init__(self):
            self.duration = 0.5  # Quick flash
            self.start_time = time.time()
            self.colors = [NEON_PINK, NEON_BLUE]
            self.flashes = 3  # Number of flashes

        def draw(self, screen, current_time):
            if current_time - self.start_time > self.duration:
                return False

            progress = (current_time - self.start_time) / self.duration
            flash_index = int(progress * self.flashes * 2) % 2  # Alternates between 0 and 1
            color = self.colors[flash_index]
            
            # Draw full screen flash with alpha
            flash_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            flash_alpha = int(100 * (1 - progress))  # Fade out
            pygame.draw.rect(flash_surf, (*color, flash_alpha), 
                           (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
            screen.blit(flash_surf, (0, 0))
            
            return True

def draw_snake_segment(screen, pos, next_pos, prev_pos, is_head, is_tail, color):
    x, y = pos[0] * GRID_SIZE, pos[1] * GRID_SIZE
    segment_surf = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    
    if is_head:
        # Calculate direction for head (same as body)
        direction = (pos[0] - next_pos[0], pos[1] - next_pos[1])
        
        # Draw head exactly like body segment
        if abs(direction[0]) > abs(direction[1]):  # Moving horizontally
            pygame.draw.ellipse(segment_surf, color,
                              (0, GRID_SIZE/6,  # Long sides on left/right for horizontal
                               GRID_SIZE, GRID_SIZE*2/3))
        else:  # Moving vertically
            pygame.draw.ellipse(segment_surf, color,
                              (GRID_SIZE/6, 0,  # Long sides on top/bottom for vertical
                               GRID_SIZE*2/3, GRID_SIZE))
        
    elif is_tail:
        # Draw tail (existing tail code)
        angle = math.atan2(prev_pos[1] - pos[1], prev_pos[0] - pos[0])
        
        # Draw ribbed segments
        num_ribs = 4
        for i in range(num_ribs):
            rib_size = GRID_SIZE/2 - (i * GRID_SIZE/8)
            rib_offset = i * GRID_SIZE/4
            rib_rect = pygame.Rect(
                GRID_SIZE/2 - rib_size/2,
                rib_offset,
                rib_size,
                GRID_SIZE/5
            )
            pygame.draw.ellipse(segment_surf, color, rib_rect)
        
        # Rotate the surface to face outward
        segment_surf = pygame.transform.rotate(segment_surf, -math.degrees(angle) + 90 + 180)
    else:
        # Draw body segment (jelly bean)
        direction = (next_pos[0] - prev_pos[0], next_pos[1] - prev_pos[1])
        if abs(direction[0]) > abs(direction[1]):  # Moving horizontally
            pygame.draw.ellipse(segment_surf, color,
                              (0, GRID_SIZE/6,  # Long sides on left/right for horizontal
                               GRID_SIZE, GRID_SIZE*2/3))
        else:  # Moving vertically
            pygame.draw.ellipse(segment_surf, color,
                              (GRID_SIZE/6, 0,  # Long sides on top/bottom for vertical
                               GRID_SIZE*2/3, GRID_SIZE))
    
    # Position the segment
    new_rect = segment_surf.get_rect(center=(x + GRID_SIZE/2, y + GRID_SIZE/2))
    screen.blit(segment_surf, new_rect)

class Obstacles:
    def __init__(self):
        self.positions = set()
        self.last_spawn_time = time.time()
        # Don't generate obstacles in __init__
        # Will generate first obstacles in main() instead

    def is_valid_position(self, new_positions, snake, food, special_food):
        # Check if position overlaps with snake
        for pos in new_positions:
            if pos in snake.positions:
                return False
            
            # Check if position overlaps with food
            if pos == food.position:
                return False
                
            # Check if position overlaps with special food
            if special_food.active and pos == special_food.position:
                return False
                
            # Check if position overlaps with existing obstacles
            if pos in self.positions:
                return False
        
        return True

    def add_new_obstacle(self, snake, food, special_food):
        max_attempts = 100
        for _ in range(max_attempts):
            # Random starting position
            start_x = random.randint(0, GRID_WIDTH - 2)
            start_y = random.randint(0, GRID_HEIGHT - 2)
            
            # Calculate all positions for 2x2 obstacle
            new_positions = {
                (start_x, start_y),
                (start_x + 1, start_y),
                (start_x, start_y + 1),
                (start_x + 1, start_y + 1)
            }
            
            # Check if position is valid
            if self.is_valid_position(new_positions, snake, food, special_food):
                self.positions.update(new_positions)
                return True
        
        return False  # Could not find valid position

    def generate_obstacles(self, snake, food, special_food):
        self.positions.clear()
        num_clusters = random.randint(3, 5)
        
        for _ in range(num_clusters):
            self.add_new_obstacle(snake, food, special_food)

class GooDrop:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.length = 0
        self.max_length = random.randint(10, 30)

    def update(self):
        self.length = min(self.length + self.speed, self.max_length)
        return self.length < self.max_length

def draw_grid():
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        alpha = abs(math.sin(time.time() * 2 + x * 0.1)) * 100 + 50
        s = pygame.Surface((1, WINDOW_HEIGHT))
        s.fill(GRID_COLOR)
        s.set_alpha(int(alpha))
        screen.blit(s, (x, 0))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        alpha = abs(math.sin(time.time() * 2 + y * 0.1)) * 100 + 50
        s = pygame.Surface((WINDOW_WIDTH, 1))
        s.fill(GRID_COLOR)
        s.set_alpha(int(alpha))
        screen.blit(s, (0, y))

def draw_game_over(alpha):
    text_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    try:
        font = pygame.font.Font("font/Orbitron-Bold.ttf", 74)
    except:
        font = pygame.font.Font(None, 74)
    
    # Glitch effect
    glitch_offset = random.randint(-3, 3) if random.random() < 0.5 else 0
    
    # Main text with cyber effect
    text = "GAME OVER"
    for i in range(3):
        offset = random.randint(-2, 2) if random.random() < 0.3 else 0
        color = random.choice([NEON_GREEN, NEON_BLUE, NEON_PINK])
        text_render = font.render(text, True, color)
        text_rect = text_render.get_rect(center=(WINDOW_WIDTH/2 + offset + glitch_offset, 
                                               WINDOW_HEIGHT/2 - 50))
        text_surface.blit(text_render, text_rect)
    
    text_surface.set_alpha(int(alpha * 255))
    screen.blit(text_surface, (0, 0))
    
    # Play again text with cyber effect
    if alpha > 0.8:
        try:
            font = pygame.font.Font("font/Orbitron-Regular.ttf", 36)
        except:
            font = pygame.font.Font(None, 36)
        text = "CLICK TO RESTART"
        glow = font.render(text, True, NEON_BLUE)
        main = font.render(text, True, NEON_GREEN)
        text_rect = main.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 50))
        glow_rect = text_rect.copy()
        
        # Add glow effect
        screen.blit(glow, glow_rect.move(2, 2))
        screen.blit(glow, glow_rect.move(-2, -2))
        screen.blit(main, text_rect)

def draw_fruit(position, fruit_data, current_time):
    rect = pygame.Rect(position[0] * GRID_SIZE,
                      position[1] * GRID_SIZE,
                      GRID_SIZE, GRID_SIZE)
    
    fruit_surf = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    pulse = (math.sin(current_time * 3) + 1) / 2  # Slower pulse than special fruit
    
    if fruit_data['name'] == 'apple':
        # Draw apple body
        pygame.draw.circle(fruit_surf, fruit_data['main'], 
                         (GRID_SIZE/2, GRID_SIZE/2 + 2), GRID_SIZE/2.5)
        # Draw leaf
        leaf_points = [(GRID_SIZE/2, GRID_SIZE/3),
                      (GRID_SIZE/2 - 3, GRID_SIZE/4),
                      (GRID_SIZE/2 + 3, GRID_SIZE/4)]
        pygame.draw.polygon(fruit_surf, fruit_data['leaf'], leaf_points)
        
    elif fruit_data['name'] == 'orange':
        # Draw orange with segments
        pygame.draw.circle(fruit_surf, fruit_data['main'], 
                         (GRID_SIZE/2, GRID_SIZE/2), GRID_SIZE/2.2)
        for i in range(4):
            angle = math.pi/4 + i * math.pi/2
            pygame.draw.line(fruit_surf, fruit_data['detail'],
                           (GRID_SIZE/2, GRID_SIZE/2),
                           (GRID_SIZE/2 + math.cos(angle) * GRID_SIZE/2.5,
                            GRID_SIZE/2 + math.sin(angle) * GRID_SIZE/2.5), 1)
            
    elif fruit_data['name'] == 'lemon':
        # Draw lemon shape
        points = [(GRID_SIZE/4, GRID_SIZE/2),
                 (GRID_SIZE/2, GRID_SIZE/4),
                 (3*GRID_SIZE/4, GRID_SIZE/2),
                 (GRID_SIZE/2, 3*GRID_SIZE/4)]
        pygame.draw.polygon(fruit_surf, fruit_data['main'], points)
        
    elif fruit_data['name'] == 'kiwi':
        # Draw kiwi with seeds
        pygame.draw.circle(fruit_surf, fruit_data['main'], 
                         (GRID_SIZE/2, GRID_SIZE/2), GRID_SIZE/2.2)
        for i in range(5):
            seed_x = GRID_SIZE/2 + math.cos(current_time + i) * GRID_SIZE/4
            seed_y = GRID_SIZE/2 + math.sin(current_time + i) * GRID_SIZE/4
            pygame.draw.circle(fruit_surf, fruit_data['seeds'], 
                             (seed_x, seed_y), 1)
            
    elif fruit_data['name'] == 'banana':
        # Draw curved banana shape
        points = []
        for i in range(5):
            angle = i * math.pi/4
            r = GRID_SIZE/3
            x = GRID_SIZE/2 + math.cos(angle) * r
            y = GRID_SIZE/2 + math.sin(angle) * r
            points.append((x, y))
        pygame.draw.polygon(fruit_surf, fruit_data['main'], points)
        
    elif fruit_data['name'] == 'pineapple':
        # Draw pineapple body
        points = [(GRID_SIZE/2, GRID_SIZE/4),
                 (3*GRID_SIZE/4, GRID_SIZE/2),
                 (GRID_SIZE/2, 3*GRID_SIZE/4),
                 (GRID_SIZE/4, GRID_SIZE/2)]
        pygame.draw.polygon(fruit_surf, fruit_data['main'], points)
        # Draw cross-pattern
        for i in range(3):
            y = GRID_SIZE/3 + i * GRID_SIZE/4
            pygame.draw.line(fruit_surf, fruit_data['detail'],
                           (GRID_SIZE/3, y),
                           (2*GRID_SIZE/3, y), 1)
            
    elif fruit_data['name'] == 'cherries':
        # Draw two cherries
        pygame.draw.circle(fruit_surf, fruit_data['main'], 
                         (GRID_SIZE/3, GRID_SIZE/2), GRID_SIZE/4)
        pygame.draw.circle(fruit_surf, fruit_data['main'], 
                         (2*GRID_SIZE/3, GRID_SIZE/2), GRID_SIZE/4)
        # Draw stem
        pygame.draw.line(fruit_surf, fruit_data['stem'],
                        (GRID_SIZE/3, GRID_SIZE/3),
                        (GRID_SIZE/2, GRID_SIZE/4), 2)
        pygame.draw.line(fruit_surf, fruit_data['stem'],
                        (2*GRID_SIZE/3, GRID_SIZE/3),
                        (GRID_SIZE/2, GRID_SIZE/4), 2)

    # Add subtle glow effect
    glow_alpha = int(64 + 64 * pulse)
    glow_surf = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (*fruit_data['highlight'], glow_alpha),
                      (GRID_SIZE/2, GRID_SIZE/2), GRID_SIZE/2)
    fruit_surf.blit(glow_surf, (0, 0))
    
    screen.blit(fruit_surf, rect)

def draw_special_fruit(position, current_time):
    rect = pygame.Rect(position[0] * GRID_SIZE,
                      position[1] * GRID_SIZE,
                      GRID_SIZE, GRID_SIZE)
    
    # Create surface for the special fruit
    fruit_surf = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    
    # Calculate pulsing values
    pulse = (math.sin(current_time * 5) + 1) / 2  # Pulsing effect
    rotation = current_time * 2  # Rotation angle
    
    # Draw outer gold rim (rotating)
    points = []
    for i in range(8):
        angle = rotation + i * (math.pi / 4)
        radius = GRID_SIZE/2 - 1
        x = GRID_SIZE/2 + math.cos(angle) * radius
        y = GRID_SIZE/2 + math.sin(angle) * radius
        points.append((x, y))
    
    # Draw gold rim with gradient effect
    pygame.draw.polygon(fruit_surf, GOLD, points, 2)
    pygame.draw.polygon(fruit_surf, BRIGHT_GOLD, points, 1)
    
    # Inner circle with dynamic pattern
    center_radius = GRID_SIZE/3
    pygame.draw.circle(fruit_surf, NEON_BLUE, (GRID_SIZE/2, GRID_SIZE/2), center_radius)
    
    # Add cross pattern
    cross_size = int(center_radius * 0.8)
    cross_thickness = 2
    cross_offset = GRID_SIZE/2
    
    # Rotating cross
    rot_angle = -rotation  # Counter-rotation
    for i in range(2):
        angle = rot_angle + i * math.pi/2
        start_x = cross_offset + math.cos(angle) * cross_size
        start_y = cross_offset + math.sin(angle) * cross_size
        end_x = cross_offset - math.cos(angle) * cross_size
        end_y = cross_offset - math.sin(angle) * cross_size
        pygame.draw.line(fruit_surf, NEON_GOLD, 
                        (start_x, start_y), 
                        (end_x, end_y), 
                        cross_thickness)
    
    # Add glow effect
    glow_alpha = int(127 + 128 * pulse)  # Pulsing alpha
    glow_surf = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (*NEON_BLUE, glow_alpha), 
                      (GRID_SIZE/2, GRID_SIZE/2), 
                      center_radius * 0.8)
    
    # Combine surfaces
    fruit_surf.blit(glow_surf, (0, 0))
    
    # Add final highlight
    highlight_pos = (GRID_SIZE/2 + math.cos(rotation) * center_radius * 0.3,
                    GRID_SIZE/2 + math.sin(rotation) * center_radius * 0.3)
    pygame.draw.circle(fruit_surf, BRIGHT_GOLD, 
                      (int(highlight_pos[0]), int(highlight_pos[1])), 
                      2)
    
    # Draw the final fruit
    screen.blit(fruit_surf, rect)

def main():
    # Hide cursor
    pygame.mouse.set_visible(False)
    
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    special_food = SpecialFood()
    obstacles = Obstacles()
    score = 0
    game_over = False
    fade_alpha = 0
    last_special_spawn = time.time()
    background_index = 0
    milestone_flash = None
    last_milestone = 0

    # Speed settings
    base_speed = 7  # Starting speed (frames per second)
    max_speed = 15  # Maximum speed
    speed_increase = 0.5  # How much speed increases per point
    current_speed = base_speed

    # Generate initial obstacles
    obstacles.generate_obstacles(snake, food, special_food)

    while True:
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Add escape key to exit
                    pygame.quit()
                    return
                elif not game_over:
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                # Reset game and speed
                snake.reset()
                food.randomize_position()
                obstacles.generate_obstacles(snake, food, special_food)
                score = 0
                current_speed = base_speed  # Reset speed
                game_over = False
                fade_alpha = 0

        if not game_over:
            # Update speed based on score
            current_speed = min(max_speed, base_speed + (score * speed_increase))

            snake.update()  # Update snake's position
            
            # Handle self-collision
            if snake.get_head_position() in snake.positions[1:]:
                game_over = True  # Stop the game if the snake hits itself
            
            # Handle special food spawning
            if not special_food.active and current_time - last_special_spawn >= 10:
                special_food.randomize_position(obstacles.positions)
                last_special_spawn = current_time
            
            # Handle special food despawning
            if special_food.active and current_time - special_food.spawn_time >= 5:
                special_food.active = False

            # Handle obstacle spawning every 10 seconds
            if current_time - obstacles.last_spawn_time >= 10:
                if obstacles.add_new_obstacle(snake, food, special_food):
                    obstacles.last_spawn_time = current_time

            # Check collision with obstacles
            if snake.get_head_position() in obstacles.positions:
                game_over = True
                continue

            # Check if snake ate food
            if snake.get_head_position() == food.position:
                snake.length += 1
                score += 1
                snake.rainbow_index = (snake.rainbow_index + 1) % len(CYBER_COLORS)
                background_index = (background_index + 1) % len(CYBER_BACKGROUNDS)
                food.randomize_position()
                snake.set_regular_gold(1.0)
                
                # Check for 10-point milestone
                if score % 10 == 0:
                    snake.set_regular_gold(5.0)

            # Check if snake ate special food
            if special_food.active and snake.get_head_position() == special_food.position:
                snake.length += 1
                score += special_food.value
                special_food.active = False
                snake.rainbow_index = (snake.rainbow_index + 1) % len(CYBER_COLORS)
                background_index = (background_index + 1) % len(CYBER_BACKGROUNDS)
                snake.set_special_effect()  # Start color cycle effect

            # Check for score milestone (every 10 points)
            current_milestone = score // 10
            if current_milestone > last_milestone:
                milestone_flash = flash_milestone()
                last_milestone = current_milestone

        # Draw everything
        screen.fill(CYBER_BACKGROUNDS[background_index])
        draw_grid()  # Add cyber grid
        
        # Draw obstacles with glow effect
        for pos in obstacles.positions:
            rect = pygame.Rect(pos[0] * GRID_SIZE,
                             pos[1] * GRID_SIZE,
                             GRID_SIZE, GRID_SIZE)
            # Glow
            glow_surf = pygame.Surface((GRID_SIZE + 4, GRID_SIZE + 4))
            glow_surf.fill(NEON_PURPLE)
            glow_rect = glow_surf.get_rect(center=rect.center)
            screen.blit(glow_surf, glow_rect)
            # Main
            pygame.draw.rect(screen, CYBER_BLACK, rect)
            pygame.draw.rect(screen, NEON_PURPLE, rect, 1)

        # Draw regular food
        draw_fruit(food.position, CYBER_FRUITS[food.fruit_index], current_time)

        # Draw special food (completely separate from regular food)
        if special_food.active:
            draw_special_fruit(special_food.position, current_time)

        # Draw snake with updated effects
        for i, pos in enumerate(snake.positions):
            is_head = i == 0
            is_tail = i == len(snake.positions) - 1
            next_pos = snake.positions[i-1] if i > 0 else pos
            
            # Handle prev_pos calculation safely
            if is_tail:
                if len(snake.positions) >= 2:
                    prev_pos = snake.positions[-2]  # Use second-to-last segment for tail
                else:
                    prev_pos = (pos[0] - snake.direction[0], pos[1] - snake.direction[1])  # Use direction for single-segment snake
            else:
                prev_pos = snake.positions[i+1]
            
            # Determine color based on effects
            special_color = snake.get_special_color(current_time)
            if special_color:
                color = special_color
            elif snake.is_segment_gold(current_time):
                color = GOLD_COLOR
            else:
                color = CYBER_COLORS[i % len(CYBER_COLORS)]
            
            draw_snake_segment(screen, pos, next_pos, prev_pos, is_head, is_tail, color)

        # Draw score with cyber font and glow
        try:
            font = pygame.font.Font("font/Orbitron-Bold.ttf", 36)
        except:
            font = pygame.font.Font(None, 36)
        score_text = f'SCORE: {score}'
        glow = font.render(score_text, True, NEON_BLUE)
        main = font.render(score_text, True, NEON_GREEN)
        screen.blit(glow, (12, 12))
        screen.blit(main, (10, 10))

        if game_over:
            fade_alpha = min(fade_alpha + 0.05, 1.0)  # Gradually increase alpha
            draw_game_over(fade_alpha)
        else:
            fade_alpha = 0

        # Draw milestone flash if active
        if milestone_flash:
            if not milestone_flash.draw(screen, current_time):
                milestone_flash = None

        pygame.display.flip()
        clock.tick(current_speed)

    # Show cursor again when game ends
    pygame.mouse.set_visible(True)

if __name__ == '__main__':
    main()