import pygame
import sys
import random
from dino_ai_game import Dino, Obstacle, Bird, WIDTH, HEIGHT, GROUND_Y, FPS
from dino_ai_game import draw_window

def run_reflex_agent():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
    pygame.display.set_caption("Reflex Agent Mode")
    clock = pygame.time.Clock()

    base_jump_velocity = -20
    base_duck_duration = 140
    base_jump_duration = 30
    dino = Dino(jump_velocity=base_jump_velocity)
    dino.jump_duration = base_jump_duration
    obstacles = []
    birds = []
    speed = 5
    score = 0
    font = pygame.font.SysFont(None, 24)

    def spawn_obstacle():
        if random.random() < 0.7:
            obstacles.append(Obstacle(speed))
        else:
            birds.append(Bird(speed))

    frame_count = 0
    duck_timer = 0
    run = True
    while run:
        screen.fill((255, 255, 255))
        frame_count += 1
        score += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Calculate dynamic speed modifiers
        speed_multiplier = 1 + (score // 700) * 0.2
        dino.jump_duration = int(base_jump_duration * speed_multiplier)
        dino.jump_velocity = int(base_jump_velocity * (1 + (score // 700) * 0.1))
        current_duck_duration = int(base_duck_duration * (1 + (score // 700) * 0.15))

        jump_threshold = 120
        duck_threshold = 90

        nearest_obstacle = None
        if obstacles:
            nearest_obstacle = min(obstacles, key=lambda obs: obs.x)

        nearest_bird = None
        if birds:
            nearest_bird = min(birds, key=lambda b: b.x)

        action = "none"
        if nearest_obstacle:
            distance = nearest_obstacle.x - dino.x
            if 0 < distance < jump_threshold:
                action = "jump"

        if nearest_bird:
            distance = nearest_bird.x - dino.x
            if 0 < distance < jump_threshold:
                if nearest_bird.y > HEIGHT - 120:
                    action = "jump"
                elif HEIGHT - 160 < nearest_bird.y <= HEIGHT - 120:
                    action = "duck"

        if duck_timer > 0:
            dino.duck()
            duck_timer -= 1
        else:
            if action == "jump":
                dino.jump()
                dino.unduck()
            elif action == "duck":
                dino.duck()
                duck_timer = int(40 * speed_multiplier)  # matches dynamic duck duration
            else:
                dino.unduck()

        # Update Dino
        dino.update(score)

        # Update Obstacles
        for obs in obstacles:
            obs.update(score)
        obstacles = [obs for obs in obstacles if obs.x + obs.width > 0]

        # Update Birds
        for bird in birds:
            bird.update(score)
        birds = [bird for bird in birds if bird.x + bird.width > 0]

        # Collision Detection
        for obs in obstacles:
            if dino.collides_with(obs):
                run = False
        for bird in birds:
            if dino.collides_with(bird):
                run = False

        draw_window(screen, dino, obstacles, birds, score, font)
        # Spawn new obstacle
        if frame_count % 90 == 0:
            spawn_obstacle()

        pygame.display.update()
        clock.tick(FPS)

    with open("scores_reflex.txt", "a") as f:
        f.write(f"{score}\n")
    pygame.quit()

    sys.exit()


if __name__ == "__main__":
    run_reflex_agent()
