import pygame
from collections import namedtuple
import random
import numpy as np

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
SPEED = 80
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
        self.place_food()
        self.frame_iteration = 0
        # self.maxu = self.maxd = self.head.y
        # self.maxl = self.maxr = self.head.x
        
        self.reset()
    
    def reset(self):
        self.w , self.h = screen_width , screen_height
        self.clock = pygame.time.Clock()

        self.direction = 1
        self.head = Point(self.w/2 , self.h/2)
        self.snake = [self.head , 
                      Point(self.head.x - BLOCK_SIZE , self.head.y),
                      Point(self.head.x - (2*BLOCK_SIZE) , self.head.y)]
        self.score = 0
        self.food = None
        self.frame_iteration = 0
        self.place_food()
        


    def place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self.place_food()
    
    def play_step(self , action):

        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self.move(action)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self.frame_iteration = 0
            reward = 100
            self.place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self.update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score
    
    def is_collision(self , pt = None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False
    
    def is_danger(self , pt):
        # if pt.x > self.maxl and pt.x < self.maxr and pt.y > self.maxu:
        #     return True
        # if pt.x > self.maxl and pt.x < self.maxr and pt.y < self.maxd:
        #     return True
        # if pt.x > self.maxl and pt.y < self.maxd and pt.y > self.maxu:
        #     return True
        # if pt.x < self.maxr and pt.y < self.maxd and pt.y > self.maxu:
        #     return True
        x, y = pt

    # Check up direction
        up_side = any((x, y - i) in self.snake for i in range(1, len(self.snake) + 1))

        # Check down direction
        down_side = any((x, y + i) in self.snake for i in range(1, len(self.snake) + 1))

        # Check left direction
        left_side = any((x - i, y) in self.snake for i in range(1, len(self.snake) + 1))

        # Check right direction
        right_side = any((x + i, y) in self.snake for i in range(1, len(self.snake) + 1))

        # If at least one side is surrounded, return True; otherwise, return False
        return up_side and down_side and left_side and right_side

        

    def update_ui(self):
        screen.fill(BLACK)
        self.frame_iteration += 1
        for pt in self.snake:
            pygame.draw.rect(screen , BLUE1 , pygame.Rect(pt.x , pt.y , BLOCK_SIZE , BLOCK_SIZE))
            pygame.draw.rect(screen, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            # if pt.x > self.maxr:
            #     self.maxr = pt.x
            # if pt.x < self.maxl:
            #     self.maxl = pt.x
            # if pt.y > self.maxd:
            #     self.maxd = pt.y
            # if pt.y < self.maxu:
            #     self.maxu = pt.y

        pygame.draw.rect(screen , RED , pygame.Rect(self.food.x , self.food.y , BLOCK_SIZE , BLOCK_SIZE))
        text = font.render("Score: " + str(self.score) , True , WHITE)
        screen.blit(text , [0 , 0])
        pygame.display.flip()

    def move(self , action):
        # [straight, right, left]

        clock_wise = [0 , 1 , 2, 3]
        idx = clock_wise.index(self.direction)
        # print(self.snake)
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == 1:
            x += BLOCK_SIZE
        elif self.direction == 2:
            y += BLOCK_SIZE
        elif self.direction == 3:
            x -= BLOCK_SIZE
        else:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


if __name__ == '__main__':
    game = Snake()
    
    # game loop
    while True:
        game_over, score = game.play_step()
        # print(game_over)
        if game_over == True:
            break
        
    print('Final Score', score)
        
        
    pygame.quit()