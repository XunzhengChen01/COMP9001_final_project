import pygame
import random
import os # For constructing file paths robustly

# --- Constants ---
# Screen dimensions
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 720
FPS = 60

# Colors (RGB) - Still useful for text or fallback
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
# LIGHT_BLUE and GRAY might not be needed if images replace them fully

# Game grid
NUM_LANES = 3
NUM_ROWS = 6

LANE_WIDTH = SCREEN_WIDTH // NUM_LANES
ROW_HEIGHT = SCREEN_HEIGHT // NUM_ROWS

# Player properties
PLAYER_SIZE_W = LANE_WIDTH // 2 
PLAYER_SIZE_H = ROW_HEIGHT // 2 # Shortened player height
PLAYER_START_LANE = 1
PLAYER_START_ROW_FROM_BOTTOM = 2
PLAYER_Y_POSITION = SCREEN_HEIGHT - (PLAYER_START_ROW_FROM_BOTTOM * ROW_HEIGHT) + (ROW_HEIGHT // 2) - (PLAYER_SIZE_H // 2)

# Bullet properties
BULLET_WIDTH = 8
BULLET_HEIGHT = 20
BULLET_SPEED = 25
BULLET_COLOR = YELLOW # Bullet can remain a colored rectangle for now

# Obstacle properties
OBSTACLE_SIZE_W = LANE_WIDTH - 20
OBSTACLE_SIZE_H = ROW_HEIGHT - 10
OBSTACLE_SPEED = 3 # This will also be background scroll speed
OBSTACLE_SPAWN_INTERVAL_ROWS = 2
OBSTACLE_SPAWN_COOLDOWN_FRAMES = int((OBSTACLE_SPAWN_INTERVAL_ROWS * ROW_HEIGHT) / OBSTACLE_SPEED)

# Asset Paths
# Construct paths relative to the script's directory
script_dir = os.path.dirname(__file__) # Get the directory of the current script
ASSETS_DIR = os.path.join(script_dir, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

PLAYER_IMG_PATH = os.path.join(IMAGES_DIR, "player_ship.png")
METEORITE_IMG_PATH = os.path.join(IMAGES_DIR, "meteorite.png")
PIRATE_IMG_PATH = os.path.join(IMAGES_DIR, "pirate_ship.png")
BACKGROUND_IMG_PATH = os.path.join(IMAGES_DIR, "background.png")
MUSIC_PATH = os.path.join(SOUNDS_DIR, "background_music.mp3") # or .ogg

# --- Global variables for loaded assets (to avoid loading multiple times) ---
player_image_orig = None
meteorite_image_orig = None
pirate_image_orig = None
background_image = None

def load_assets():
    global player_image_orig, meteorite_image_orig, pirate_image_orig, background_image
    try:
        player_image_orig = pygame.image.load(PLAYER_IMG_PATH).convert_alpha()
        meteorite_image_orig = pygame.image.load(METEORITE_IMG_PATH).convert_alpha()
        pirate_image_orig = pygame.image.load(PIRATE_IMG_PATH).convert_alpha()
        background_image = pygame.image.load(BACKGROUND_IMG_PATH).convert() # Use .convert() for non-alpha bg
        
        # Background music
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.set_volume(0.5) # Adjust volume (0.0 to 1.0)
        pygame.mixer.music.play(loops=-1) # Play indefinitely

    except pygame.error as e:
        print(f"Error loading assets: {e}")
        print("Please ensure all asset files are in the correct 'assets' subdirectories.")
        pygame.quit()
        exit()

# --- Asset Scaling/Surface Functions ---
def get_player_surface():
    if player_image_orig:
        return pygame.transform.scale(player_image_orig, (PLAYER_SIZE_W, PLAYER_SIZE_H))
    else: # Fallback if image loading failed (though program should exit)
        surf = pygame.Surface((PLAYER_SIZE_W, PLAYER_SIZE_H))
        surf.fill((173, 216, 230)) # LIGHT_BLUE
        return surf

def get_meteorite_surface():
    if meteorite_image_orig:
        return pygame.transform.scale(meteorite_image_orig, (OBSTACLE_SIZE_W, OBSTACLE_SIZE_H))
    else:
        surf = pygame.Surface((OBSTACLE_SIZE_W, OBSTACLE_SIZE_H))
        surf.fill((128,128,128)) # GRAY
        return surf

def get_pirate_surface():
    if pirate_image_orig:
        return pygame.transform.scale(pirate_image_orig, (OBSTACLE_SIZE_W, OBSTACLE_SIZE_H))
    else:
        surf = pygame.Surface((OBSTACLE_SIZE_W, OBSTACLE_SIZE_H))
        surf.fill(RED)
        return surf

def get_bullet_surface(): # Bullet can remain a simple rectangle
    surf = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
    surf.fill(BULLET_COLOR)
    return surf

# --- Classes (Largely unchanged, they use the get_xxx_surface methods) ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = get_player_surface()
        self.rect = self.image.get_rect()
        self.current_lane = PLAYER_START_LANE
        self.rect.centerx = (self.current_lane + 0.5) * LANE_WIDTH
        self.rect.top = PLAYER_Y_POSITION

    def update(self):
        self.rect.centerx = (self.current_lane + 0.5) * LANE_WIDTH
        self.rect.top = PLAYER_Y_POSITION

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = get_bullet_surface()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, lane_index, image_surface, obs_type):
        super().__init__()
        self.image = image_surface # This will be the scaled image
        self.rect = self.image.get_rect()
        self.rect.centerx = (lane_index + 0.5) * LANE_WIDTH
        self.rect.bottom = 0
        self.type = obs_type

    def update(self):
        self.rect.y += OBSTACLE_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Meteorite(Obstacle):
    def __init__(self, lane_index):
        super().__init__(lane_index, get_meteorite_surface(), "meteorite")

class Pirate(Obstacle):
    def __init__(self, lane_index):
        super().__init__(lane_index, get_pirate_surface(), "pirate")

# --- Game Helper Functions ---
def draw_text(surface, text, size, x, y, color=WHITE, align="topright"):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "topright":
        text_rect.topright = (x, y)
    elif align == "center":
        text_rect.center = (x,y)
    surface.blit(text_surface, text_rect)

def spawn_obstacle_row():
    global score
    global first_row_spawned

    obstacle_types_in_row = []
    for _ in range(NUM_LANES):
        if random.random() < 0.6:
            obstacle_types_in_row.append("meteorite")
        else:
            obstacle_types_in_row.append("pirate")

    if all(ot == "meteorite" for ot in obstacle_types_in_row):
        change_index = random.randrange(NUM_LANES)
        obstacle_types_in_row[change_index] = "pirate"

    for lane_idx, obs_type in enumerate(obstacle_types_in_row):
        if obs_type == "meteorite":
            obstacle = Meteorite(lane_idx)
        else: # pirate
            obstacle = Pirate(lane_idx)
        
        all_sprites.add(obstacle)
        obstacles_group.add(obstacle)
        if isinstance(obstacle, Pirate):
            pirates_group.add(obstacle)
        # No need for meteorites_group if obstacles_group handles all player collisions
    
    if first_row_spawned:
        score += 1
    else:
        first_row_spawned = True

def show_game_over_screen(screen, final_score):
    # Stop music on game over screen or fade out
    pygame.mixer.music.fadeout(1000) # Fade out over 1 second

    # Create a semi-transparent overlay for the game over screen
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) # SRCALPHA for transparency
    overlay.fill((0, 0, 0, 180)) # Black with alpha 180 (0-255)
    screen.blit(overlay, (0,0))

    draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, RED, align="center")
    draw_text(screen, f"Final Score: {final_score}", 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, WHITE, align="center")
    draw_text(screen, "Press ANY KEY to play again", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4, WHITE, align="center")
    draw_text(screen, "or ESCAPE to quit", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4 + 30, WHITE, align="center")
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                # Restart music if playing again
                if background_image: # Check if assets were loaded
                    pygame.mixer.music.play(loops=-1)
                return True

