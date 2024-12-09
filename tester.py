import pygame
import random
import time
import sys
import Chameleon
import Button

# Initialize pygame & set up screen
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Chameleon Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)
BRIGHTS = [(34, 139, 34), (0, 255, 0), (144, 238, 144)]  # Shades of green
DULLS = [(0, 48, 0), (0, 100, 0), (56, 79, 15)]  # Duller greens
RED = (255, 0, 0)

# Font for text
fontS = pygame.font.SysFont("couriernew", 15)
fontM = pygame.font.SysFont("couriernew", 25)
fontL = pygame.font.SysFont("couriernew", 35)


# Game variables
clock = pygame.time.Clock()
running = True
game_started = False
collision = False
level = 1  # Start at level 1
max_level = 5
delays = [0.5, 0.25, 0.125, 0.0625, 0.01]

# Countdown screen
def countdown_screen():
    for i in range(3, 0, -1):
        screen.fill(WHITE)
        countdown_text = fontL.render(f"{i}", True, GREEN)
        screen.blit(countdown_text, (275, 150))
        pygame.display.update()

def draw_chameleons(c1, c2):
    background = pygame.image.load('branch.jpeg')
    background = pygame.transform.scale(background, (600, 400))
    screen.blit(background, (0, 0))
    c1.draw(screen)
    c2.draw(screen)
    pygame.display.update()

# Main game function
def game(level):
    global game_started
    global collision

    # Countdown before objects appear
    countdown_screen()

    chameleonL = Chameleon.Chameleon(100, 400 // 2, facing_right=True)
    chameleonR = Chameleon.Chameleon(500, 400 // 2, facing_right=False)

    # Set the delay times based on level
    delay = delays[level - 1]

    # Which object is expected to be selected
    winner = random.choice(["L", "R"])
    brighter = (0,255,0)

    start_ticks = pygame.time.get_ticks()

    while game_started:
        draw_chameleons(chameleonL, chameleonR)

        elapsed_time = pygame.time.get_ticks() - start_ticks

        if elapsed_time >= 1000:
            if winner == "L":
                chameleonL.head_color = brighter
                draw_chameleons(chameleonL, chameleonR)

                time.sleep(delay)

                chameleonR.head_color = brighter
                draw_chameleons(chameleonL, chameleonR)

            else:
                chameleonR.head_color = brighter
                draw_chameleons(chameleonL, chameleonR)

                time.sleep(delay)

                chameleonL.head_color = brighter
                draw_chameleons(chameleonL, chameleonR)

            chameleonL.move_towards()
            chameleonR.move_towards()

            draw_chameleons(chameleonL, chameleonR)

            # Check if both chameleons have reached the targets
            if abs(chameleonL.x - 225) < 5 and abs(chameleonR.x - 375) < 5:
                collision = True
                break

            # Handle events (mouse click)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if the user clicks on object 1
                    if chameleonL.body_rect.collidepoint(mouse_pos):       
                        if winner == "L":
                            print(f"You selected object 1 at level {level}!")
                            return True 
                        return False 

                    # Check if the user clicks on object 2
                    elif chameleonR.body_rect.collidepoint(mouse_pos):
                        if winner == "R":
                            print(f"You selected object 2 at level {level}!")
                            return True 
                        return False 

        pygame.display.update()
        clock.tick(30)

    return False  # If something goes wrong, end game

# Function to show Game Over message
def game_over(message):
    screen.fill(WHITE)
    text = "Game Over: " + message
    game_over_text = fontS.render(text, True, BLACK)
    screen.blit(game_over_text, (50, 150))
    pygame.display.update()
    time.sleep(2)

def start_game():
    global game_started
    game_started = True
    print("Game Started!")

# Home Screen Function
def home_screen():
    global game_started
    screen.fill(WHITE)
    title_text = fontL.render("Chameleon Countdown", True, GREEN)
    help_text = fontS.render("To win: Click on the chameleon who will win the faceoff!", True, BLACK)
    help2_text = fontS.render("Choose wisely and quickly... a chameleon's life is in your hands!", True, BLACK)

    image = pygame.image.load('cute_chameleon.jpg')
    image = pygame.transform.scale(image, (600, 200))
    screen.blit(image, (0, 200))
    screen.blit(title_text, (100, 50))
    screen.blit(help_text, (50, 100))
    screen.blit(help2_text, (5, 125))

    start_button = Button.Button(200, 150, 25, 200, 50, "Start Game", start_game)
    start_button.draw(screen)

    pygame.display.update()

    # Wait for the player to press the button
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_input = False
                game_started = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_button.click()  # Check if button is clicked
                if game_started:  # If game is started after click, break the loop
                    waiting_for_input = False

# Game loop
while running:
    if not game_started:
        home_screen()
    else:
        if level <= max_level:
            if not game(level):
                running = False  # End game if incorrect selection (Game Over)
                if collision:
                    game_over("The chameleons fought :(")
                else:
                    game_over("You picked the wrong chameleon :(")
            else:
                level += 1  # Move to next level
        else:
            screen.fill(WHITE)
            win_text = fontL.render("You Win! Game Over.", True, GREEN)
            screen.blit(win_text, (150, 150))
            pygame.display.update()
            time.sleep(2)
            running = False  # End game after level 5

pygame.quit()
