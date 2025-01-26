import pygame
from pygame.locals import *
import time
import random

SIZE = 40
background_color = (11, 179, 72)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("a.jpg.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self, snake_x, snake_y):
        while True:
            self.x = random.randint(0, (800 // SIZE) - 1) * SIZE
            self.y = random.randint(0, (500 // SIZE) - 1) * SIZE
            # Ensure apple does not overlap with the snake
            if (self.x, self.y) not in zip(snake_x, snake_y):
                break

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("b.jpg.jpg").convert()
        self.direction = 'down'
        self.length = 3  # Start length is 3
        self.x = [40] * self.length
        self.y = [40] * self.length

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # Update body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # Update head
        if self.direction == 'left':
            self.x[0] = self.x[0] - SIZE
        if self.direction == 'right':
            self.x[0] = self.x[0] + SIZE
        if self.direction == 'up':
            self.y[0] = self.y[0] - SIZE
        if self.direction == 'down':
            self.y[0] = self.y[0] + SIZE

        self.draw()

    def draw(self):
        self.parent_screen.fill(background_color)
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake And Apple Game")
        self.surface = pygame.display.set_mode((800, 500))
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.snake.draw()
        self.apple.draw()
        self.score = 0
        self.speed = 0.2  # Faster initial speed

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.score = 0
        self.speed = 0.3  # Reset speed

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # Snake eats apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move(self.snake.x, self.snake.y)
            self.score += 1
            self.speed = max(0.05, self.speed - 0.01)  # Increase speed

        # Snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise Exception("Collision Occurred")

        # Collision with window boundaries
        if not (0 <= self.snake.x[0] < 800 and 0 <= self.snake.y[0] < 500):
            raise Exception("Hit the boundary error")

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score_text = font.render(f"Score: {self.score}", True, (200, 200, 200))
        self.surface.blit(score_text, (690, 10))

    def show_game_over(self):
        self.surface.fill(background_color)
        font = pygame.font.SysFont('times new roman', 30)
        line1 = font.render(f"Game Over! Your score is: {self.score}", True, (255, 255, 255))
        self.surface.blit(line1, (195, 220))
        line2 = font.render("Press Enter to Play Again or Escape to Exit.", True, (255, 255, 255))
        self.surface.blit(line2, (125, 250))
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(self.speed)

if __name__ == '__main__':
    game = Game()
    game.run()