# --- Pygame Initialization ---
pygame.init()
pygame.mixer.init() # Initialize mixer for sounds/music
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lane Dodger X - Enhanced")
clock = pygame.time.Clock()

# --- Load assets ONCE ---
load_assets() 

# --- Game Variables ---
all_sprites = None
# meteorites_group is not strictly needed if obstacles_group is used for all player-obstacle collisions
# pirates_group is for bullet-pirate collisions
obstacles_group = None 
pirates_group = None
bullets = None
player = None
score = 0
game_over = False
obstacle_spawn_timer = 0
first_row_spawned = False
background_scroll_y = 0 # For scrolling background

# --- Main Game Loop ---
running = True
restart_game = True

while running:
    if restart_game:
        all_sprites = pygame.sprite.Group()
        obstacles_group = pygame.sprite.Group()
        pirates_group = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)

        score = 0
        game_over = False
        obstacle_spawn_timer = 0
        first_row_spawned = False
        background_scroll_y = 0 # Reset scroll for new game
        
        # Ensure music is playing if it was stopped/faded
        if not pygame.mixer.music.get_busy() and background_image: # Check if assets loaded
             pygame.mixer.music.play(loops=-1)

        restart_game = False

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
            if not game_over:
                if event.key == pygame.K_SPACE:
                    player.shoot()

    if not game_over:
        # --- Player Lane Control ---
        keys_pressed = pygame.key.get_pressed()
        target_lane = 1 

        if keys_pressed[pygame.K_LEFT]:
            target_lane = 0
        elif keys_pressed[pygame.K_RIGHT]:
            target_lane = 2
        
        player.current_lane = target_lane
        
        # --- Update ---
        all_sprites.update()

        # Background Scroll
        if background_image:
            background_scroll_y = (background_scroll_y + OBSTACLE_SPEED) % background_image.get_height()

        # Obstacle Spawning
        obstacle_spawn_timer -= 1
        if obstacle_spawn_timer <= 0:
            spawn_obstacle_row()
            obstacle_spawn_timer = OBSTACLE_SPAWN_COOLDOWN_FRAMES

        # Collision Detection: Player vs Obstacles
        # Using collide_mask for more precise collision with transparent images
        # For this, Player and Obstacle classes need self.mask = pygame.mask.from_surface(self.image)
        # This is more complex, so let's stick to rect collision with ratio for now.
        # If your images have a lot of empty space, consider mask collision or tighter rects.
        collided_obstacles = pygame.sprite.spritecollide(player, obstacles_group, False, pygame.sprite.collide_rect_ratio(0.7)) # Adjust ratio if needed
        if collided_obstacles:
            game_over = True

        # Collision Detection: Bullets vs Pirates
        hits = pygame.sprite.groupcollide(pirates_group, bullets, True, True) # True, True kills both
        for _ in hits:
            score += 1

    # --- Drawing ---
    # Draw scrolling background first
    if background_image:
        # Draw two copies of the background to create a seamless scroll
        # Ensure your background_image is at least SCREEN_HEIGHT tall, or designed to tile
        bg_img_height = background_image.get_height()
        
        # Calculate y positions for the two background tiles
        # This method handles backgrounds of any height correctly for tiling
        y1 = background_scroll_y % bg_img_height
        y2 = (background_scroll_y % bg_img_height) - bg_img_height
        
        screen.blit(background_image, (0, y1))
        screen.blit(background_image, (0, y2))
    else:
        screen.fill(BLACK) # Fallback if no background image

    all_sprites.draw(screen) # Draw all game sprites (player, obstacles, bullets)
    draw_text(screen, f"Score: {score}", 24, SCREEN_WIDTH - 10, 10)

    # No need to flip here if game_over is true, show_game_over_screen will handle its own flip

    pygame.display.flip() # Update the full display
    clock.tick(FPS)

    # --- Post-frame Game Over Handling ---
    if game_over and running:
        should_restart = show_game_over_screen(screen, score) # This function now also stops music
        if should_restart:
            restart_game = True
            game_over = False
            # Music will be restarted at the beginning of the game loop if restart_game is True
        else:
            running = False

# --- Cleanup ---
pygame.quit()