import pygame

class Player():
    def __init__(self, x, y, width , height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.velocity = 3

    def get_color(self):
        return self.color

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_pos(self):
        return (self.x, self.y)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.y += self.velocity

        if keys[pygame.K_UP]:
            self.y -= self.velocity

        if keys[pygame.K_RIGHT]:
            self.x += self.velocity

        if keys[pygame.K_LEFT]:
            self.x -= self.velocity

        po = pygame.mouse.get_pressed()
        if po[0]:
            mPos = pygame.mouse.get_pos()
            if (self.x <= mPos[0] and mPos[0] <= self.x + self.width) and (self.y <= mPos[1] and mPos[1] <= self.y + self.height):
                self.color = (0,0,255)
            else:
                self.color = (0,255,0)


        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)