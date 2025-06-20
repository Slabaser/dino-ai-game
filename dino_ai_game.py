import pygame
import sys
import random
import time

pygame.init()

# Ekran ayarları
WIDTH, HEIGHT = 1000, 300
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino AI")
ground_image = pygame.image.load("assets/ground.png")
bird_images = [
    pygame.image.load("assets/berd.png"),
    pygame.image.load("assets/berd2.png")
]
ground_x = 0
clock = pygame.time.Clock()

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Dino
class Dino:
    def __init__(self, jump_velocity=-20):
        self.x = 50
        self.y = HEIGHT - 100
        self.w, self.h = 40, 50
        self.vel_y = 0
        self.jump_velocity = jump_velocity
        self.is_jumping = False
        self.run_images = [
            pygame.image.load("assets/dinorun0000.png"),
            pygame.image.load("assets/dinorun0001.png")
        ]
        self.jump_image = pygame.image.load("assets/dinoJump0000.png")
        self.duck_images = [
            pygame.image.load("assets/dinoduck0000.png"),
            pygame.image.load("assets/dinoduck0001.png")
        ]
        self.is_ducking = False
        self.image_index = 0
        self.image = self.run_images[0]
        self.dead_image = pygame.image.load("assets/dinodead0000.png")
        self.dead_image = pygame.transform.scale(self.dead_image, (self.run_images[0].get_width(), self.run_images[0].get_height()))
        self.is_dead = False

    def jump(self):
        if not self.is_jumping:
            self.vel_y = self.jump_velocity
            self.is_jumping = True

    def update(self, score):
        self.vel_y += 0.8 * get_dynamic_speed(score) / BASE_SPEED
        self.y += self.vel_y
        if self.y >= HEIGHT - 100:
            self.y = HEIGHT - 100
            self.is_jumping = False

        speed_factor = get_dynamic_speed(score) / BASE_SPEED

        if self.is_ducking and not self.is_jumping:
            self.image_index = (self.image_index + 0.1 * speed_factor) % len(self.duck_images)
            self.image = self.duck_images[int(self.image_index)]
        elif self.is_jumping:
            self.image = self.jump_image
        else:
            self.image_index = (self.image_index + 0.1 * speed_factor) % len(self.run_images)
            self.image = self.run_images[int(self.image_index)]

    def draw(self, win):
        if self.is_dead:
            win.blit(self.dead_image, (self.x, self.y))
        elif self.is_ducking:
            self.duck_offset = 35
            win.blit(self.image, (self.x, self.y + self.duck_offset))
        else:
            self.duck_offset = 0
            win.blit(self.image, (self.x, self.y - 5))

    def unduck(self):
        self.is_ducking = False

    def duck(self):
        if not self.is_ducking:
            self.is_ducking = True
            self.image_index = 0
            self.image = self.duck_images[self.image_index]
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = GROUND_Y + 20

    def get_rect(self):
        if self.is_ducking:
            return pygame.Rect(self.x + 5, self.y + 35, self.image.get_width() - 10, self.image.get_height() - 10)
        else:
            return pygame.Rect(self.x + 5, self.y - 5, self.image.get_width() - 10, self.image.get_height() - 10)

    def collides_with(self, obj):
        return self.get_rect().colliderect(obj.rect())

class Obstacle:
    def __init__(self, speed):
        self.x = WIDTH
        self.speed = speed
        self.image_choices = [
            pygame.image.load("assets/cactusSmall0000.png"),
            pygame.image.load("assets/cactusSmallMany0000.png"),
            pygame.image.load("assets/cactusBig0000.png")
        ]
        self.image = random.choice(self.image_choices)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.8), int(self.image.get_height() * 0.8)))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.y = HEIGHT - self.image.get_height()
        self.spawn_buffer = random.randint(1000, 1200)

    def update(self, score):
        self.x -= get_dynamic_speed(score)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Bird:
    def __init__(self, speed):
        self.x = WIDTH
        # Sequential cycling logic for bird height
        if not hasattr(Bird, "spawn_index"):
            Bird.spawn_index = 0
        heights = [HEIGHT - 80, HEIGHT - 155, HEIGHT - 220]
        self.y = heights[Bird.spawn_index % len(heights)]
        Bird.spawn_index += 1
        self.speed = speed
        self.images = bird_images
        self.image_index = 0
        self.image = self.images[0]
        self.frame_counter = 0
        self.width = self.image.get_width()
        self.spawn_buffer = random.randint(1000, 1200)

    def update(self, score):
        self.x -= get_dynamic_speed(score)
        self.frame_counter += 1
        if self.frame_counter % 10 == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def rect(self):
        return pygame.Rect(self.x + 5, self.y, self.image.get_width() - 10, self.image.get_height() - 25)


# Shared constants and functions for external use
FPS = 60
BASE_SPEED = 5

def get_dynamic_speed(score):
    """
    Görsel (engeller ve zemin) hızı, skor 700'de bir sabit artar.
    Dino'nun hareketleri de bu hız ile orantılı olarak değişmeli.
    """
    return BASE_SPEED + (score // 700)

GROUND_Y = HEIGHT - 30

def draw_window(screen, dino, obstacles, birds, score, font):
    global ground_x
    screen.fill(WHITE)

    ground_x -= get_dynamic_speed(score)
    if ground_x <= -ground_image.get_width():
        ground_x = 0

    screen.blit(ground_image, (ground_x, HEIGHT - ground_image.get_height()))
    screen.blit(ground_image, (ground_x + ground_image.get_width(), HEIGHT - ground_image.get_height()))

    dino.draw(screen)
    for obs in obstacles:
        obs.draw(screen)
    for bird in birds:
        bird.draw(screen)

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    if dino.is_dead:
        game_over_font = pygame.font.SysFont(None, 36)
        game_over_text = game_over_font.render("Game Over", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 70, HEIGHT // 2 - 30))

    pygame.display.update()


import sys

if __name__ == "__main__":
    from reflex_agent import run_reflex_agent
    from heuristic_agent import run_heuristic_agent

    print("Select mode:")
    print("r - Run Reflex Agent")
    print("h - Run Heuristic Agent")
    print("q - Quit")

    choice = input("Enter choice: ").strip().lower()

    if choice == 'r':
        run_reflex_agent()
    elif choice == 'h':
        run_heuristic_agent()
    else:
        print("Exiting.")
        sys.exit()
