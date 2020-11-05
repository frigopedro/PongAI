import pygame
import random

white = (236, 240, 241)
black = (0,0,0)
try:
    pygame.init()
except:
    print("O modulo nao foi iniciado corretamente")

width, height = 1024, 768

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong by Pedro and Leo')
font = pygame.font.SysFont(None, 30)
#Players
def Player1(p1x, p1y):
  pygame.draw.rect(screen, white, [p1x, p1y, 10, 150])

def Player2(p2x, p2y):
  pygame.draw.rect(screen, white, [p2x, p2y, 10, 150])
#Ball
def Ball(bx, by):
  pygame.draw.circle(screen, white,[bx,by], 5 )

def Scores(msg, sx, sy):
  text = font.render(msg, True, white)
  screen.blit(text, [sx,sy])

def main():
  sair = True
  p1x = 10
  p1y = height/2

  p2x = width -20
  p2y = height/2

  bx = width/ 2
  by = height/ 2

  ball_speed_x = 1
  ball_speed_y = 1

  points_p1 = 0
  points_p2 = 0
  while sair:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sair = False

      #Player 1 Controls  
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
          p1y += 20
        if event.key == pygame.K_w:
          p1y -= 20
      #Player 2 Controls
      if event.type == pygame.KEYDOWN:
        print('a')
        if event.key == pygame.K_UP:
          p2y -= 20
        if event.key == pygame.K_DOWN:
          p2y += 20
    
    
    screen.fill(black)
    Player1(p1x, p1y)
    Player2(p2x, p2y)
    Ball(bx,by)
    # Scores
    Scores(f'{points_p1}', width/2-30, 20)
    Scores(f'{points_p2}', width/2+20, 20)

    pygame.draw.line(screen, white, (width/2, 0),( width/2, height))
    pygame.display.update()

    

    # Ball Movements
    bx += 1 * ball_speed_x
    by += 1 * ball_speed_y

    #Collisions
      # Ball enviroment collisions
    if bx >= width:
      ball_speed_x = -1
    if by >= height:
      ball_speed_y = -1

    if bx <= 0:
      ball_speed_x = 1
    if by <= 0:
      ball_speed_y = 1
      #Players environment collision
    if p1y <= 0:
      p1y += 10
    if p1y+ 150 >= height:
      p1y -= 10
    
    if p2y <= 0:
      p2y += 10
    if p2y+ 150 >= height:
      p2y -= 10
      #Players and ball collision
    if by <= p1y+150 and by > p1y:
      if bx == p1x+10:
        ball_speed_x = 1
        points_p1 += 1
    if by <= p2y+150 and by > p2y:
      if bx == p2x-10:
        ball_speed_x = -1
        points_p2 += 1
main()