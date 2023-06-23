import pygame
from pygame.locals import *
import sys
import time
import random
import os

#author@ATUL

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
open_img_path = os.path.join(IMAGE_DIR, 'img1.png')
bg_path = os.path.join(IMAGE_DIR, 'img2.jpg')
icon_path = os.path.join(IMAGE_DIR, 'img3.png')



class Game:
    def __init__(self):
        self.w = 750
        self.h = 500
        self.reset = True
        self.active = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time: 0 Accuracy: 0% Wpm: 0'
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255, 213, 102)
        self.TEXT_C = (240, 240, 240)
        self.RESULT_C = (255, 70, 70)

        pygame.init()

        # Load images
        self.open_img = self.load_image(open_img_path)
        self.bg = self.load_image(bg_path)
        self.time_img = self.load_image(icon_path)

        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Type Speed Test')

    @staticmethod
    def load_image(image_path):
        try:
            image = pygame.image.load(image_path)
            return pygame.transform.scale(image, (750, 500))
        except pygame.error as e:
            print(f"Error loading image: {image_path}")
            raise e

    def draw_text(self, screen, msg, y, fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1, color)
        text_rect = text.get_rect(center=(self.w/2, y))
        screen.blit(text, text_rect)

    def get_sentence(self):
        file_path = os.path.join(BASE_DIR, 'sentences.txt')
        with open(file_path, 'r') as f:
            sentences = f.read().split('\n')
        return random.choice(sentences)

    def show_results(self, screen):
        if not self.end:
            # Calculate time
            self.total_time = time.time() - self.time_start

            # Calculate accuracy
            count = sum(1 for i, c in enumerate(self.word) if i < len(self.input_text) and self.input_text[i] == c)
            self.accuracy = count / len(self.word) * 100

            # Calculate words per minute
            self.wpm = len(self.input_text) * 60 / (5 * self.total_time)
            self.end = True
            print(self.total_time)

            self.results = f"Time: {round(self.total_time)} secs   Accuracy: {round(self.accuracy)}%   Wpm: {round(self.wpm)}"

            # Draw icon image
            screen.blit(self.time_img, (self.w/2 - 75, self.h - 140))
            self.draw_text(screen, "Reset", self.h - 70, 26, (100, 100, 100))

            print(self.results)
            pygame.display.update()

    def run(self):
        self.reset_game()
        self.running = True
        clock = pygame.time.Clock()

        while self.running:
            self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            pygame.draw.rect(self.screen, self.HEAD_C, (50, 250, 650, 50), 2)
            self.draw_text(self.screen, self.input_text, 274, 26, (250, 250, 250))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if 50 <= x <= 650 and 250 <= y <= 300:
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                    elif 310 <= x <= 510 and 390 <= y <= 440 and self.end:
                        self.reset_game()

                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            self.draw_text(self.screen, self.results, 350, 28, self.RESULT_C)
                            self.end = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass

            pygame.display.update()
            clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img, (0, 0))
        pygame.display.update()
        time.sleep(1)
        self.reset = False
        self.end = False
        self.input_text = ''
        self.word = self.get_sentence()

        if not self.word:
            self.reset_game()

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        msg = "Typing Speed Check"
        self.draw_text(self.screen, msg, 80, 80, self.HEAD_C)
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)
        self.draw_text(self.screen, self.word, 200, 28, self.TEXT_C)
        pygame.display.update()

Game().run()
