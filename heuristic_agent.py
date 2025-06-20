import pygame
import sys
import random
from dino_ai_game import Dino, Obstacle, Bird, draw_window, WIDTH, HEIGHT, GROUND_Y, FPS

def run_heuristic_agent():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Heuristic Agent Mode")
    clock = pygame.time.Clock()

    dino = Dino(jump_velocity=-22)
    obstacles = []
    birds = []
    BASE_SPEED = 5
    speed = BASE_SPEED
    score = 0
    font = pygame.font.SysFont(None, 24)

    duck_timer = 0

    def spawn_obstacle():
        if random.random() < 0.7:
            obstacles.append(Obstacle(speed))
        else:
            birds.append(Bird(speed))

    frame_count = 0
    run = True
    while run:
        screen.fill((255, 255, 255))
        frame_count += 1
        score += 1
        speed = BASE_SPEED + (score // 700)
        base_jump_velocity = -20
        speed_multiplier = 1 + (score // 700) * 0.1
        dino.jump_velocity = int(base_jump_velocity * speed_multiplier)
        dino.jump_duration = int(20 * speed_multiplier)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Heuristic Agent Logic
        jump_threshold = 120
        duck_threshold = 90

        nearest_obstacle = None
        if obstacles:
            nearest_obstacle = min(obstacles, key=lambda obs: obs.x)

        nearest_bird = None
        if birds:
            nearest_bird = min(birds, key=lambda b: b.x)

        # Determine action
        action = "none"
        if nearest_obstacle:
            distance = nearest_obstacle.x - dino.x
            if 0 < distance < jump_threshold:
                action = "jump"

        # Updated bird logic
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
                base_duck_duration = 40
                duck_timer = int(base_duck_duration * speed_multiplier)
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

        # Spawn new obstacle
        if frame_count % 90 == 0:
            spawn_obstacle()

        draw_window(screen, dino, obstacles, birds, score, font)
        pygame.display.update()
        clock.tick(FPS)

    # Save score to file
    try:
        with open("scores_heuristic.txt", "a") as f:
            f.write(str(score) + "\n")
    except Exception as e:
        print("Failed to save score:", e)

    pygame.quit()
    sys.exit()
