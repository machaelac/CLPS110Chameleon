import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
CHAMELEON_SIZE = 100
STRIPE_COUNT = 5  # Number of stripes on the body

# Colors
BRIGHT_COLORS = [(34, 139, 34), (0, 255, 0), (144, 238, 144)]  # Shades of green
DULL_COLORS = [(0, 48, 0), (0, 100, 0), (56, 79, 15)]  # Duller greens
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = WHITE  # White background

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chameleon Game")
clock = pygame.time.Clock()

# Chameleon class
class Chameleon:
    def __init__(self, x, y, facing_right=True):
        self.x = x
        self.y = y
        self.facing_right = facing_right
        self.base_color = random.choice(BRIGHT_COLORS + DULL_COLORS)  # Select from new shades of green
        self.is_bright = self.base_color in BRIGHT_COLORS
        self.stripe_color = WHITE if self.is_bright else BLACK  # Contrast stripes for visibility
        self.head_color = self.base_color  # Initial head color

        # Speed for head color change (random between 1 and 5)
        self.head_color_change_speed = random.randint(1, 5)

    def update_head_color(self):
        # Change head color at a random speed (simulate the color changing process)
        if random.random() < 0.1 * self.head_color_change_speed:  # 10% chance of color change per frame
            self.head_color = random.choice(BRIGHT_COLORS + DULL_COLORS)

    def draw(self):
        # Adjust drawing direction
        body_left = self.x - CHAMELEON_SIZE // 2 if self.facing_right else self.x + CHAMELEON_SIZE // 2 - CHAMELEON_SIZE
        body_rect = pygame.Rect(body_left, self.y - CHAMELEON_SIZE // 4, CHAMELEON_SIZE, CHAMELEON_SIZE // 2)
        stripe_width = body_rect.width // STRIPE_COUNT

        # Draw striped body
        for i in range(STRIPE_COUNT):
            stripe_rect = pygame.Rect(
                body_rect.left + i * stripe_width,
                body_rect.top,
                stripe_width,
                body_rect.height,
            )
            stripe_color = self.base_color if i % 2 == 0 else self.stripe_color
            pygame.draw.rect(screen, stripe_color, stripe_rect)

        # Draw outline for the body
        pygame.draw.ellipse(screen, BLACK, body_rect, 2)

        # Draw tail
        tail_x = (
            body_rect.left - CHAMELEON_SIZE // 4
            if self.facing_right
            else body_rect.right - CHAMELEON_SIZE // 4
        )
        pygame.draw.arc(
            screen, self.base_color,
            (tail_x, self.y - CHAMELEON_SIZE // 4, CHAMELEON_SIZE // 2, CHAMELEON_SIZE // 2),
            3.14 if self.facing_right else 4.71,
            4.71 if self.facing_right else 6.28,
            3
        )

        # Draw head
        head_x = body_rect.right if self.facing_right else body_rect.left - CHAMELEON_SIZE // 4
        pygame.draw.circle(screen, self.head_color, (head_x, self.y), CHAMELEON_SIZE // 4)

        # Draw eye
        eye_x = head_x + CHAMELEON_SIZE // 8 if self.facing_right else head_x - CHAMELEON_SIZE // 8
        pygame.draw.circle(screen, WHITE, (eye_x, self.y - CHAMELEON_SIZE // 8), CHAMELEON_SIZE // 10)
        pygame.draw.circle(screen, BLACK, (eye_x, self.y - CHAMELEON_SIZE // 8), CHAMELEON_SIZE // 20)

# Main game loop
def main():
    running = True
    font = pygame.font.Font(None, 36)
    result_text = ""
    result_color = WHITE
    instruction_color = BLACK  # Set instruction text color to black

    while running:
        # Generate chameleons
        chameleon1 = Chameleon(200, SCREEN_HEIGHT // 2, facing_right=True)
        chameleon2 = Chameleon(600, SCREEN_HEIGHT // 2, facing_right=False)

        # Determine correct answer
        correct_answer = "LEFT" if chameleon1.is_bright else "RIGHT"

        # Reset game state
        player_answer = None
        result_text = ""

        # Wait for player's choice
        waiting_for_input = True
        while waiting_for_input:
            screen.fill(BACKGROUND_COLOR)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_input = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player_answer = "LEFT"
                        waiting_for_input = False
                    elif event.key == pygame.K_RIGHT:
                        player_answer = "RIGHT"
                        waiting_for_input = False

            # Draw chameleons
            chameleon1.draw()
            chameleon2.draw()

            # Display instructions in black
            question = font.render("Which chameleon will approach first? (Left or Right)", True, instruction_color)
            screen.blit(question, (SCREEN_WIDTH // 2 - question.get_width() // 2, 50))

            # Update screen
            pygame.display.flip()
            clock.tick(FPS)

        # Evaluate the player's answer
        if player_answer == correct_answer:
            result_text = "Correct! The brighter chameleon approaches first."
            result_color = (0, 255, 0)  # Green
        else:
            result_text = "Wrong! The brighter chameleon approaches first."
            result_color = (255, 0, 0)  # Red

        # Show result
        result_display_time = 2  # seconds
        result_start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - result_start_time < result_display_time * 1000:
            screen.fill(BACKGROUND_COLOR)
            chameleon1.draw()
            chameleon2.draw()

            # Display result
            result = font.render(result_text, True, result_color)
            screen.blit(result, (SCREEN_WIDTH // 2 - result.get_width() // 2, 50))

            pygame.display.flip()
            clock.tick(FPS)

        # Now enter the contest round
        contest_text1 = "Now that one has approached, they will engage in their contest."
        contest_text2 = "Which chameleon is most likely to win the fight?"
        contest_prompt1 = font.render(contest_text1, True, instruction_color)
        contest_prompt2 = font.render(contest_text2, True, instruction_color)


        # Display contest text
        screen.fill(BACKGROUND_COLOR)
        screen.blit(contest_prompt1, (SCREEN_WIDTH // 2 - contest_prompt1.get_width() // 2, 10))
        screen.blit(contest_prompt2, (SCREEN_WIDTH // 2 - contest_prompt1.get_width() // 2, 40))   
        pygame.display.flip()

        pygame.time.wait(2000)  # Wait for 2 seconds before starting the contest round

        # Assign random speeds for head color change
        chameleon1.head_color_change_speed = random.randint(1, 5)
        chameleon2.head_color_change_speed = random.randint(1, 5)

        # Wait for player to choose which chameleon will win
        waiting_for_input = True
        while waiting_for_input:
            screen.fill(BACKGROUND_COLOR)

            # Update head colors
            chameleon1.update_head_color()
            chameleon2.update_head_color()

            # Draw chameleons
            chameleon1.draw()
            chameleon2.draw()

            # Ask the player to choose
            choose_text = "Choose: Left or Right?"
            choose_prompt = font.render(choose_text, True, instruction_color)
            screen.blit(choose_prompt, (SCREEN_WIDTH // 2 - choose_prompt.get_width() // 2, 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_input = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player_answer = "LEFT"
                        waiting_for_input = False
                    elif event.key == pygame.K_RIGHT:
                        player_answer = "RIGHT"
                        waiting_for_input = False

            clock.tick(FPS)

        # Determine the winner
        if chameleon1.head_color_change_speed > chameleon2.head_color_change_speed:
            correct_answer = "LEFT"
        else:
            correct_answer = "RIGHT"

        # Evaluate the player's answer
        if player_answer == correct_answer:
            contest_result = "Correct! The faster changing chameleon wins."
            contest_result_color = (0, 255, 0)  # Green
        else:
            contest_result = "Wrong! The faster changing chameleon wins."
            contest_result_color = (255, 0, 0)  # Red

        # Show contest result
        contest_result_display_time = 2  # seconds
        contest_result_start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - contest_result_start_time < contest_result_display_time * 1000:
            screen.fill(BACKGROUND_COLOR)
            chameleon1.draw()
            chameleon2.draw()

            # Display contest result
            contest_result_text = font.render(contest_result, True, contest_result_color)
            screen.blit(contest_result_text, (SCREEN_WIDTH // 2 - contest_result_text.get_width() // 2, 50))

            pygame.display.flip()
            clock.tick(FPS)

# Run the game
if __name__ == "__main__":
    main()
