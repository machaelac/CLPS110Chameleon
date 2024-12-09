import pygame
import random
import time
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
MID = 148
DIFF = 20
GREENS =  [(17, MID - DIFF, 71), (17, MID, 71), (17, MID + DIFF, 71)]
BRIGHTS = [(34, 139, 34), (0, 255, 0), (144, 238, 144)]  # Brighter greens
DULLS = [(0, 48, 0), (0, 100, 0), (56, 79, 15)]  # Duller greens
BACKGROUND_GREEN = (44, 168, 104)

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
game_started = False

cameron = Chameleon.Chameleon(SWIDTH // 2, SHEIGHT // 2 + 100, None, 250)
female1 = Chameleon.Chameleon(1 * (SWIDTH // 4), 50 + (SHEIGHT // 4), None, 100)
female2 = Chameleon.Chameleon(2 * (SWIDTH // 4), 50 + (SHEIGHT // 4), None, 100)
female3 = Chameleon.Chameleon(3 * (SWIDTH // 4), 50 + (SHEIGHT // 4), None, 100)


def start_game():
    global game_started, running
    game_started = True
    running = True

def home_screen():
    global game_started

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
                button.click() 
                if game_started:  
                    waiting_for_input = False

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
        cameron.draw(screen)

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
 
def draw_chameleons():
    screen.fill(BACKGROUND_GREEN)
    branch_background = pygame.transform.scale(pygame.image.load('branch_image.jpeg'), (SWIDTH, SHEIGHT))
    screen.blit(branch_background, (0, 125))

    cameron.draw(screen)
    female1.draw(screen)
    female2.draw(screen)
    female3.draw(screen)

def round1():
    # randomly select the receptive female
    random.shuffle(GREENS)

    female1.change_color(GREENS[0])
    female2.change_color(GREENS[1])
    female3.change_color(GREENS[2])

    most_receptive = 1
    if GREENS[1][1] == (MID + DIFF):
        most_receptive = 2
    if GREENS[2][1] == (MID + DIFF):
        most_receptive = 3

    while running:
        draw_chameleons()

        instructions = fontMB.render("Select the female most interested in Cameron", True, BLACK)
        screen.blit(instructions, (SWIDTH // 2 - instructions.get_width() // 2, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Female 1?
                if female1.body_rect.collidepoint(mouse_pos):       
                    if most_receptive == 1:
                        print("YAYYY")
                        return True 
                    return False 
                # Female 2?
                elif female2.body_rect.collidepoint(mouse_pos):
                    if most_receptive == 2:
                        print("YAYYY")
                        return True 
                    return False 
                # Female 3?
                elif female3.body_rect.collidepoint(mouse_pos):
                    if most_receptive == 3:
                        print("YAYYY")
                        return True 
                    return False 
                
        pygame.display.flip()
        clock.tick(FPS)



def game1_logic(level):
    global game_started, collision

    # Initialize chameleons
    chameleonL = Chameleon.Chameleon(Chameleon.SIZE, SHEIGHT // 2, level, facing_right=True)
    chameleonR = Chameleon.Chameleon(SWIDTH - Chameleon.SIZE, SHEIGHT // 2, level, facing_right=False)

    # Predetermined answers
    winner = random.choice(["L", "R"])
    approacher = random.choice(["L", "R"])

    delay = round(delays[level - 1] * 1000)
    stripe_diff = stripe_diffs[level - 1]

    rand_green = random.choice(BRIGHTS)
    alt_green = rand_green[0], rand_green[1] - stripe_diff, rand_green[2]
    if approacher == "L":
        chameleonL.stripe_color = rand_green
        chameleonR.stripe_color = alt_green
    else:
        chameleonR.stripe_color = rand_green
        chameleonL.stripe_color = alt_green

    part1 = True

    color_changed = False
    save_time = None

    start_ticks = None
    while game_started:
        if part1:
            draw_chameleons(chameleonL, chameleonR)
            question = fontLB.render("Which chameleon will approach first?", True, BLACK)
            screen.blit(question, (SWIDTH // 2 - question.get_width() // 2, 75))
            pygame.display.update()

            # Await choice
            player_answer = None
            while player_answer == None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            player_answer = "L"
                        elif event.key == pygame.K_RIGHT:
                            player_answer = "R"

            # Evaluate player's answer
            if player_answer != approacher:
                response_ticks = pygame.time.get_ticks()
                while pygame.time.get_ticks() - response_ticks < 3000:
                    draw_chameleons(chameleonL, chameleonR)

                    result = fontSB.render("Wrong! The brighter striped chameleon approaches first.", True, BLACK)
                    screen.blit(result, (SWIDTH // 2 - result.get_width() // 2, 75))

                    pygame.display.update()
                return False        

            response_ticks = pygame.time.get_ticks()
            while pygame.time.get_ticks() - response_ticks < 3000:
                draw_chameleons(chameleonL, chameleonR)

                result = fontSB.render("Correct! The brighter striped chameleon approaches first.", True, BLACK)
                screen.blit(result, (SWIDTH // 2 - result.get_width() // 2, 75))

                pygame.display.update()

            # Now enter the contest round
            response_ticks = pygame.time.get_ticks()
            while pygame.time.get_ticks() - response_ticks < 5000:
                screen.fill(WHITE)
                contest_text1 = "Uh oh, they're still approaching to battle."
                contest_text2 = "Click on the one who is most likely to win the fight"
                contest_prompt1 = fontMB.render(contest_text1, True, BLACK)
                contest_prompt2 = fontMB.render(contest_text2, True, BLACK)
                screen.blit(contest_prompt1, (SWIDTH // 2 - contest_prompt1.get_width() // 2, 100))
                screen.blit(contest_prompt2, (SWIDTH // 2 - contest_prompt2.get_width() // 2, 200))   
                pygame.display.update()
            part1 = False
            start_ticks = pygame.time.get_ticks()

        else:
            draw_chameleons(chameleonL, chameleonR)

            if pygame.time.get_ticks() - start_ticks >= 1000:
                if color_changed == False:
                    if winner == "L":
                        chameleonL.head_color = BRIGHTS[1]
                    else:
                        chameleonR.head_color = BRIGHTS[1]
                    color_changed = True
                    save_time = pygame.time.get_ticks()

                if color_changed == True:
                    if pygame.time.get_ticks() - save_time >= delay:
                        if winner == "L":
                            chameleonR.head_color = BRIGHTS[1]
                        else:
                            chameleonL.head_color = BRIGHTS[1]
                
                chameleonL.move_towards()
                chameleonR.move_towards()

                draw_chameleons(chameleonL, chameleonR)

                # Check if both chameleons have reached the targets
                if abs(chameleonL.x - chameleonL.invisible_wall) < 7 and abs(chameleonR.x - chameleonR.invisible_wall) < 7:
                    collision = True
                    return False

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
        clock.tick(FPS)

    return False  # If something goes wrong, end game

# _________________________&&&&&&&&&&&&&&&&&&__________________________ #

home_screen()
intro()

round1()

while running:
    screen.fill(WHITE)
    win_text = fontLB.render("You Win! Game Over.", True, GREEN)
    screen.blit(win_text, (SWIDTH // 2 - win_text.get_width() // 2, SHEIGHT // 2 - win_text.get_height() // 2))
    pygame.display.update()
    time.sleep(3)
    running = False  # End game after level 5

pygame.quit()
