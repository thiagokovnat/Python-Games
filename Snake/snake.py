import pygame

class Snake:

    def __init__(self, screen, screenWidth, screenHeight):
        self.snakeBody = []
        self.bodyCount = 1
        self.x = 200
        self.y = 200
        self.screen = screen
        self.snakeBody.append((self.x, self.y))
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.xDirection = 10
        self.yDirection = 0

    def move(self, xDirection, yDirection):
        self.xDirection = xDirection
        self.yDirection = yDirection

    def draw(self):

        for rect in self.snakeBody:
            pygame.draw.rect(self.screen, pygame.Color(255, 255, 255), [rect[0], rect[1], 10, 10])

    def update(self):
        self.x += self.xDirection
        self.y += self.yDirection

        if self.x < 0 or self.x >= self.screenWidth or self.y < 0 or self.y >= self.screenHeight:
            return False

        newBody = (self.x, self.y)

        for bodyPart in self.snakeBody:
            if bodyPart == newBody:
                return False

        self.snakeBody.append(newBody)

        if self.bodyCount < len(self.snakeBody):
            del self.snakeBody[0]
        
        return True

    def eatFood(self):
        self.bodyCount += 1

        
