import pygame
import random
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 125, 0)
ORANGE = (255, 165, 0)

SIZE = 100
STRIPES = 5

class Chameleon:
    def __init__(self, x, y, speed, sz, color, facing_right=True):
        self.x = x
        self.y = y
        self.facing_right = facing_right
        self.base_color = DARK_GREEN if color == None else color
        self.stripe_color = self.base_color
        self.head_color = self.stripe_color
        self.size = SIZE if sz == None else sz
        self.body_left = self.x - self.size // 2 if self.facing_right else self.x + self.size // 2 - self.size
        self.body_rect = pygame.Rect(self.body_left, self.y - self.size // 4, self.size, self.size // 2)
        self.invisible_wall = 300 if self.facing_right else 450
        self.speed = speed
        self.bobbing = False
        self.mad = False

    def change_color(self, color):
        self.base_color = color
        self.stripe_color = color
        self.head_color = color

    def draw(self, screen, spots):
        # Adjust drawing direction
        stripe_width = self.body_rect.width // STRIPES

        # Draw striped body
        for i in range(STRIPES):
            stripe_rect = pygame.Rect(
                self.body_rect.left + i * stripe_width,
                self.body_rect.top,
                stripe_width,
                self.body_rect.height,
            )
            stripe_color = self.base_color if i % 2 == 0 else self.stripe_color
            pygame.draw.rect(screen, stripe_color, stripe_rect)

        if spots:
            spot_positions = [
                (self.body_rect.left + stripe_width * 1, self.body_rect.top + (self.size // 4)),  # First spot
                (self.body_rect.left + stripe_width * 2, self.body_rect.top + (self.size // 4)),  # Second spot
                (self.body_rect.left + stripe_width * 3, self.body_rect.top + (self.size // 4)),  # Third spot
                (self.body_rect.left + stripe_width * 4, self.body_rect.top + (self.size // 4)),  # Fourth spot
            ]
            for spot_x, spot_y in spot_positions:
                pygame.draw.circle(screen, ORANGE, (spot_x, spot_y), self.size // 20)


        # Draw outline for the body
        pygame.draw.ellipse(screen, BLACK, self.body_rect, 2)

        # Draw tail
        tail_x = (
            self.body_rect.left - self.size // 4
            if self.facing_right
            else self.body_rect.right - self.size // 4
        )
        tail_y = self.body_rect.centery - self.size // 4

        pygame.draw.arc(
            screen, self.base_color,
            (tail_x, tail_y, self.size // 2, self.size // 2),
            3.14 if self.facing_right else 4.71,
            4.71 if self.facing_right else 6.28,
            3
        )

        # Draw head
        head_x = self.body_rect.right if self.facing_right else self.body_rect.left - self.size // 4


        if self.bobbing:
            head_offset = math.sin(pygame.time.get_ticks() * 0.05) * 10
        else:
            head_offset = 0  # If not bobbing, no offset
        head_y = self.y + head_offset

        pygame.draw.circle(screen, self.head_color, (head_x, head_y), self.size // 4)

        if self.mad:
            mouth_width = self.size // 2  # Width of the mouth
            mouth_height = self.size // 4  # Height of the mouth
            mouth_points = [
                (head_x - mouth_width // 2, head_y + mouth_height // 2),  # Left corner of the mouth
                (head_x + mouth_width // 2, head_y + mouth_height // 2),  # Right corner of the mouth
                (head_x, head_y - mouth_height // 2)  # Top corner (vertex) of the mouth
            ]
            pygame.draw.polygon(screen, BLACK, mouth_points)  # Draw the triangle mouth


        # Draw eye
        eye_x = head_x + self.size // 8 if self.facing_right else head_x - self.size // 8
        pygame.draw.circle(screen, WHITE, (eye_x, self.y - self.size // 8), self.size // 10)
        pygame.draw.circle(screen, BLACK, (eye_x, self.y - self.size // 8), self.size // 20)

    def move_towards(self):
        if self.x < self.invisible_wall:
            self.x += self.speed  # Move right
        else:
            self.x -= self.speed # Move left
        self.body_rect.x = self.x - self.size // 2
