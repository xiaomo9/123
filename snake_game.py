#!/usr/bin/env python3
"""
贪吃蛇小游戏
使用方向键控制蛇的移动
"""

import pygame
import sys
import random
import time

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# 方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = self.direction  # 添加方向缓冲
        self.score = 0
        self.grow_to = 3

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        head = self.get_head_position()
        # 使用下一个方向
        self.direction = self.next_direction
        x, y = self.direction
        new_position = (((head[0] + x) % GRID_WIDTH), ((head[1] + y) % GRID_HEIGHT))

        # 检查是否撞到自己
        if new_position in self.positions[1:]:
            return False

        self.positions.insert(0, new_position)

        if len(self.positions) > self.grow_to:
            self.positions.pop()

        return True

    def grow(self):
        self.grow_to += 1
        self.score += 10

    def change_direction(self, direction):
        # 防止反向移动，但可以设置下一个方向
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
            return True
        return False

    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            color = GREEN if i == 0 else BLUE  # 蛇头绿色，身体蓝色
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)  # 边框

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

def draw_grid(surface):
    for y in range(0, GRID_HEIGHT):
        for x in range(0, GRID_WIDTH):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, GRAY, rect, 1)

def show_game_over(screen, score):
    font = pygame.font.SysFont('Arial', 50)
    text = font.render('Game Over!', True, RED)
    score_text = font.render(f'Score: {score}', True, WHITE)

    screen.fill(BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

    restart_font = pygame.font.SysFont('Arial', 30)
    restart_text = restart_font.render('Press SPACE to restart or ESC to quit', True, WHITE)
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))

    pygame.display.update()

def show_score(screen, score):
    font = pygame.font.SysFont('Arial', 25)
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (5, 5))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('贪吃蛇游戏')
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        # 重新开始游戏
                        snake = Snake()
                        food = Food()
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        if not game_over:
            # 处理键盘事件队列中的所有事件，提高响应性
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_UP]:
                snake.change_direction(UP)
            elif keys_pressed[pygame.K_DOWN]:
                snake.change_direction(DOWN)
            elif keys_pressed[pygame.K_LEFT]:
                snake.change_direction(LEFT)
            elif keys_pressed[pygame.K_RIGHT]:
                snake.change_direction(RIGHT)

            # 更新蛇的位置
            if not snake.update():
                game_over = True

            # 检查是否吃到食物
            if snake.get_head_position() == food.position:
                snake.grow()
                food.randomize_position()
                # 确保食物不出现在蛇身上
                while food.position in snake.positions:
                    food.randomize_position()

        # 绘制游戏
        screen.fill(BLACK)
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)
        show_score(screen, snake.score)

        if game_over:
            show_game_over(screen, snake.score)

        pygame.display.update()
        clock.tick(15)  # 提高游戏速度，让转向更及时

if __name__ == '__main__':
    main()