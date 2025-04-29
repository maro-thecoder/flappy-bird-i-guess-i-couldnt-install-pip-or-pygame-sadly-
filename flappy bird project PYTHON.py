import pygame  # type: ignore
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Remake")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)

# Game variables
GRAVITY = 0.5
BIRD_JUMP = -10
PIPE_SPEED = 5
PIPE_GAP = 150
WINNING_SCORE = 1005
FRAME_RATE = 30  # Frame rate for consistent performance

# Load assets
FONT = pygame.font.Font(None, 40)
BIRD_IMG = pygame.Surface((30, 30))
BIRD_IMG.fill((255, 255, 0))  # Yellow bird
PIPE_IMG = pygame.Surface((50, SCREEN_HEIGHT))
PIPE_IMG.fill((0, 255, 0))  # Green pipes

# Home screen function
def home_screen():
    while True:
        SCREEN.fill(BLUE)
        title_text = FONT.render("Flappy Bird Remake", True, BLACK)
        start_text = FONT.render("Press SPACE to Start", True, BLACK)
        SCREEN.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))
        SCREEN.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 300))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

# End screen function
def end_screen(score):
    while True:
        SCREEN.fill(BLUE)
        score_text = FONT.render(f"Your Score: {score}", True, BLACK)
        restart_text = FONT.render("Press R to Restart or Q to Quit", True, BLACK)
        SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Win screen function
def win_screen():
    BLUE_BIRD_IMG = pygame.Surface((30, 30))
    BLUE_BIRD_IMG.fill((0, 0, 255))  # Blue bird

    while True:
        SCREEN.fill(BLUE)
        SCREEN.blit(BLUE_BIRD_IMG, (SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 2 - 100))

        chat_text = FONT.render("You never give up huh?", True, BLACK)
        SCREEN.blit(chat_text, (SCREEN_WIDTH // 2 - chat_text.get_width() // 2, SCREEN_HEIGHT // 2))

        win_text = FONT.render("Congratulations! You beat the game!", True, BLACK)
        SCREEN.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        restart_text = FONT.render("Press R to Restart or Q to Quit", True, BLACK)
        SCREEN.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Main game function
def play_game():
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0

    def create_pipe():
        pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        top_pipe = pygame.Rect(SCREEN_WIDTH, 0, 50, pipe_height)
        bottom_pipe = pygame.Rect(SCREEN_WIDTH, pipe_height + PIPE_GAP, 50, SCREEN_HEIGHT - pipe_height - PIPE_GAP)
        return top_pipe, bottom_pipe

    pipes.extend(create_pipe())

    clock = pygame.time.Clock()

    while True:
        SCREEN.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_velocity = BIRD_JUMP

        bird_velocity += GRAVITY
        bird_y += bird_velocity
        bird_rect = pygame.Rect(50, bird_y, 30, 30)

        for pipe in pipes:
            pipe.x -= PIPE_SPEED

        if pipes[0].x + pipes[0].width < 0:
            pipes = pipes[2:]
            pipes.extend(create_pipe())
            score += 1

            if score >= WINNING_SCORE:
                return "win"

        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                return score  # Return score on collision

        if bird_y < 0 or bird_y > SCREEN_HEIGHT:
            return score  # Return score if bird goes out of bounds

        SCREEN.blit(BIRD_IMG, (bird_rect.x, bird_rect.y))

        for pipe in pipes:
            SCREEN.blit(PIPE_IMG, (pipe.x, pipe.y))

        score_text = FONT.render(f"Score: {score}", True, BLACK)
        SCREEN.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(FRAME_RATE)

# Main loop
def main():
    while True:
        home_screen()
        result = play_game()
        if result == "win":
            win_screen()
        else:
            end_screen(result)  # Pass the score to the end screen

if __name__ == "__main__":
    main()