import sys
import os
from random import randint
import pygame
import neat

WIDTH = 1024
HEIGHT = 768
GEN = 0
WIN_ON = True

pygame.init()
STAT_FONT = pygame.font.SysFont("comicsans", 40)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("AI Pong by Pedro Maia and Leonardo Rocha")

class Player:
    def __init__(self, x_c, y_c, color):
        self.x_c = x_c
        self.y_c = y_c
        self.vel = 0
        self.color = color
        self.width = 5
        self.height = 100
        self.rect = pygame.Rect(self.x_c,self.y_c,self.width,self.height)

    def move_up(self):
        self.vel = -5

    def move_down(self):
        self.vel = 5

    def move_stop(self):
        self.vel = 0

    def move(self):
        if self.rect.top <= 0 and self.vel < 0:
            self.vel = 0
        elif self.rect.bottom >= HEIGHT and self.vel > 0:
            self.vel = 0

        self.rect = self.rect.move([0,self.vel])

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def get_y(self):
        return self.rect.y

    def get_x(self):
        return self.rect.x

class Ball:
    def __init__(self, x_c, y_c, color):
        self.x_c = x_c
        self.y_c = y_c
        self.vel = [1*4,-1*4]
        self.color = color
        self.width = 10
        self.rect = pygame.Rect(self.x_c,self.y_c,self.width,self.width)

    def change_vel_y(self):
        self.vel[1] = -self.vel[1]

    def change_vel_x(self):
        self.vel[0] = -self.vel[0]

    def move(self):
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.change_vel_y()
        self.rect = self.rect.move([self.vel[0],self.vel[1]])

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def collide(self, player):
        return self.rect.colliderect(player)



def draw_window(screen, players,  balls, hy):
    screen.fill((0,0,0))
    for ball in balls:
        ball.draw(screen)
    for player in players:
        player.draw(screen)


    score_label = STAT_FONT.render("Geração: " + str(GEN-1),1,(255,255,255))
    screen.blit(score_label, (10, 10))
    Human(WIDTH-10, hy)
    pygame.display.flip()
    

def Human(hx, hy):
    pygame.draw.rect(screen, (255,255,255), [hx, hy, 5, 150])

def eval_genomes(genomes, config):
    global GEN
    global WIN_ON
    GEN += 1
    score = 0

    players = []
    balls = []
    nets = [] 
    ge = [] 

    hy = HEIGHT/2
    
    for genome_id, g in genomes:
        tmp_color = (randint(0,255),randint(0,255),randint(0,255))
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        players.append(Player(0,240,tmp_color))
    
        balls.append(Ball(WIDTH/2,HEIGHT/2, (255,255,255)))
        g.fitness = 0
        ge.append(g)

    clock = pygame.time.Clock()

    run = True
    while run and len(players) > 0:
        if WIN_ON: clock.tick(90)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    hy += 50
                if event.key == pygame.K_w:
                    hy -= 50
        

        for x_c, player in enumerate(players):
            
            ge[x_c].fitness += 0.05
            player.move()

            
            outputs = nets[players.index(player)].activate((player.get_y(),
                                    abs(player.get_x() - balls[players.index(player)].rect.x),
                                    balls[players.index(player)].rect.y))

            if outputs[0] > outputs[1]:
                if outputs[0] > 0.5:
                    player.move_up()
                else:
                    player.move_stop()
            elif outputs[1] > 0.5:
                player.move_down()
            else:
                player.move_stop()
    
    
        for ball in balls:
            if ball.collide(players[balls.index(ball)]):
                ball.change_vel_x()
                ge[balls.index(ball)].fitness += 5
                score += 1

            if ball.get_x() > WIDTH-10:
                if ball.get_y() > hy and ball.get_y() < hy+150:
                    ball.change_vel_x()

            ball.move()
            if ball.get_x() < 0 or ball.get_x() > WIDTH:
                #check if player misses ball
                ge[balls.index(ball)].fitness -= 2
                nets.pop(balls.index(ball))
                ge.pop(balls.index(ball))
                players.pop(balls.index(ball))
                balls.pop(balls.index(ball))

            


        if WIN_ON:
            draw_window(screen, players, balls, hy)

        if score > 500:
            break

def run(config_file):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 1000)

    print('\nMelhor Genoma:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)

