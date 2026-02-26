import pygame
from asteroidfield import AsteroidField  
from logger import log_state, log_event
from constants import *
from shot import Shot
from player import Player
from asteroid import Asteroid
import sys
import os

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'r') as file:
            high_score = file.read()
            return int(high_score) if high_score.isdigit() else 0
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(score))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, FONT_SIZE)
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    high_score = load_high_score()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group() 
    shots = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable,)
    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    while True:
        log_state()
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        updatable.update(dt)
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                print(f"High score is {high_score}")
                print(f"Your score is {score}")
                if score > high_score:
                    save_high_score(score)
                sys.exit()
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
                    score += 100
        for obj in drawable:
            obj.draw(screen)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 50))
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
