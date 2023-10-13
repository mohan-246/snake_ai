import pygame
from collections import namedtuple
import random

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
BLOCK_SIZE = 20
SPEED = 10
Point = namedtuple('Point', 'x, y')
font = pygame.font.SysFont('arial', 25)

class Snake:
    def __init__(self):
        self.w , self.h = screen_width , screen_height
        self.clock = pygame.time.Clock()

        self.direction = 1
        self.head = Point(self.w/2 , self.h/2)
        self.snake = [self.head , 
                      Point(self.head.x - BLOCK_SIZE , self.head.y),
                      Point(self.head.x - (2*BLOCK_SIZE) , self.head.y)]
        self.score = 0
        self.food = None
        self.place_food()
    
    def place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self.place_food()
    
    def play_step(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = 3
                elif event.key == pygame.K_RIGHT:
                    self.direction = 1
                elif event.key == pygame.K_UP:
                    self.direction = 0
                elif event.key == pygame.K_DOWN:
                    self.direction = 2
        self.move(self.direction)
        self.snake.insert(0, self.head)

        game_over = False
        if self.is_collision():
            game_over = True
            return game_over , self.score
        
        if self.head == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop()

        self.update_ui()
        self.clock.tick(SPEED)

        return game_over , self.score

    def is_collision(self):
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0 :
            return True
        if self.head in self.snake[1:]:
            return True

        return False
    
    def update_ui(self):
        screen.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(screen , BLUE1 , pygame.Rect(pt.x , pt.y , BLOCK_SIZE , BLOCK_SIZE))
            pygame.draw.rect(screen, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(screen , RED , pygame.Rect(self.food.x , self.food.y , BLOCK_SIZE , BLOCK_SIZE))
        text = font.render("Score: " + str(self.score) , True , WHITE)
        screen.blit(text , [0 , 0])
        pygame.display.flip()

    def move(self , direction):
        x = self.head.x
        y = self.head.y

        if direction == 1:
            x += BLOCK_SIZE
        elif direction == 2:
            y += BLOCK_SIZE
        elif direction == 3:
            x -= BLOCK_SIZE
        else:
            y -= BLOCK_SIZE

        self.head = Point(x , y)

if __name__ == '__main__':
    game = Snake()
    
    # game loop
    while True:
        game_over, score = game.play_step()
        # print(game_over)
        if game_over == True:
            print("T")
            break
        
    print('Final Score', score)
        
        
    pygame.quit()