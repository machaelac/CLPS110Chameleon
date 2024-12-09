import pygame
import random
import time
import sys
import Chameleon
import Button

# Initialize pygame & set up screen
pygame.init()
SWIDTH, SHEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((SWIDTH, SHEIGHT))
pygame.display.set_caption("Chameleon Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 100, 0)
BRIGHTS = [(34, 139, 34), (0, 255, 0), (144, 238, 144)]  # Brighter greens
DULLS = [(0, 48, 0), (0, 100, 0), (56, 79, 15)]  # Duller greens

# Font for text
fontS = pygame.font.SysFont("couriernew", 15)
fontM = pygame.font.SysFont("couriernew", 25)
fontL = pygame.font.SysFont("couriernew", 35)
fontSB = pygame.font.SysFont("couriernew", 15, bold=True)
fontMB = pygame.font.SysFont("couriernew", 25, bold=True)
fontLB = pygame.font.SysFont("couriernew", 35, bold=True)


# Game variables
clock = pygame.time.Clock()
running = True
game_started = False
collision = False
level = 1
max_level = 5
delays = [1, 0.5, 0.25, 0.125, 0.0625, 0.01]
stripe_diffs = [100, 50, 25, 12, 5]

def start_game():
    global game_started, running, collision, level, incorrect
    game_started = True
    running = True
    collision = False
    incorrect = False
    level = 1

def home_screen():
    global game_started

    screen.fill(WHITE)

    chameleon_image = pygame.transform.scale(pygame.image.load('cute_chameleon.jpg'), (SWIDTH, SHEIGHT // 2))
    screen.blit(chameleon_image, (0, SHEIGHT // 2))

    title_text = fontLB.render("* Chameleon Countdown *", True, GREEN)
    help_text = fontSB.render("Use your knowledge about Veiled Chameleon contest behaviors to keep these guys alive!", True, BLACK)
    help2_text = fontSB.render("Choose wisely and choose quickly... ready?", True, BLACK)

    screen.blit(title_text, (SWIDTH // 2 - title_text.get_width() // 2, 75))
    screen.blit(help_text, (SWIDTH // 2 - help_text.get_width() // 2, 150))
    screen.blit(help2_text, (SWIDTH // 2 - help2_text.get_width() // 2, 175))

    start_button = Button.Button(250, 225, 300, 75, RED, "Start Game", 35, start_game)
    start_button.draw(screen)

    pygame.display.flip()

    await_start(start_button)

def countdown_screen():
    start_ticks = pygame.time.get_ticks()  # Record the start time
    countdown_duration = 1000

    for i in range(3, 0, -1):
        screen.fill(WHITE)
        countdown_text = fontLB.render(f"{i}", True, GREEN)
        screen.blit(countdown_text, (SWIDTH // 2 - countdown_text.get_width() // 2, SHEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.update()

        while pygame.time.get_ticks() - start_ticks < countdown_duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        start_ticks = pygame.time.get_ticks()

def await_start(button):
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_input = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button.click()  # Check if button is clicked
                if game_started:  # If game is started after click, break the loop
                    waiting_for_input = False

def draw_chameleons(c1, c2):
    screen.fill(WHITE)
    branch_background = pygame.transform.scale(pygame.image.load('branch_image.jpeg'), (SWIDTH, SHEIGHT))
    screen.blit(branch_background, (0, 125))
    c1.draw(screen, False)
    c2.draw(screen, False)
    level_text = fontLB.render(f"Level {level}", True, RED)
    screen.blit(level_text, (SWIDTH // 2 - level_text.get_width() // 2, 25))

def game_over(message):
    screen.fill(WHITE)
    text = "Game Over: " + message
    game_over_text = fontMB.render(text, True, BLACK)
    screen.blit(game_over_text, (SWIDTH // 2 - game_over_text.get_width() // 2, 250))

    restart_button = Button.Button(250, 350, 300, 75, RED, "Play again", 35, start_game)
    restart_button.draw(screen)
    pygame.display.update()

    await_start(restart_button)

def game1_logic(level):
    global game_started, collision

    countdown_screen()

    # Initialize chameleons
    chameleonL = Chameleon.Chameleon(Chameleon.SIZE, SHEIGHT // 2, level, None, None, facing_right=True)
    chameleonR = Chameleon.Chameleon(SWIDTH - Chameleon.SIZE, SHEIGHT // 2, level, None, None, facing_right=False)

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

# Game loop
while running:
    if not game_started:
        home_screen()
    else:
        if level <= max_level:
            if not game1_logic(level):
                running = False  # End game if incorrect selection (Game Over)
                if collision:
                    game_over("The chameleons fought :(")
                else:
                    game_over("You picked the wrong chameleon :(")
            else:
                level += 1  # Move to next level
        else:
            screen.fill(WHITE)
            win_text = fontLB.render("You Win! Game Over.", True, GREEN)
            screen.blit(win_text, (SWIDTH // 2 - win_text.get_width() // 2, SHEIGHT // 2 - win_text.get_height() // 2))
            pygame.display.update()
            time.sleep(3)
            running = False  # End game after level 5

pygame.quit()
