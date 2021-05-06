import pygame
import sys
from snake import Snake
from random import randrange

def checkCollision(food, snake):

    print(f"""Snake x: {snake.x}, Snake y: {snake.y}, food x: {food[0]}, food y: {food[1]} """)

    if food[0] == snake.x and food[1] == snake.y:
        return True 

    return False

def generateRandomFood(width, height):
    foodx = round(randrange(0, width - 10) / 10.0) * 10.0
    foody = round(randrange(0, width - 10) / 10.0) * 10.0
    return (foodx, foody)

def draw(screen, food):
     pygame.draw.rect(screen, (255, 0 ,0), [food[0], food[1], 10, 10])

pygame.init()
pygame.display.set_caption("Snake")
width = 800
height = 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
snake = Snake(screen, width, height)
food = generateRandomFood(width, height)


while True:

    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            break 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                    snake.move(-10, 0)
            if event.key == pygame.K_RIGHT:
                    snake.move(10, 0)
            if event.key == pygame.K_UP:
                    snake.move(0, -10)
            if event.key == pygame.K_DOWN:
                    snake.move(0, 10)
            if event.key == pygame.K_SPACE: 
                    snake.eatFood()

            

    if not snake.update():
        print("Collision detected, you lost")
        break 

    draw(screen, food)
    snake.draw()
    pygame.display.update()

    if checkCollision(food, snake):
        snake.eatFood()
        food = generateRandomFood(width, height)


   
    clock.tick(15)

        