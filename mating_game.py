import pygame
import random
import sys
import Chameleon
import Button

# Initialize pygame & set up screen
pygame.init()
SWIDTH, SHEIGHT = 800, 600
FPS = 10
screen = pygame.display.set_mode((SWIDTH, SHEIGHT))
pygame.display.set_caption("Chameleon Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 100, 0)
DARK_GREEN = (0, 50, 0)
BRIGHT_GREEN = (0, 255, 0)
BACKGROUND_GREEN = (44, 168, 104)
MID = 148
level = 1
DIFFS = [50, 40, 30, 20, 10]
GREENS =  [(17, MID - DIFFS[level - 1], 71), (17, MID, 71), (17, MID + DIFFS[level - 1], 71)]

# Font for text
fontS = pygame.font.SysFont("couriernew", 15)
fontM = pygame.font.SysFont("couriernew", 25)
fontL = pygame.font.SysFont("couriernew", 35)
fontSB = pygame.font.SysFont("couriernew", 15, bold=True)
fontMB = pygame.font.SysFont("couriernew", 25, bold=True)
fontLB = pygame.font.SysFont("couriernew", 35, bold=True)


# Game variables
clock = pygame.time.Clock()
running = False
saved_color = None
cameron = Chameleon.Chameleon(SWIDTH // 2, SHEIGHT // 2 + 100, None, 250, None)


def start_game():
    global running, saved_color, cameron, level
    running = True
    saved_color = None
    level = 1
    cameron = Chameleon.Chameleon(SWIDTH // 2, SHEIGHT // 2 + 100, None, 250, None)


def home_screen():
    screen.fill(WHITE)

    chameleon_image = pygame.transform.scale(pygame.image.load('romance.jpeg'), (SWIDTH, SHEIGHT // 2 + 50))
    screen.blit(chameleon_image, (0, SHEIGHT // 2 - 50))

    title_text = fontLB.render("* Cameron's Courtship *", True, GREEN)
    help_text = fontSB.render("Interpret Veiled Chameleon mating behaviors to help Cameron find love!", True, BLACK)

    screen.blit(title_text, (SWIDTH // 2 - title_text.get_width() // 2, 75))
    screen.blit(help_text, (SWIDTH // 2 - help_text.get_width() // 2, 150))

    start_button = Button.Button(250, 200, 300, 75, RED, "Start Game", 35, start_game)
    start_button.draw(screen)

    pygame.display.flip()

    await_start(start_button)

def await_start(button):
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_input = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_input = False
                button.click() 
  
def game_over(message):
    screen.fill(BACKGROUND_GREEN)
    text = "Game Over: " + message
    game_over_text = fontMB.render(text, True, BLACK)
    screen.blit(game_over_text, (SWIDTH // 2 - game_over_text.get_width() // 2, 250))

    restart_button = Button.Button(250, 350, 300, 75, RED, "Play again", 35, start_game)
    restart_button.draw(screen)
    pygame.display.update()

    await_start(restart_button)

def intro():
    caption_strings = ["Meet Cameron!", "Cameron is lonely...", "and he is looking for love.", "Unfortunately, he has trouble with social signals...", "and, like most of us, he fears rejection.", "Can you help him find a match?"]

    for frame_num in range(len(caption_strings)):    
        screen.fill(BACKGROUND_GREEN)
        caption = fontMB.render(caption_strings[frame_num], True, BLACK)
        screen.blit(caption, (SWIDTH // 2 - caption.get_width() // 2, 150))
        cameron.draw(screen, False)

        if frame_num == (len(caption_strings) - 1):
            heart_image = pygame.transform.scale(pygame.image.load('heart.webp'), (SWIDTH // 6, SHEIGHT // 6))
            screen.blit(heart_image, (SWIDTH // 2 + 125, SHEIGHT // 2 - 75))

        pygame.display.flip()

        awaiting_press = True
        while awaiting_press:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        awaiting_press = False
    running = True
 
def draw_cameron(spots):
    screen.fill(BACKGROUND_GREEN)
    branch_background = pygame.transform.scale(pygame.image.load('branch_image.jpeg'), (SWIDTH, SHEIGHT))
    screen.blit(branch_background, (0, 125))
    level_text = fontMB.render(f"Level {level}", True, GREEN)
    screen.blit(level_text, (SWIDTH // 2 - level_text.get_width() // 2, 20))
    cameron.draw(screen, spots)

def mate_choice():
    global saved_color, GREENS

    # randomly select the receptive female
    random.shuffle(GREENS)
    f1 = Chameleon.Chameleon(1 * (SWIDTH // 4), 50 + (SHEIGHT // 4), None, 100, GREENS[0])
    f2 = Chameleon.Chameleon(2 * (SWIDTH // 4), 50 + (SHEIGHT // 4), None, 100, GREENS[1])
    f3 = Chameleon.Chameleon(3 * (SWIDTH // 4), 50 + (SHEIGHT // 4), None, 100, GREENS[2])
    females = [f1, f2, f3]

    receptive = None
    if f1.base_color[1] == (MID + DIFFS[level - 1]):
        receptive = 1
    elif f2.base_color[1] == (MID + DIFFS[level - 1]):
        receptive = 2
    else:
        receptive = 3

    cameron.change_color(BRIGHT_GREEN)
    cameron.bobbing = True

    while running:
        cameron.change_color(BRIGHT_GREEN)
        cameron.bobbing = True
        draw_cameron(True)

        for obj in females: obj.draw(screen, False)

        instructions = fontMB.render("Quick! Select the female most interested in Cameron.", True, BLACK)
        screen.blit(instructions, (SWIDTH // 2 - instructions.get_width() // 2, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if f1.body_rect.collidepoint(mouse_pos):       
                    saved_color = f1.base_color[1]
                    if receptive == 1: return True
                    return False
                elif f2.body_rect.collidepoint(mouse_pos):
                    saved_color = f2.base_color[1]
                    if receptive == 2: return True
                    return False
                elif f3.body_rect.collidepoint(mouse_pos):
                    saved_color = f3.base_color[1]
                    if receptive == 3: return True
                    return False
                
        pygame.display.flip()
        clock.tick(FPS)
    return False

def lovey_dovey():
    global cameron

    female = Chameleon.Chameleon(SWIDTH - Chameleon.SIZE, SHEIGHT // 2, 15, 100, DARK_GREEN, facing_right=False)
    female.change_color((17, saved_color, 71))
    cameron = Chameleon.Chameleon(Chameleon.SIZE, SHEIGHT // 2, 15, 100, BRIGHT_GREEN, facing_right=True)

    while abs(cameron.x - cameron.invisible_wall) >= 7 and abs(female.x - female.invisible_wall) >= 7:    
        cameron.move_towards()
        female.move_towards()
        draw_cameron(True)
        caption = fontMB.render("Awwww it's a match. Great job!", True, BLACK)
        screen.blit(caption, (SWIDTH // 2 - caption.get_width() // 2, 50))
        female.draw(screen, False)

        pygame.display.flip()
        clock.tick(FPS)

    start = pygame.time.get_ticks()

    while pygame.time.get_ticks() <= start + 3000:
        draw_cameron(True)
        female.draw(screen, False)
        caption = fontMB.render("Awwww it's a match. Great job!", True, BLACK)
        screen.blit(caption, (SWIDTH // 2 - caption.get_width() // 2, 50))
        heart_image = pygame.transform.scale(pygame.image.load('heart.webp'), (SWIDTH // 10, SHEIGHT // 10))
        screen.blit(heart_image, (SWIDTH // 2 - 50, SHEIGHT // 2 - 100))
        pygame.display.flip()


def display_aggression():
    global cameron
    # open mouth
    caption_strings = ["She is NOT interested.", "You've put Cameron in a very awkward situation.", "Better luck next time, buddy!"]
    female = Chameleon.Chameleon(SWIDTH - Chameleon.SIZE, SHEIGHT // 2, None, 100, DARK_GREEN, facing_right=False)
    female.change_color((17, saved_color, 71))
    cameron = Chameleon.Chameleon(Chameleon.SIZE, SHEIGHT // 2, None, 100, DARK_GREEN, facing_right=True)
    female.mad = True
    cameron.mad = True

    for frame_num in range(len(caption_strings)):    
        screen.fill(BACKGROUND_GREEN)
        draw_cameron(True)
        female.draw(screen, False)
        caption = fontMB.render(caption_strings[frame_num], True, BLACK)
        screen.blit(caption, (SWIDTH // 2 - caption.get_width() // 2, 50))

        pygame.display.flip()

        awaiting_press = True
        while awaiting_press:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        awaiting_press = False
    running = False


def game_loop():
    global level, GREENS, DIFFS, saved_color, cameron

    while level <= 5:
        # Update difficulty based on level
        cameron = Chameleon.Chameleon(SWIDTH // 2, SHEIGHT // 2 + 100, None, 250, None)
        GREENS = [(17, MID - DIFFS[level - 1], 71), (17, MID, 71), (17, MID + DIFFS[level - 1], 71)]
        
        # Proceed to mate choice
        if mate_choice():
            lovey_dovey()  # If correct choice, show match animation
            level += 1  # Move to the next level
        else:
            display_aggression()  # If wrong choice, show aggression screen

    # End of game (after level 5)
    game_over("You Win!")

# _________________________&&&&&&&&&&&&&&&&&&__________________________ #

# Start game
home_screen()
intro()

# Start the game loop with 5 levels
while True:
    game_loop()