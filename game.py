import random
import sys

import neat
from config import SCREEN_WIDTH, BLACK, SPEED_INCREMENT, \
    GROUND_LEVEL, OBSTACLE_SPEED, WHITE, \
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
        self.average_score = 0
        self.spacing = 0
        self.show_fps = show_fps
        self.generation = 0
        self.WIN = 0
        self.generation = 0
        self.best_fitness = 0
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
        self.save_score()
        self.score = 0
        self.obstacle_speed = self.original_obstacle_speed
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
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if self.fps != 60:
                        self.fps = 60
                    else:
                        self.fps = 10000
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    if event.key == pygame.K_1:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 1
                        logging.debug(f"Obstacle jump: 1")
                    if event.key == pygame.K_2:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 2
                        logging.debug(f"Obstacle jump: 2")
                    if event.key == pygame.K_3:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 5
                        logging.debug(f"Obstacle jump: 5")
                    if event.key == pygame.K_4:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 10
                        logging.debug(f"Obstacle jump: 10")
                    if event.key == pygame.K_5:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 20
                        logging.debug(f"Obstacle jump: 20")
                    if event.key == pygame.K_6:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 50
                        logging.debug(f"Obstacle jump: 50")
                    if event.key == pygame.K_7:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 100
                        logging.debug(f"Obstacle jump: 100")
                    if event.key == pygame.K_8:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 200
                        logging.debug(f"Obstacle jump: 200")
                    if event.key == pygame.K_9:
                        for obstacle in self.obstacles:
                            obstacle.x = obstacle.x - 500
                        logging.debug(f"Obstacle jump: 500")

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
            self.spacing += 6
            self.obstacles.append(Obstacle(self.score))
            logging.debug(f"Placed new obstacle")

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

            for x, dino in enumerate(self.dinos):
                if obstacle.collides_with(dino):
                    self.best_fitness = max(self.best_fitness, self.ge[x].fitness)
                    self.ge[self.dinos.index(dino)].fitness -= 2
                    self.nets.pop(self.dinos.index(dino))
                    self.ge.pop(self.dinos.index(dino))
                    self.dinos.pop(self.dinos.index(dino))

            self.obstacle_speed += SPEED_INCREMENT

    def draw(self):
        if not self.background_flip:
            screen.blit(self.background_day_flipped, (self.background_x, 0))
            screen.blit(self.background_day, (self.background_x + SCREEN_WIDTH + 800, 0))
        else:
            screen.blit(self.background_day, (self.background_x, 0))
            screen.blit(self.background_day_flipped, (self.background_x + SCREEN_WIDTH + 800, 0))
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
        average_score_text = font.render(f"Average Score: {round(self.average_score, 1)}", True, color)
        screen.blit(average_score_text, (10, 35))
        highest_score_text = font.render(f"High Score: {max(self.score, self.high_score)}", True, color)
        screen.blit(highest_score_text, (10, 60))
        best_fitness_text = font.render(
            f"Best fitness this round: {round(max(genome.fitness for genome in self.ge), 1) if self.ge else 0} | Gen: {self.generation}",
            True, color)
        screen.blit(best_fitness_text, (10, 85))
        all_best_fitness_text = font.render(f"Best fitness all time: {round(self.best_fitness, 1) if self.ge else 0} | Gen: {self.generation}",
            True, color)
        screen.blit(all_best_fitness_text, (10, 110))
        alive_text = font.render(f"Alive: {len(self.dinos)}", True, color)
        screen.blit(alive_text, (10, 135))

        if self.show_fps:
            fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, color)
            screen.blit(fps_text, (SCREEN_WIDTH - 110, 10))

        pygame.display.flip()

    def save_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

        self.average_score = self.average_score + (self.score - self.average_score) / self.generation
        self.average_score = round(self.average_score, 0)

    def run(self):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    self.config_path)

        p = neat.Population(config)

        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        winner = p.run(self.run_with_neat)

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
                self.reset()
                break
            self.update()
            self.draw()
            clock.tick(self.fps)


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
                obstacle_type = 0
                if next_obstacle.type == "small":
                    obstacle_type = 1
                if next_obstacle.type == "large":
                    obstacle_type = 2
                if next_obstacle.type == "double":
                    obstacle_type = 3
                # Inputs to the neural network: dino's vertical position, the obstacle's distance, and height difference
                inputs = (
                    dino.y,
                    next_obstacle.x - dino.x,
                    next_obstacle.height[0] - dino.y,
                    next_obstacle.y[0],
                    obstacle_type
                )
                output = self.nets[self.dinos.index(dino)].activate(inputs)

                # Decision to jump based on the neural network's output
                if output[0] > 0.5:
                    dino.start_jump()

        # Check for collisions with obstacles
        for obstacle in self.obstacles:
            for x, dino in enumerate(self.dinos):
                if obstacle.collides_with(dino):
                    self.best_fitness = max(self.best_fitness, self.ge[x].fitness)
                    self.ge[self.dinos.index(dino)].fitness -= 2
                    self.nets.pop(self.dinos.index(dino))
                    self.ge.pop(self.dinos.index(dino))
                    self.dinos.pop(self.dinos.index(dino))

        if len(self.dinos) == 0:
            logging.info("No dinos left, ending the game.")
            return True

        return False