import pickle
import random

import neat
from config import SCREEN_WIDTH, BLACK, SPEED_INCREMENT, \
    GROUND_LEVEL, OBSTACLE_SPEED, WHITE, BROWN, LIGHT_BLUE, BLUE, \
    SCREEN_HEIGHT
from resources import screen, clock, font, pygame
from obstacle import Obstacle
from resources import logging

class Game:

    def __init__(self, show_fps, custom_obstacle_speed, fps, config_path):
        logging.info("Initializing game...")
        self.fps = fps
        self.running = True
        self.pause = False
        self.score = 0
        if custom_obstacle_speed is None:
            self.obstacle_speed = OBSTACLE_SPEED
            self.original_obstacle_speed = OBSTACLE_SPEED
        else:
            self.obstacle_speed = custom_obstacle_speed
            self.original_obstacle_speed = custom_obstacle_speed
        self.dinos = []
        self.config_path = config_path
        self.obstacles = []
        self.high_score = 0
        self.spacing = 0
        self.show_fps = show_fps
        self.generation = 0
        self.WIN = 0
        self.generation = 0
        self.nets = []
        self.ge = []

        self.background_day = pygame.image.load('textures/desert_day/desert_day_background.png').convert_alpha()
        self.background_day_flipped = pygame.transform.flip(self.background_day, True, False).convert_alpha()
        self.background_day_2 = pygame.image.load('textures/desert_day/desert_day_background_2.png').convert_alpha()
        self.background_day_2_flipped = pygame.transform.flip(self.background_day_2, True, False).convert_alpha()
        self.background_day_3 = pygame.image.load('textures/desert_day/desert_day_background_3.png').convert_alpha()
        self.background_day_3_flipped = pygame.transform.flip(self.background_day_3, True, False).convert_alpha()
        self.background_day_4 = pygame.image.load('textures/desert_day/desert_day_background_4.png').convert_alpha()
        self.background_day_4_flipped = pygame.transform.flip(self.background_day_4, True, False).convert_alpha()

        self.background_night = pygame.image.load('textures/desert_night/desert_night_background.png').convert_alpha()
        self.background_night_flipped = pygame.transform.flip(self.background_night, True, False).convert_alpha()
        self.background_night_2 = pygame.image.load('textures/desert_night/desert_night_background_2.png').convert_alpha()
        self.background_night_2_flipped = pygame.transform.flip(self.background_night_2, True, False).convert_alpha()
        self.background_night_3 = pygame.image.load('textures/desert_night/desert_night_background_3.png').convert_alpha()
        self.background_night_3_flipped = pygame.transform.flip(self.background_night_3, True, False).convert_alpha()
        self.background_night_4 = pygame.image.load('textures/desert_night/desert_night_background_4.png').convert_alpha()
        self.background_night_4_flipped = pygame.transform.flip(self.background_night_4, True, False).convert_alpha()

        self.game_over_image = pygame.image.load('textures/texts/game_over.png')

        self.background_flip = True
        self.background_flip_2 = True
        self.background_flip_3 = True
        self.background_flip_4 = True
        self.background_x = 0
        self.background_x_2 = 0
        self.background_x_3 = 0
        self.background_x_4 = 0

        self.progress_birds = 0
        self.birds_score = 5000
        self.progress_day = 0
        self.day_score = 5600
        self.progress_sky = 0
        self.sky_score = 10000
        self.progress_smoothed = 0

        self.night_to_day_transition = False
        self.night_to_day_transition_progress = 0
        self.night_to_day_transition_speed = 0.02
        logging.info("Prepared game")

    def reset(self):
        self.running = True
        self.pause = False
        self.score = 0
        self.obstacle_speed = self.original_obstacle_speed
        from dino import Dino
        self.dino = Dino()
        self.obstacles.clear()
        self.spacing = 0

        self.background_flip = True
        self.background_flip_2 = True
        self.background_flip_3 = True
        self.background_flip_4 = True
        self.background_x = 0
        self.background_x_2 = 0
        self.background_x_3 = 0
        self.background_x_4 = 0

        self.progress_birds = 0
        self.birds_score = 5000
        self.progress_day = 0
        self.day_score = 5600
        self.progress_sky = 0
        self.sky_score = 10000
        self.progress_smoothed = 0

        self.night_to_day_transition = False
        self.night_to_day_transition_progress = 0
        self.night_to_day_transition_speed = 0.01
        logging.info("Game was reset and prepared")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                logging.info("Exit")

    def update(self):
        if self.pause:
            return

        for dino in self.dinos:
            dino.update(self.score)

        if not self.pause:
            self.background_x -= self.obstacle_speed * 0.20
            if self.background_x <= -SCREEN_WIDTH - 800:
                self.background_x = 0
                self.background_flip = not self.background_flip
            self.background_x_2 -= self.obstacle_speed * 0.25
            if self.background_x_2 <= -SCREEN_WIDTH - 800:
                self.background_x_2 = 0
                self.background_flip_2 = not self.background_flip_2
            self.background_x_3 -= self.obstacle_speed * 0.50
            if self.background_x_3 <= -SCREEN_WIDTH - 800:
                self.background_x_3 = 0
                self.background_flip_3 = not self.background_flip_3
            self.background_x_4 -= self.obstacle_speed
            if self.background_x_4 <= -SCREEN_WIDTH - 800:
                self.background_x_4 = 0
                self.background_flip_4 = not self.background_flip_4

            self.progress_birds = min((self.score + self.progress_smoothed) / self.birds_score, 1)
            self.progress_day = min((self.score + self.progress_smoothed) / self.day_score, 1)
            self.progress_sky = min((self.score + self.progress_smoothed) / self.sky_score, 1)
            if self.score < 100:
                self.progress_smoothed = self.progress_smoothed + 0.5
            else:
                self.progress_smoothed = self.progress_smoothed + 0.9


        if not self.obstacles or self.obstacles[-1].x < SCREEN_WIDTH - random.randint(600, 800) - self.spacing:
            self.spacing += 2.5
            self.obstacles.append(Obstacle(self.score))
            logging.debug(f"Placed new obstacle")

        if -300 >= self.background_x:
            self.night_to_day_transition = True

        if self.background_x <= -500 and (self.night_to_day_transition_progress == 1 or self.night_to_day_transition_progress == 0) :
            self.night_to_day_transition = False

        if self.night_to_day_transition:
            if 5000 <= self.score <= 7000:
                self.night_to_day_transition_progress = min(
                    self.night_to_day_transition_progress + self.night_to_day_transition_speed, 1)


        for obstacle in self.obstacles[:]:
            obstacle.update(self.obstacle_speed)

            if obstacle.complete_off_screen():
                logging.debug(f"Obstacle complete off screen: {obstacle.x + obstacle.width[0] < 0}")
                self.obstacles.remove(obstacle)
                logging.debug("Removed obstacle")

            if obstacle.off_screen() and not obstacle.got_counted:
                logging.debug(f"Obstacle off screen: {obstacle.x + obstacle.width[0] < 0}")
                obstacle.got_counted = True
                self.score += 100
                self.progress_smoothed = 0
                for genome in self.ge:
                    genome.fitness += 5

                logging.info(f"Score: {self.score}")

            self.obstacle_speed += SPEED_INCREMENT

    def draw(self):
        if not self.background_flip:
            screen.blit(self.background_night_flipped, (self.background_x, 0))
            screen.blit(self.background_night, (self.background_x + SCREEN_WIDTH + 800, 0))
        else:
             screen.blit(self.background_night, (self.background_x, 0))
             screen.blit(self.background_night_flipped, (self.background_x + SCREEN_WIDTH + 800, 0))

        if not self.background_flip_2:
            screen.blit(self.background_night_2_flipped, (self.background_x_2, 410))
            screen.blit(self.background_night_2, (self.background_x_2 + SCREEN_WIDTH + 800, 410))
        else:
            screen.blit(self.background_night_2, (self.background_x_2, 410))
            screen.blit(self.background_night_2_flipped, (self.background_x_2 + SCREEN_WIDTH + 800, 410))

        if not self.background_flip_3:
            screen.blit(self.background_night_3_flipped, (self.background_x_3, 500))
            screen.blit(self.background_night_3, (self.background_x_3 + SCREEN_WIDTH + 800, 500))
        else:
            screen.blit(self.background_night_3, (self.background_x_3, 500))
            screen.blit(self.background_night_3_flipped, (self.background_x_3 + SCREEN_WIDTH + 800, 500))


        if not self.background_flip_4:
            screen.blit(self.background_night_4_flipped, (self.background_x_4, GROUND_LEVEL - 80))
            screen.blit(self.background_night_4, (self.background_x_4 + SCREEN_WIDTH + 800, GROUND_LEVEL - 80))
        else:
            screen.blit(self.background_night_4, (self.background_x_4, GROUND_LEVEL - 80))
            screen.blit(self.background_night_4_flipped, (self.background_x_4 + SCREEN_WIDTH + 800, GROUND_LEVEL - 80))

        self.background_day.set_alpha(int(self.night_to_day_transition_progress * 255))
        self.background_day_flipped.set_alpha(int(self.night_to_day_transition_progress * 255))
        if not self.background_flip:
            screen.blit(self.background_day_flipped, (self.background_x, 0))
            screen.blit(self.background_day, (self.background_x + SCREEN_WIDTH + 800, 0))
        else:
            screen.blit(self.background_day, (self.background_x, 0))
            screen.blit(self.background_day_flipped, (self.background_x + SCREEN_WIDTH + 800, 0))

        self.background_day_2.set_alpha(int(self.night_to_day_transition_progress * 255))
        self.background_day_2_flipped.set_alpha(int(self.night_to_day_transition_progress * 255))
        if not self.background_flip_2:
            screen.blit(self.background_day_2_flipped, (self.background_x_2, 410))
            screen.blit(self.background_day_2, (self.background_x_2 + SCREEN_WIDTH + 800, 410))
        else:
            screen.blit(self.background_day_2, (self.background_x_2, 410))
            screen.blit(self.background_day_2_flipped, (self.background_x_2 + SCREEN_WIDTH + 800, 410))

        self.background_day_3.set_alpha(int(self.night_to_day_transition_progress * 255))
        self.background_day_3_flipped.set_alpha(int(self.night_to_day_transition_progress * 255))
        if not self.background_flip_3:
            screen.blit(self.background_day_3_flipped, (self.background_x_3, 500))
            screen.blit(self.background_day_3, (self.background_x_3 + SCREEN_WIDTH + 800, 500))
        else:
            screen.blit(self.background_day_3, (self.background_x_3, 500))
            screen.blit(self.background_day_3_flipped, (self.background_x_3 + SCREEN_WIDTH + 800, 500))

        self.background_day_4.set_alpha(int(self.night_to_day_transition_progress * 255))
        self.background_day_4_flipped.set_alpha(int(self.night_to_day_transition_progress * 255))
        if not self.background_flip_4:
            screen.blit(self.background_day_4_flipped, (self.background_x_4, GROUND_LEVEL - 80))
            screen.blit(self.background_day_4, (self.background_x_4 + SCREEN_WIDTH + 800, GROUND_LEVEL - 80))
        else:
            screen.blit(self.background_day_4, (self.background_x_4, GROUND_LEVEL - 80))
            screen.blit(self.background_day_4_flipped, (self.background_x_4 + SCREEN_WIDTH + 800, GROUND_LEVEL - 80))

        for obstacle in self.obstacles:
            obstacle.draw()

        for dino in self.dinos:
            dino.draw()

        color = WHITE if self.pause else BLACK

        if self.pause:
            screen.fill(BLACK)
            pause_text = font.render("Paused", True, WHITE)
            continue_text = font.render("Press space to continue", True, WHITE)
            escape_text = font.render("Press escape to exit", True, WHITE)
            restart_text = font.render("Press enter to start from beginning", True, WHITE)
            hard_restart_text = font.render("Press backspace to change account", True, WHITE)
            screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))
            screen.blit(continue_text, continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
            screen.blit(escape_text, escape_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
            screen.blit(hard_restart_text, hard_restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))

        score_text = font.render(f"Score: {self.score}", True, color)
        screen.blit(score_text, (10, 10))
        highest_score_text = font.render(f"High Score: {max(self.score, self.high_score)}", True, color)
        screen.blit(highest_score_text, (10, 35))

        if not self.pause:
            rect_surface = pygame.Surface((SCREEN_WIDTH // 2, 50), pygame.SRCALPHA)
            rect_surface.set_alpha(128)
            rect_surface.fill(WHITE)
            screen.blit(rect_surface, (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, 10))

            pygame.draw.rect(screen, BROWN,
                             (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, 10, self.progress_birds * SCREEN_WIDTH // 2, 50))
            pygame.draw.rect(screen, BLUE,
                             (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, 10, self.progress_day * SCREEN_WIDTH // 2, 50))
            pygame.draw.rect(screen, LIGHT_BLUE,
                             (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, 10, self.progress_sky * SCREEN_WIDTH // 2, 50))
            pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, 10, SCREEN_WIDTH // 2, 50), 2)

        if self.show_fps:
            fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, color)
            screen.blit(fps_text, (SCREEN_WIDTH - 110, 10))

        pygame.display.flip()

    def run(self):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    self.config_path)

        p = neat.Population(config)

        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        winner = p.run(self.run_with_neat, 100000)

        print('\nBest genome:\n{!s}'.format(winner))


    def run_with_neat(self, genomes, config):
        self.generation += 1
        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.nets.append(net)
            from dino import Dino
            self.dinos.append(Dino())
            self.ge.append(genome)

        while self.running:
            self.handle_events()
            if self.neat_update():
                break
            self.update()
            self.draw()
            clock.tick(self.fps)
        pygame.quit()

    def neat_update(self):
        for x, dino in enumerate(self.dinos):
            # Rewarding dinos slightly for staying alive
            self.ge[x].fitness += 0.1

            # Find the next obstacle that the dino will encounter
            next_obstacle = None
            for obstacle in self.obstacles:
                if obstacle.x + obstacle.width[0] > dino.x:
                    next_obstacle = obstacle
                    break

            if next_obstacle:
                # Inputs to the neural network: dino's vertical position, the obstacle's distance, and height difference
                inputs = (
                    dino.y,
                    next_obstacle.x - dino.x,
                    next_obstacle.height[0] - dino.y
                )
                output = self.nets[self.dinos.index(dino)].activate(inputs)

                # Decision to jump based on the neural network's output
                if output[0] > 0.5:
                    dino.start_jump()

        # Check for collisions with obstacles
        for obstacle in self.obstacles:
            for dino in self.dinos:
                if obstacle.collides_with(dino):
                    # Penalize dinos that collide with obstacles
                    self.ge[self.dinos.index(dino)].fitness -= 1
                    self.nets.pop(self.dinos.index(dino))
                    self.ge.pop(self.dinos.index(dino))
                    self.dinos.pop(self.dinos.index(dino))

        # Handle dinos that go out of bounds (fall or jump too high)
        for dino in self.dinos:
            if dino.y + dino.height - 10 >= GROUND_LEVEL or dino.y < -50:
                # Remove the dino if it goes out of bounds
                self.nets.pop(self.dinos.index(dino))
                self.ge.pop(self.dinos.index(dino))
                self.dinos.pop(self.dinos.index(dino))

        # End the game if a goal score is reached
        if self.score > 20000:
            pickle.dump(self.nets[0], open("best.pickle", "wb"))
            return True

        return False