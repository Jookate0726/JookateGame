import pygame
import os
import random as r
from tkinter import *
from PIL import Image, ImageTk


def game(score, win_points, bomb_point, heart_point):
    pygame.mixer.init()
    pygame.font.init()

    BOMB_SCORE = pygame.USEREVENT + 1
    HEART_SCORE = pygame.USEREVENT + 2

    SCORE_FONT = pygame.font.SysFont('comicsans', 40)
    WINNER_FONT = pygame.font.SysFont('comicsans', 100)

    WIDTH, HEIGHT = 1200, 800
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jookate game")
    WHITE = (255, 255, 255)
    JOOKATE_WIDTH, JOOKATE_HEIGHT = 150, 150
    SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 170, 150
    BOMB_VEL = 1
    HEART_VEL = 1
    FPS = 40
    CLOCK = pygame.time.Clock()
    SCORE, WIN_POINTS, BOMB_POINT, HEART_POINT = score, win_points, bomb_point, heart_point

    JOO_IMAGE = pygame.transform.scale(pygame.image.load('Assets\main.png'), (JOOKATE_WIDTH, JOOKATE_HEIGHT))
    BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bgj.jpg')), (WIDTH, HEIGHT))
    SPACE_IMAGE = pygame.transform.scale(pygame.image.load('Assets\space.png'), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
    BOMB = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bomb.png')), (30, 45))
    HEART = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'heart.png')), (40, 45))

    BOMB_HIT = pygame.mixer.Sound('Assets\Grenade+1.mp3')
    BOMB_RELEASE = pygame.mixer.Sound('Assets\Gun+Silencer.mp3')
    HEART_RELEASE = pygame.mixer.Sound('Assets\sms_tone.mp3')
    HEART_HIT = pygame.mixer.Sound('Assets\winner.mp3')

    def draw_display(rect, s_rect, bombs, hearts, score):
        WIN.fill(WHITE)
        WIN.blit(BG, (0, 0))
        WIN.blit(SPACE_IMAGE, (s_rect.x, s_rect.y))

        for bomb in bombs:
            WIN.blit(BOMB, (bomb.x, bomb.y))

        for heart in hearts:
            WIN.blit(HEART, (heart.x, heart.y))

        WIN.blit(JOO_IMAGE, (rect.x, rect.y))

        score1 = SCORE_FONT.render("SCORE: " + str(score), 1, WHITE)
        WIN.blit(score1, (10, 10))

        pygame.display.update()

    def bullet_display(rect, bombs):
        for bomb in bombs:
            bomb.y += BOMB_VEL
            if rect.colliderect(bomb):
                pygame.event.post(pygame.event.Event(BOMB_SCORE))
                bombs.remove(bomb)
                BOMB_HIT.play()

            elif bomb.y > HEIGHT:
                bombs.remove(bomb)

    def heart_display(rect, hearts):
        for heart in hearts:
            heart.y += HEART_VEL
            if rect.colliderect(heart):
                pygame.event.post(pygame.event.Event(HEART_SCORE))
                hearts.remove(heart)
                HEART_HIT.play()

            elif heart.y > HEIGHT:
                hearts.remove(heart)

    def winner_draw(WINNER_TEXT):
        win = WINNER_FONT.render(WINNER_TEXT, 1, WHITE)
        WIN.blit(win, (WIDTH // 2 - win.get_width() // 2, HEIGHT // 2 - win.get_height() // 2))
        pygame.display.update()

        pygame.time.delay(4000)

    def main():
        RUN = 1
        right = 1
        rect = pygame.Rect(25, HEIGHT - JOOKATE_HEIGHT + 10, JOOKATE_WIDTH, JOOKATE_HEIGHT)
        s_rect = pygame.Rect(0, 0, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        CLOCK.tick(FPS)

        score = SCORE

        bombs = []
        hearts = []

        while RUN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUN = 0

                if event.type == BOMB_SCORE:
                    score -= BOMB_POINT
                if event.type == HEART_SCORE:
                    score += HEART_POINT

            flag = [i for i in range(0, 500)]
            if r.choice(flag) == 10:
                flag2 = [i for i in range(0, 2)]
                if r.choice(flag2) == 1:
                    heart = pygame.Rect(s_rect.x + SPACESHIP_WIDTH // 2, s_rect.y + SPACESHIP_HEIGHT, 15, 16)
                    hearts.append(heart)
                    HEART_RELEASE.play()

            flag1 = [i for i in range(0, 250)]
            if r.choice(flag1) == 10:
                bomb = pygame.Rect(s_rect.x + SPACESHIP_WIDTH // 2, s_rect.y + SPACESHIP_HEIGHT, 7, 13)
                bombs.append(bomb)
                BOMB_RELEASE.play()

            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_LEFT] and rect.x > 0:
                rect.x -= 1
            if key_pressed[pygame.K_RIGHT] and rect.x < WIDTH - JOOKATE_WIDTH:
                rect.x += 1

            if right == 1:
                if s_rect.x > 5:
                    s_rect.x -= 1
                else:
                    s_rect.x += 1
                    right = 0
            else:
                if s_rect.x < WIDTH - SPACESHIP_WIDTH:
                    s_rect.x += 1
                else:
                    s_rect.x -= 1
                    right = 1

            bullet_display(rect, bombs)
            heart_display(rect, hearts)
            draw_display(rect, s_rect, bombs, hearts, score)

            WINNER_TEXT = ""
            if score <= 0:
                WINNER_TEXT = "JooKate Lose!"
            if score >= WIN_POINTS:
                WINNER_TEXT = "JooKate Wins!"

            if WINNER_TEXT != "":
                winner_draw(WINNER_TEXT)
                break

        pygame.quit()

    if __name__ == "__main__":
        main()


WINDOW = Tk()
WINDOW.title("JooKate Game")
WINDOW.geometry("563x540")
WINDOW.configure(bg='black')

imgs = ImageTk.PhotoImage(Image.open(os.path.join('Assets', 'background.png')))  # getting image
imglab = Label(WINDOW, image=imgs).grid(row=0, column=0, padx=40, pady=(50, 10), columnspan=3)

b7 = Button(WINDOW, text="  EASY  \n\nBOMB : -1, HEART : +2", fg="black", bg="white", padx=10, pady=10, command=lambda: game(25, 50, 1, 2)).grid(row=1, column=0, padx=5, pady=20, ipadx=15)
b8 = Button(WINDOW, text="MEDIUM\n\nBOMB : -1, HEART : +1", fg="black", bg="white", padx=10, pady=10, command=lambda: game(10, 75, 1, 1)).grid(row=1, column=1, padx=5, pady=20, ipadx=15)
b9 = Button(WINDOW, text="  HARD  \n\nBOMB : -2, HEART : +1", fg="black", bg="white", padx=10, pady=10, command=lambda: game(10, 100, 2, 1)).grid(row=1, column=2, padx=5, pady=20, ipadx=15)

WINDOW.mainloop()

