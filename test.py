import pygame, random
# from icecream import ic
# icecream till testutskrifter:


pygame.init()

# Hämta användarens skärmstorlek och använd 90 % av skärmhöjden
info = pygame.display.Info() 
SCREEN_SIZE = int(info.current_h * 0.9)

GRID_SIZE = 16
BOMB_CHANCE = 0.25

CELL_SIZE = SCREEN_SIZE // GRID_SIZE  # how large can each cell be?
READJUSTED_SIZE = CELL_SIZE * GRID_SIZE

SCREEN_WIDTH, SCREEN_HEIGHT = READJUSTED_SIZE, READJUSTED_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Spelet startar upp med en random grå färg
GRAY = (random.randrange(77, 99) ,random.randrange(77, 99) ,random.randrange(77, 99))
WHITE = (240, 240, 255)
GREEN = (0, 120, 40)
DARK_BLUE = (0, 20, 40)
RED = (255 , 0, 10)
GREEN = (0, 90, 30)
YELLOW = (233, 200, 0)

NUM_FONT = pygame.font.SysFont("Arial", 36)

# TODO: skapa funktion som kollar en inbäddad lista med alla flaggor med positioner
BOMB_FLAG = [0, 0, False]

# Skapar alla celler 16x16 och en 16x16 matris som döljer värderna under
cells = [[x for x in range(GRID_SIZE)] for x in range(GRID_SIZE)]
visable = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def add_bombs():
    # Lägger in bomber i cellerna med ett X
    for row in cells:
        for cell in row:
            bomb = random.random() < BOMB_CHANCE
            if bomb:
                row[cell] = "X"


def set_bomb_neighbour_value():
    ''' Räknar antalet bomber'''
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            # Om cellen inte är en bomb, räkna antalet närliggande bomber
            if cells[x][y] != "X":
                bomb_count = 0
                # loopar en rad före och en rad efter
                for i in range(-1, 2):
                    # loopar en cell före och efter
                    for j in range(-1, 2):
                        # Kontrollera, en cell i taget, att granncellen är inom rutnätet
                        '''  Kontrollera:
                        1, om x + i är större än eller lika med 0 (för att vara inom rutnätet i x-led).
                        2, om x + i är mindre än GRID_SIZE (för att vara inom rutnätet i x-led).
                        3, om y + j är större än eller lika med 0 (för att vara inom rutnätet i y-led).
                        4, om y + j är mindre än GRID_SIZE (för att vara inom rutnätet i y-led).
                        5, Slutligen Om alla ovanstående villkor är uppfyllda, fortsätt till nästa steg. 
                        Annars, fortsätt med nästa iteration av loopen. '''
                        if x + i >= 0 and x + i < GRID_SIZE and y + j >= 0 and y + j < GRID_SIZE:
                            # Om granncellen är en bomb, öka räknaren (kollar även cellen du klickat på)
                            if cells[x + i][y + j] == "X":
                                bomb_count += 1
                # Sätt cellens värde till antalet närliggande bomber
                cells[x][y] = bomb_count


def draw_grid_and_value(screen):
    # Rita rutnätet och cellernas innehåll
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            # Ritar alla celler som vit bakgrund
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE -4, CELL_SIZE -4)
            pygame.draw.rect(screen, WHITE, rect)

            # Visa cellens värde
            cell_value = cells[x][y]
            if cell_value == 0:
                text = NUM_FONT.render(str(cell_value),1 , GREEN)
            elif cell_value != "X":
                text = NUM_FONT.render(str(cell_value), 1, DARK_BLUE)
            else:
                text = NUM_FONT.render(str(cell_value),1 , RED)
            # Cellens värde visas i rätt position och färg
            screen.blit(text, (x * CELL_SIZE + CELL_SIZE // 2 - text.get_width() // 2, 
                               y * CELL_SIZE + CELL_SIZE // 2 - text.get_height() // 2))

            # Täcker för alla celler. Visar bara synliga
            if visable[x][y] == False:
                # Täck för celler som inte är synliga
                rect_hide = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 4, CELL_SIZE -4)
                pygame.draw.rect(screen, GRAY, rect_hide)


def get_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Vänsterklick
            pos = pygame.mouse.get_pos()
            x = pos[0] // CELL_SIZE
            y = pos[1] // CELL_SIZE
            visable[x][y] = True
            if cells[x][y] == "X":
                print("Booomb!!!")

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Högerklick
            pos = pygame.mouse.get_pos()
            x = pos[0] // CELL_SIZE
            y = pos[1] // CELL_SIZE

            # En redan skapad flagga, tas bort
            if BOMB_FLAG[0] == x and BOMB_FLAG[1] == y and BOMB_FLAG[2] == True:
                BOMB_FLAG[2] = False
            else: 
                BOMB_FLAG[2] = True
                BOMB_FLAG[0] = x
                BOMB_FLAG[1] = y


def show_bomb_flag(BOMB_FLAG):
        pygame.draw.circle(screen, YELLOW, (BOMB_FLAG[0] * CELL_SIZE + CELL_SIZE // 2,  
                                         BOMB_FLAG[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
    

def main():
    # Lägger till alla bomber i matrisen celler
    add_bombs()
    # Lägger till alla värden runt bomberna i matrisen celler
    set_bomb_neighbour_value()
    
    while True:
        screen.fill(DARK_BLUE)

        get_event()
        draw_grid_and_value(screen)

        # TODO: skapa funktion som kollar en inbäddad lista med alla flaggor med positioner
        if BOMB_FLAG[2] == True:
            show_bomb_flag(BOMB_FLAG)

        pygame.display.flip()


if __name__ == "__main__":
    main()
