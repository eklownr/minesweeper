import pygame
import random


class Cell:
    """This file contains the self class representing each square in the game"""

    def __init__(self, x, y, width, height, bomb_chance):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (0, 64, 110)  
        self.selected_color = (0, 200, 255)
        self.cell_thickness = 2
        self.neighbouring_bombs = 0
        self.selected = False
        self.flag = False
        self.NUM_FONT = pygame.font.SysFont("Arial", 36)

        self.cell_center = (
            self.x + self.width // 2,
            self.y + self.width // 2,
        )  # useful for drawing
        self.bomb = (
            random.random() < bomb_chance
        )  # each self has a chance of being a bomb


    def draw(self, screen):
        """This method is called in the main.py files draw_cells fkn"""

        if self.selected == False:
            rect = pygame.Rect(self.x * self.width, self.y * self.height, self.width -4, self.height -4)
            pygame.draw.rect(screen, self.color, rect)

        if self.selected == True and self.bomb == True:
            text = self.NUM_FONT.render("X",1 , (255,0,0))
            screen.blit(text, (self.x * self.width + self.width // 2 - text.get_width() // 2 ,
                            self.y * self.width + self.width // 2 - text.get_height() // 2 ))

        if self.selected == True and self.bomb == False:
            rect = pygame.Rect(self.x * self.width, self.y * self.height, self.width -4, self.height -4)
            pygame.draw.rect(screen, self.selected_color, rect)
            text = self.NUM_FONT.render(str(self.neighbouring_bombs),1 , self.color)
            screen.blit(text, (self.x * self.width + self.width // 2 - text.get_width() // 2 ,
                            self.y * self.width + self.width // 2 - text.get_height() // 2 ))