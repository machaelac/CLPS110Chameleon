import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 100, 0)

SIZE = 100
STRIPES = 5

class Chameleon:
    def __init__(self, x, y, speed, facing_right=True):
        self.x = x
        self.y = y
        self.facing_right = facing_right
        self.base_color = DARK_GREEN
        self.stripe_color = self.base_color
        self.head_color = self.stripe_color
        self.body_left = self.x - SIZE // 2 if self.facing_right else self.x + SIZE // 2 - SIZE
        self.body_rect = pygame.Rect(self.body_left, self.y - SIZE // 4, SIZE, SIZE // 2)
        self.invisible_wall = 325 if self.facing_right else 475
        self.speed = speed

    def draw(self, screen):
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

        # Draw outline for the body
        pygame.draw.ellipse(screen, BLACK, self.body_rect, 2)

        # Draw tail
        tail_x = (
            self.body_rect.left - SIZE // 4
            if self.facing_right
            else self.body_rect.right - SIZE // 4
        )
        tail_y = self.body_rect.centery - SIZE // 4

        pygame.draw.arc(
            screen, self.base_color,
            (tail_x, tail_y, SIZE // 2, SIZE // 2),
            3.14 if self.facing_right else 4.71,
            4.71 if self.facing_right else 6.28,
            3
        )

        # Draw head
        head_x = self.body_rect.right if self.facing_right else self.body_rect.left - SIZE // 4
        pygame.draw.circle(screen, self.head_color, (head_x, self.y), SIZE // 4)

        # Draw eye
        eye_x = head_x + SIZE // 8 if self.facing_right else head_x - SIZE // 8
        pygame.draw.circle(screen, WHITE, (eye_x, self.y - SIZE // 8), SIZE // 10)
        pygame.draw.circle(screen, BLACK, (eye_x, self.y - SIZE // 8), SIZE // 20)

    def move_towards(self):
        if self.x < self.invisible_wall:
            self.x += self.speed  # Move right
        else:
            self.x -= self.speed # Move left
        self.body_rect.x = self.x - SIZE // 2
