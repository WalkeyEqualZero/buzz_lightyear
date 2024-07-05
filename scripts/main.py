import time

import pygame
import os
import logging

from datetime import datetime
from scripts.utils import pygame_load_image, RotateAnimation, CounterAnimation,\
    MirrorAnimation, EnemyState, CharacterDirection, CharacterState, Character,\
    Professor, NPCState, RandomNPC, Character2, Mann, Brend, Sheila, Bullet, BigStarship, PlanetQuests,\
    SwimmingCharacter, UnderWater
from typing import List, Dict
pygame.init()


class World:
    def __init__(self, screen, char_x, char_y, bg):
        print("ASSET_DIRECTORY", ASSET_DIRECTORY)
        self.last_tp = None
        self.bg = bg
        self.def_bg = 'tamploin 2.0.png'
        self.char_x = char_x
        self.char_y = char_y
        self.screen = screen
        self.tavern_rect = pygame.Rect(900, 315, 20, char_y)
        self.right_rect = pygame.Rect(1100, 315, 20, char_y)
        self.left_rect = pygame.Rect(-100, 315, 20, char_y)
        self.decors = {'locker_room': {pygame.image.load(ASSET_DIRECTORY + 'bench.png'): (579, 427), pygame.image.load(ASSET_DIRECTORY + 'bench1.png'): (207, 430), pygame.image.load(ASSET_DIRECTORY + 'wetf.png'): (901, 404)},
                       'outside': {pygame.image.load(ASSET_DIRECTORY + 'fence.png'): (892, 226)},
                       'lab': {pygame.image.load(ASSET_DIRECTORY + 'tlab.png'): (0, 221), pygame.image.load(ASSET_DIRECTORY + 'light_tlab.png'): (0, 188)},
                       'ship2': {pygame.image.load(ASSET_DIRECTORY + 'cube.png'): (212, 333)},
                       'outside_planet2': {pygame.image.load(ASSET_DIRECTORY + 'outside_planet2dec.png'): (29, 429)}}

    def is_collided(self, character, last):
        max_n = 2
        if part3:
            max_n = 1
        if self.bg != 'tavern.png':
            if self.last_tp == "right" and self.left_rect.colliderect(character.char_rect):
                return 0
            elif self.last_tp == "left" and self.right_rect.colliderect(character.char_rect):
                return 0
            else:
                self.last_tp = None
            if self.right_rect.colliderect(character.char_rect) and last < max_n:
                self.last_tp = "right"
                character.x = -60
                return 1
            elif self.left_rect.colliderect(character.char_rect) and last != 0:
                self.last_tp = "left"
                character.x = 900
                return -1
            else:
                self.right_rect = pygame.Rect(1100, 315, 20, game.char_y)
                self.left_rect = pygame.Rect(-100, 315, 20, game.char_y)
                return 0
        else:
            return 0

    def tavern(self, character):
        if self.tavern_rect.colliderect(character.char_rect) and self.bg == self.def_bg and self.bg != 'tavern.png':
            logging.info('tavern')
            character.y = 290
            return 3
        elif self.bg == 'tavern.png':
            logging.info('tavern')
            character.y = 360
            character.x = 720
            return 2
        else:
            return 2

    def decor(self):
        if self.bg in self.decors:
            for name, xy in self.decors[self.bg].items():
                win.blit(name, xy)


def collide(x, y):
    global starship1
    asteroid = pygame.image.load(ASSET_DIRECTORY + 'asteroid.png')
    asteroid_rect = asteroid.get_rect(topleft=(x, y))
    # pygame.draw.rect(win, 'white',asteroid_rect)
    # asteroid_rect = pygame.Rect(x + 20, y + 20, asteroid_rect.width - 20, asteroid_rect.height - 20)
    # print(asteroid_rect.width, asteroid_rect.height)
    if starship1.rect1.colliderect(asteroid_rect):
        return True
    elif starship1.rect2.colliderect(asteroid_rect):
        return True
    elif starship1.rect3.colliderect(asteroid_rect):
        return True
    else:
        return False


ASSET_DIRECTORY = os.path.abspath(os.path.dirname(__file__)) + "/../imgs/"
ASSET_DIRECTORY_CHARACTER = os.path.abspath(os.path.dirname(__file__)) + "/../imgs/buzz_character/"


logging.basicConfig(level=logging.DEBUG)

win = pygame.display.set_mode((1012, 576))
pygame.display.set_caption("Buzz Lighter: The Game")
bg = pygame.image.load(ASSET_DIRECTORY + 'menu_bg.png')
bg = pygame.transform.scale(bg, (1012, 576))
bgs_names = ['outside', 'locker_room', 'lab']
bgs = [pygame.image.load(ASSET_DIRECTORY + 'outside.png'), pygame.image.load(ASSET_DIRECTORY + 'locker_room.png'), pygame.image.load(ASSET_DIRECTORY + 'lab.png')]
# pygame.transform.scale(pygame.image.load(ASSET_DIRECTORY+'tamploin 2.0.png'), (1012, 576))
width = 0
game = World(win, 210, 210, bg)
end = False

char = Character(450, 300, win, 'buzz_idle1.png', bg, 160, 160, ASSET_DIRECTORY_CHARACTER)
swim_char = SwimmingCharacter(100, 245, win, ASSET_DIRECTORY_CHARACTER)
char2 = Character2(450, 300, win, 'buzz_idle1.png', bg, 160, 160, ASSET_DIRECTORY_CHARACTER)

n_text = 2
run = True
last = 0
last_r = 0
clock = pygame.time.Clock()
pressed_attack = False
kadr = 0
rectsi = pygame.Surface((1012, 576))
rectsi.set_alpha(0)
rectsi.fill((0, 0, 0))
yep = False
numbe = 0
professor = Professor(750, 255, win, 205, 205, ASSET_DIRECTORY)
manlab1 = RandomNPC(350, 255, win, 205, 205, 'man1_idle', ASSET_DIRECTORY, 6, 'r', 'lab')
womanlab1 = RandomNPC(290, 255, win, 205, 205, 'woman1_idle', ASSET_DIRECTORY, 4, 'r', 'lab')
cat = RandomNPC(600, 255, win, 205, 205, 'cat', ASSET_DIRECTORY, 5, 'l', 'outside_planet2')
rectangle = pygame.Rect(474, 308, 83, 153)
end_of_part2 = pygame.Rect(950, 308, 83, 153)
mann = Mann(-1000, 255, win, 205, 205, ASSET_DIRECTORY)
brend = Brend(-1000, 255, win, 205, 205, ASSET_DIRECTORY)
first_time = True
part_end = False

part1 = True
part2 = False
part3 = False
part4 = False
part5 = False
part6 = False
part7 = False

sheila = Sheila(-1000, 245, win, 215, 215, ASSET_DIRECTORY)
bullets = {}
del_bullets = []
num_bullets = 0
music = False
timeb = 0
box = False
box_showed = False
numbi = 255
list(game.decors['ship2'].keys())[0].set_alpha(numbi)
sh3 = False
starship1 = BigStarship(100, 245, win, ASSET_DIRECTORY)
all_events = ''
piano_tabs = []
planet = PlanetQuests()
underwater = UnderWater()
underwater_cube = pygame.Rect(859, 245, 86, 38)
tab = 'pianog.png'
pygame.mixer.music.load(ASSET_DIRECTORY + 'bgmusic.mp3')
pygame.mixer.music.play(-1)

while run:

    clock.tick(56)
    win.blit(bg, (0, 0))
    pressed_attack = False
    space = False
    # <<< ПРОСТО П@$%ЕЦ КАК ПОЛЕЗНО >>>
    # if numbe != 255:
    #     numbe += 3
    # rectsi.set_alpha(numbe)
    # win.blit(rectsi, (0, 0))
    if part1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.unicode == 'u':
                pressed_attack = True

            if event.type == pygame.KEYDOWN and event.unicode == 'q' and professor.showed and yep:
                part1 = False
                part2 = True

            if event.type == pygame.KEYDOWN and event.unicode == ' ':
                if char2.quest:
                    professor.n_text += 3
                # elif char.quest_2:
                #     if n_text % 2 == 0:
                #         char.n_text += 1
                #     if n_text % 2 != 0:
                #         keir.n_text += 1
                #     n_text += 1
            logging.info(event)

        if end:
            char.set_state(CharacterState.idle)
        elif char2.quest and char.life > 0:
            professor.win.blit(pygame.transform.scale(pygame.image.load(ASSET_DIRECTORY + 'panel.png'), (900, 300)), (56, -50))
            char2.set_state(CharacterState.idle)
            professor.set_state(NPCState.talk)
            keys = pygame.key.get_pressed()
            if professor.n_text == 9:
                n_text = 0
                char.n_text = 0
                professor.showed = True
                professor.set_state(NPCState.idle)
                char2.quest = False
            else:
                myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel2.ttf', 25)
                textsurface_2 = myfont.render('Профессор Бренд:', False, (0, 0, 0))
                textline1 = myfont.render(professor.text[professor.n_text], False, (0, 0, 0))
                textline2 = myfont.render(professor.text[professor.n_text + 1], False, (0, 0, 0))
                textline3 = myfont.render(professor.text[professor.n_text + 2], False, (0, 0, 0))
                win.blit(textline1, (150, 85))
                win.blit(textline2, (150, 110))
                win.blit(textline3, (150, 135))
                win.blit(textsurface_2, (150, 35))
        #
        # elif char.quest_2 and char.life > 0:
        #     keir.win.blit(pygame.transform.scale(pygame.image.load(ASSET_DIRECTORY + 'panel.png'), (900, 300)), (56, -50))
        #     char.set_state(CharacterState.idle)
        #     keys = pygame.key.get_pressed()
        #     print(n_text)
        #     if n_text == 5:
        #         keir.showed = True
        #         char.quest_2 = False
        #         enem.quest = True
        #     if n_text % 2 == 0:
        #         myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel.ttf', 20)
        #         textsurface = myfont.render(char.text_2[char.n_text], False, (0, 0, 0))
        #         textsurface_2 = myfont.render('Геральт:', False, (0, 0, 0))
        #         win.blit(textsurface, (150, 85))
        #         win.blit(textsurface_2, (150, 35))
        #     elif n_text % 2 != 0:
        #         myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel.ttf', 20)
        #         textsurface = myfont.render(keir.text[keir.n_text], False, (0, 0, 0))
        #         textsurface_2 = myfont.render('Кейр:', False, (0, 0, 0))
        #         win.blit(textsurface, (150, 85))
        #         win.blit(textsurface_2, (150, 35))

        elif char.life > 0:
            if pressed_attack:
                logging.info("key pressed attack.")
                if char.state == CharacterState.idle:
                    # if char.attack(enem):
                    #     enem.hp -= 35
                    #     enem.rotate.rotate()
                    #     if enem.hp <= 0:
                    #         enem.set_state(EnemyState.dead)
                    #         enem.dead = True
                    #         logging.info("Death")
                    char.set_state(CharacterState.attack)
                # elif char.state == CharacterState.attack:
                #     if char.attack(enem):
                #         enem.hp -= 35
                #         enem.rotate.rotate()
                #         if enem.hp <= 0:
                #             enem.set_state(EnemyState.dead)
                #             enem.dead = True
                #             logging.info("Death")
                #     char.set_state(CharacterState.attack2)
                # elif char.state == CharacterState.attack2:
                #     if char.attack(enem):
                #         enem.hp -= 35
                #         enem.rotate.rotate()
                #         if enem.hp <= 0:
                #             enem.set_state(EnemyState.dead)
                #             enem.dead = True
                #             logging.info("Death")
                #     char.set_state(CharacterState.attack3)
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a] and char2.x > char2.vel - 200:
                    logging.info("key pressed walk left.")

                    if char2.set_state(CharacterState.walk):
                        char2.direction = CharacterDirection.left
                        char2.x -= char2.vel
                        char.direction = CharacterDirection.left
                        char.x -= char.vel

                elif keys[pygame.K_d] and char2.x < 1100 - char2.vel:
                    logging.info("key pressed walk right.")

                    if char2.set_state(CharacterState.walk):
                        char2.x += char2.vel
                        char2.direction = CharacterDirection.right
                        char.direction = CharacterDirection.right
                        char.x += char.vel

                else:
                    char2.set_state(CharacterState.idle)

        # if enem.dead:
        #     enem.set_state(EnemyState.dead)
        # elif enem.bg == enem.def_bg and enem.quest:
        #     if abs(char.x - enem.x) <= 30 and enem.direction == CharacterDirection.left:
        #         if char.life > 0:
        #             enem.set_state(EnemyState.attack)
        #             if char.rotate.cur_eagle < 0.1:
        #                 char.rotate.rotate()
        #                 char.life -= 1
        #         else:
        #             enem.set_state(EnemyState.idle)
        #
        #     # elif char.x - enem.x >= 30 and enem.direction == EnemyDirection.right:
        #     #     enem.set_state(EnemyState.attack)
        #
        #     elif enem.rect.colliderect(char.char_rect) and enem.state != 1:
        #         if char.x < enem.x:
        #             logging.info("enemy walk left.")
        #
        #             if enem.set_state(EnemyState.walk):
        #                 enem.direction = CharacterDirection.left
        #                 enem.x -= enem.vel
        #
        #         elif char.x > enem.x:
        #             logging.info("enemy walk right.")
        #
        #             if enem.set_state(EnemyState.walk):
        #                 enem.x += enem.vel
        #                 enem.direction = CharacterDirection.right
        #
        #     else:
        #         enem.set_state(EnemyState.idle)
        #
        #
        # if keir.rect.colliderect(char.char_rect) and not keir.showed:
        #     char.quest_2 = True
        if professor.rect.colliderect(char2.char_rect) and not professor.showed:
            char2.quest = True
        if rectangle.colliderect(char2.char_rect) and bgs_names[last_r] == 'locker_room':
            yep = True
        else:
            yep = False

        professor.redraw_screen()
        manlab1.redraw_screen()
        womanlab1.redraw_screen()
        char2.redraw_screen()
        game.decor()

        last_r = last + game.is_collided(char2, last_r)
        char.x = char2.x
        bg = bgs[last_r]
        game.bg = bgs_names[last_r]
        char2.bg = bgs_names[last_r]
        professor.bg = bgs_names[last_r]
        womanlab1.bg = bgs_names[last_r]
        manlab1.bg = bgs_names[last_r]
        # if game.in_tavern:
        #     win.blit(pygame.image.load(ASSET_DIRECTORY + 'tavern_tree.png'), (0, 0))
        last = last_r

        if char.life <= 0:
            char.set_state_force(CharacterState.dead)
            myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel.ttf', 100)
            textsurface = myfont.render('Вы проиграли', False, (255, 255, 255))
            win.blit(textsurface, (150, 200))

        # <<<<  ПРОСТО МЕГА ВАЖНО  >>>>>
        # if kadr == 384:
        #     kadr = 0
        # kadr += 1
        # win.blit(pygame.image.load(ASSET_DIRECTORY + 'spacebg.png'), (0 - kadr * 3, 0))

        pygame.display.update()
    elif part2:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.unicode == 'u':
                pressed_attack = True

            if event.type == pygame.KEYDOWN and event.unicode == 'q' and not char.quest_2:
                pass

            if event.type == pygame.KEYDOWN and event.unicode == ' ':
                if char.quest:
                    if n_text % 2 == 0:
                        mann.n_text += 3
                    if n_text % 2 != 0:
                        char.n_text += 3
                    n_text += 1
                elif char.quest_2:
                    brend.n_text += 3
                    n_text += 1
                # elif char.quest_2:
                #     if n_text % 2 == 0:
                #         char.n_text += 1
                #     if n_text % 2 != 0:
                #         keir.n_text += 1
                #     n_text += 1
            logging.info(event)

        if end:
            char.set_state(CharacterState.idle)
        elif char.quest and char.life > 0:
            mann.win.blit(pygame.transform.scale(pygame.image.load(ASSET_DIRECTORY + 'panel.png'), (900, 300)),
                               (56, -50))
            char.set_state(CharacterState.idle)
            mann.set_state(NPCState.talk)
            keys = pygame.key.get_pressed()
            print(n_text)
            if n_text == 2:
                n_text = 0
                char.n_text = 0
                mann.showed = True
                mann.set_state(NPCState.idle)
                char.quest = False
            else:
                myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel2.ttf', 25)
                if n_text % 2 == 0:
                    mann.set_state(NPCState.talk)
                    textsurface_2 = myfont.render('Доктор Манн:', False, (0, 0, 0))
                    textline1 = myfont.render(mann.text[mann.n_text], False, (0, 0, 0))
                    textline2 = myfont.render(mann.text[mann.n_text + 1], False, (0, 0, 0))
                    textline3 = myfont.render(mann.text[mann.n_text + 2], False, (0, 0, 0))
                    win.blit(textline1, (150, 85))
                    win.blit(textline2, (150, 110))
                    win.blit(textline3, (150, 135))
                    win.blit(textsurface_2, (150, 35))
                if n_text % 2 != 0:
                    mann.set_state(NPCState.idle)
                    textsurface_2 = myfont.render('Базз:', False, (0, 0, 0))
                    textline1 = myfont.render(char.text[char.n_text], False, (0, 0, 0))
                    textline2 = myfont.render(char.text[char.n_text + 1], False, (0, 0, 0))
                    textline3 = myfont.render(char.text[char.n_text + 2], False, (0, 0, 0))
                    win.blit(textline1, (150, 85))
                    win.blit(textline2, (150, 110))
                    win.blit(textline3, (150, 135))
                    win.blit(textsurface_2, (150, 35))
        elif char.quest_2 and char.life > 0:
            brend.win.blit(pygame.transform.scale(pygame.image.load(ASSET_DIRECTORY + 'panel.png'), (900, 300)),
                               (56, -50))
            char.set_state(CharacterState.idle)
            brend.set_state(NPCState.talk)
            keys = pygame.key.get_pressed()
            print(n_text)
            if n_text == 1:
                n_text = 0
                char.n_text = 0
                brend.showed = True
                brend.set_state(NPCState.idle)
                char.quest_2 = False
            else:
                myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel2.ttf', 25)
                textsurface_2 = myfont.render('Амелия:', False, (0, 0, 0))
                textline1 = myfont.render(brend.text[brend.n_text], False, (0, 0, 0))
                textline2 = myfont.render(brend.text[brend.n_text + 1], False, (0, 0, 0))
                textline3 = myfont.render(brend.text[brend.n_text + 2], False, (0, 0, 0))
                win.blit(textline1, (150, 85))
                win.blit(textline2, (150, 110))
                win.blit(textline3, (150, 135))
                win.blit(textsurface_2, (150, 35))


        #
        # elif char.quest_2 and char.life > 0:
        #     keir.win.blit(pygame.transform.scale(pygame.image.load(ASSET_DIRECTORY + 'panel.png'), (900, 300)), (56, -50))
        #     char.set_state(CharacterState.idle)
        #     keys = pygame.key.get_pressed()
        #     print(n_text)
        #     if n_text == 5:
        #         keir.showed = True
        #         char.quest_2 = False
        #         enem.quest = True
        #     if n_text % 2 == 0:
        #         myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel.ttf', 20)
        #         textsurface = myfont.render(char.text_2[char.n_text], False, (0, 0, 0))
        #         textsurface_2 = myfont.render('Геральт:', False, (0, 0, 0))
        #         win.blit(textsurface, (150, 85))
        #         win.blit(textsurface_2, (150, 35))
        #     elif n_text % 2 != 0:
        #         myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel.ttf', 20)
        #         textsurface = myfont.render(keir.text[keir.n_text], False, (0, 0, 0))
        #         textsurface_2 = myfont.render('Кейр:', False, (0, 0, 0))
        #         win.blit(textsurface, (150, 85))
        #         win.blit(textsurface_2, (150, 35))

        elif char.life > 0 and not part_end:
            if pressed_attack:
                logging.info("key pressed attack.")
                if char.state == CharacterState.idle:
                    # if char.attack(enem):
                    #     enem.hp -= 35
                    #     enem.rotate.rotate()
                    #     if enem.hp <= 0:
                    #         enem.set_state(EnemyState.dead)
                    #         enem.dead = True
                    #         logging.info("Death")
                    char.set_state(CharacterState.attack)
                # elif char.state == CharacterState.attack:
                #     if char.attack(enem):
                #         enem.hp -= 35
                #         enem.rotate.rotate()
                #         if enem.hp <= 0:
                #             enem.set_state(EnemyState.dead)
                #             enem.dead = True
                #             logging.info("Death")
                #     char.set_state(CharacterState.attack2)
                # elif char.state == CharacterState.attack2:
                #     if char.attack(enem):
                #         enem.hp -= 35
                #         enem.rotate.rotate()
                #         if enem.hp <= 0:
                #             enem.set_state(EnemyState.dead)
                #             enem.dead = True
                #             logging.info("Death")
                #     char.set_state(CharacterState.attack3)
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a] and char.x > char.vel - 200:
                    logging.info("key pressed walk left.")

                    if char.set_state(CharacterState.walk):
                        char.direction = CharacterDirection.left
                        char.x -= char.vel

                elif keys[pygame.K_d] and char.x < 1100 - char.vel:
                    logging.info("key pressed walk right.")

                    if char.set_state(CharacterState.walk):
                        char.x += char.vel
                        char.direction = CharacterDirection.right

                else:
                    char.set_state(CharacterState.idle)

        # if enem.dead:
        #     enem.set_state(EnemyState.dead)
        # elif enem.bg == enem.def_bg and enem.quest:
        #     if abs(char.x - enem.x) <= 30 and enem.direction == CharacterDirection.left:
        #         if char.life > 0:
        #             enem.set_state(EnemyState.attack)
        #             if char.rotate.cur_eagle < 0.1:
        #                 char.rotate.rotate()
        #                 char.life -= 1
        #         else:
        #             enem.set_state(EnemyState.idle)
        #
        #     # elif char.x - enem.x >= 30 and enem.direction == EnemyDirection.right:
        #     #     enem.set_state(EnemyState.attack)
        #
        #     elif enem.rect.colliderect(char.char_rect) and enem.state != 1:
        #         if char.x < enem.x:
        #             logging.info("enemy walk left.")
        #
        #             if enem.set_state(EnemyState.walk):
        #                 enem.direction = CharacterDirection.left
        #                 enem.x -= enem.vel
        #
        #         elif char.x > enem.x:
        #             logging.info("enemy walk right.")
        #
        #             if enem.set_state(EnemyState.walk):
        #                 enem.x += enem.vel
        #                 enem.direction = CharacterDirection.right
        #
        #     else:
        #         enem.set_state(EnemyState.idle)
        #
        #
        # if keir.rect.colliderect(char.char_rect) and not keir.showed:
        #     char.quest_2 = True
        if professor.rect.colliderect(char2.char_rect) and not professor.showed:
            char2.quest = True
        if mann.rect.colliderect(char.char_rect) and not mann.showed:
            char.quest = True
        if brend.rect.colliderect(char.char_rect) and not brend.showed:
            char.quest_2 = True
        if end_of_part2.colliderect(char.char_rect) and bgs_names[last_r] == 'lab' and brend.showed:
            part_end = True

        if first_time:
            char.x = 2000

        professor.redraw_screen()
        manlab1.redraw_screen()
        womanlab1.redraw_screen()
        mann.redraw_screen()
        brend.redraw_screen()
        char.redraw_screen()

        game.decor()

        last_r = last + game.is_collided(char, last_r)
        bg = bgs[last_r]
        mann.bg = bgs_names[last_r]
        brend.bg = bgs_names[last_r]
        game.bg = bgs_names[last_r]
        char2.bg = bgs_names[last_r]
        professor.bg = bgs_names[last_r]
        # if game.in_tavern:
        #     win.blit(pygame.image.load(ASSET_DIRECTORY + 'tavern_tree.png'), (0, 0))
        last = last_r

        if first_time:
            if numbe != 255:
                numbe += 3
                rectsi.set_alpha(numbe)
                char2.set_state(CharacterState.idle)
                char2.redraw_screen()
                win.blit(rectsi, (0, 0))
            else:
                win.blit(rectsi, (0, 0))
                mann.x = 700
                brend.x = 350
                char.x = char2.x
                first_time = False
        elif not part_end:
            if numbe != 0:
                numbe -= 3
                rectsi.set_alpha(numbe)
                win.blit(rectsi, (0, 0))

        elif part_end:
            if numbe != 255:
                numbe += 3
                rectsi.set_alpha(numbe)
                char.set_state(CharacterState.idle)
                myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel2.ttf', 50)
                textsurface = myfont.render('Спустя месяцы полёта...', False, (255, 255, 255))
                textsurface.set_alpha(numbe)
                win.blit(rectsi, (0, 0))
                win.blit(textsurface, (150, 200))
            else:
                win.blit(rectsi, (0, 0))
                win.blit(textsurface, (150, 200))
                part2 = False
                part3 = True
                first_time = True
                part_end = False

        if char.life <= 0:
            char.set_state_force(CharacterState.dead)
            myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel.ttf', 100)
            textsurface = myfont.render('Вы проиграли', False, (255, 255, 255))
            win.blit(textsurface, (150, 200))

        # <<<<  ПРОСТО МЕГА ВАЖНО  >>>>>
        # if kadr == 384:
        #     kadr = 0
        # kadr += 1
        # win.blit(pygame.image.load(ASSET_DIRECTORY + 'spacebg.png'), (0 - kadr * 3, 0))

        pygame.display.update()
    elif part3:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.unicode == 'u':
                if timeb > 100 and not box_showed and sheila.showed2 and sheila.showed:
                    timeb = 0
                    gga = 1
                    pressed_attack = True
                    bullets['bullet' + str(num_bullets)] = Bullet(char.x, 315, win, ASSET_DIRECTORY, char.direction)
                    num_bullets += 1

            if event.type == pygame.KEYDOWN and event.unicode == 'q' and not char.quest_2:
                pass

            if event.type == pygame.KEYDOWN and event.unicode == ' ':
                if char.quest and not sheila.showed2:
                    sheila.n_text += 3
                    n_text += 1
                elif char.quest_2:
                    if n_text % 2 == 0:
                        sheila.n_text += 3
                    if n_text % 2 != 0:
                        char.n_text += 3
                    n_text += 1
                elif char.quest_3:
                    if n_text % 2 == 0:
                        char.n_text += 3
                    if n_text % 2 != 0:
                        sheila.n_text += 3
                    n_text += 1
                # elif char.quest_2:
                #     if n_text % 2 == 0:
                #         char.n_text += 1
                #     if n_text % 2 != 0:
                #         keir.n_text += 1
                #     n_text += 1
            logging.info(event)

        if end:
            char.set_state(CharacterState.idle)
        elif char.quest and char.life > 0 and not sheila.showed2:
            sheila.win.blit(pygame.transform.scale(pygame.image.load(ASSET_DIRECTORY + 'panel.png'), (900, 300)),
                           (56, -50))
            char.set_state(CharacterState.idle)
            keys = pygame.key.get_pressed()
            if n_text == 1:
                n_text = 0
                char.n_text = 0
                sheila.showed = True
                sheila.set_state(NPCState.idle)
                char.quest = False
            else:
                myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel2.ttf', 25)
                textsurface_2 = myfont.render('Шейла:', False, (0, 0, 0))
                textline1 = myfont.render(sheila.text[sheila.n_text], False, (0, 0, 0))
                textline2 = myfont.render(sheila.text[sheila.n_text + 1], False, (0, 0, 0))
                textline3 = myfont.render(sheila.text[sheila.n_text + 2], False, (0, 0, 0))
                win.blit(textline1, (150, 85))
                win.blit(textline2, (150, 110))
                win.blit(textline3, (150, 135))
                win.blit(textsurface_2, (150, 35))
        elif sheila.showed and not sheila.showed2:
            if sheila.alph != 0:
                sheila.alph -= 3
            else:
                sheila.default = 'ship2'
                sheila.x = 500
                sheila.rect = sheila.sheila_sprite.get_rect(topleft=(-1000, -1000))
                sheila.showed = False
                sheila.showed2 = True
                sheila.alph = 255
        elif char.quest_2 and char.life > 0:
            sheila.win.blit(pygame.transform.scale(pygame.image.load(ASSET_DIRECTORY + 'panel.png'), (900, 300)),
                          (56, -50))
            char.set_state(CharacterState.idle)
            keys = pygame.key.get_pressed()
            if n_text == 5:
                n_text = 0
                sheila.showed = True
                sheila.set_state(NPCState.idle)
                char.quest_2 = False
            else:
                myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel2.ttf', 25)
                if n_text % 2 == 0:
                    logging.info(sheila.n_text)
                    textsurface_2 = myfont.render('Шейла:', False, (0, 0, 0))
                    textline1 = myfont.render(sheila.text[sheila.n_text], False, (0, 0, 0))
                    textline2 = myfont.render(sheila.text[sheila.n_text + 1], False, (0, 0, 0))
                    textline3 = myfont.render(sheila.text[sheila.n_text + 2], False, (0, 0, 0))
                    win.blit(textline1, (150, 85))
                    win.blit(textline2, (150, 110))
                    win.blit(textline3, (150, 135))
                    win.blit(textsurface_2, (150, 35))
                if n_text % 2 != 0:
                    sheila.set_state(NPCState.idle)
                    textsurface_2 = myfont.render('Базз:', False, (0, 0, 0))
                    textline1 = myfont.render(char.text_2[char.n_text], False, (0, 0, 0))
                    textline2 = myfont.render(char.text_2[char.n_text + 1], False, (0, 0, 0))
                    textline3 = myfont.render(char.text_2[char.n_text + 2], False, (0, 0, 0))
                    win.blit(textline1, (150, 85))
                    win.blit(textline2, (150, 110))
                    win.blit(textline3, (150, 135))
                    win.blit(textsurface_2, (150, 35))
        elif box:
            char.set_state(CharacterState.idle)
            if numbi != 3:
                pass
                numbi -= 7
                heh = list(game.decors['ship2'].keys())[0]
                heh.set_alpha(numbi)
                win.blit(heh, list(game.decors['ship2'].values())[0])
            else:
                box = False
                box_showed = True
                sh3 = True
        elif char.quest_3:
            sheila.win.blit(pygame.transform.scale(pygame.image.load(ASSET_DIRECTORY + 'panel.png'), (900, 300)),
                            (56, -50))
            char.set_state(CharacterState.idle)
            keys = pygame.key.get_pressed()
            print(n_text)
            if n_text == 4:
                n_text = 0
                char.n_text = 0
                sheila.showed = True
                sh3 = False
                sheila.set_state(NPCState.idle)
                char.quest_3 = False
                part_end = True
            else:
                myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel2.ttf', 25)
                if n_text % 2 == 0:
                    sheila.set_state(NPCState.idle)
                    textsurface_2 = myfont.render('Базз:', False, (0, 0, 0))
                    textline1 = myfont.render(char.text_2[char.n_text], False, (0, 0, 0))
                    textline2 = myfont.render(char.text_2[char.n_text + 1], False, (0, 0, 0))
                    textline3 = myfont.render(char.text_2[char.n_text + 2], False, (0, 0, 0))
                    win.blit(textline1, (150, 85))
                    win.blit(textline2, (150, 110))
                    win.blit(textline3, (150, 135))
                    win.blit(textsurface_2, (150, 35))
                if n_text % 2 != 0:
                    logging.info(sheila.n_text)
                    textsurface_2 = myfont.render('Шейла:', False, (0, 0, 0))
                    textline1 = myfont.render(sheila.text[sheila.n_text], False, (0, 0, 0))
                    textline2 = myfont.render(sheila.text[sheila.n_text + 1], False, (0, 0, 0))
                    textline3 = myfont.render(sheila.text[sheila.n_text + 2], False, (0, 0, 0))
                    win.blit(textline1, (150, 85))
                    win.blit(textline2, (150, 110))
                    win.blit(textline3, (150, 135))
                    win.blit(textsurface_2, (150, 35))

        #
        # elif char.quest_2 and char.life > 0:
        #     keir.win.blit(pygame.transform.scale(pygame.image.load(ASSET_DIRECTORY + 'panel.png'), (900, 300)), (56, -50))
        #     char.set_state(CharacterState.idle)
        #     keys = pygame.key.get_pressed()
        #     print(n_text)
        #     if n_text == 5:
        #         keir.showed = True
        #         char.quest_2 = False
        #         enem.quest = True
        #     if n_text % 2 == 0:
        #         myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel.ttf', 20)
        #         textsurface = myfont.render(char.text_2[char.n_text], False, (0, 0, 0))
        #         textsurface_2 = myfont.render('Геральт:', False, (0, 0, 0))
        #         win.blit(textsurface, (150, 85))
        #         win.blit(textsurface_2, (150, 35))
        #     elif n_text % 2 != 0:
        #         myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel.ttf', 20)
        #         textsurface = myfont.render(keir.text[keir.n_text], False, (0, 0, 0))
        #         textsurface_2 = myfont.render('Кейр:', False, (0, 0, 0))
        #         win.blit(textsurface, (150, 85))
        #         win.blit(textsurface_2, (150, 35))

        elif char.life > 0 and not part_end and not first_time:
            if pressed_attack:
                logging.info("key pressed attack.")
                if char.state == CharacterState.idle:
                    # if char.attack(enem):
                    #     enem.hp -= 35
                    #     enem.rotate.rotate()
                    #     if enem.hp <= 0:
                    #         enem.set_state(EnemyState.dead)
                    #         enem.dead = True
                    #         logging.info("Death")
                    char.set_state(CharacterState.attack)
                # elif char.state == CharacterState.attack:
                #     if char.attack(enem):
                #         enem.hp -= 35
                #         enem.rotate.rotate()
                #         if enem.hp <= 0:
                #             enem.set_state(EnemyState.dead)
                #             enem.dead = True
                #             logging.info("Death")
                #     char.set_state(CharacterState.attack2)
                # elif char.state == CharacterState.attack2:
                #     if char.attack(enem):
                #         enem.hp -= 35
                #         enem.rotate.rotate()
                #         if enem.hp <= 0:
                #             enem.set_state(EnemyState.dead)
                #             enem.dead = True
                #             logging.info("Death")
                #     char.set_state(CharacterState.attack3)
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a] and char.x > char.vel - 200:
                    logging.info("key pressed walk left.")

                    if char.set_state(CharacterState.walk):
                        char.direction = CharacterDirection.left
                        char.x -= char.vel

                elif keys[pygame.K_d] and char.x < 1100 - char.vel:
                    logging.info("key pressed walk right.")

                    if char.set_state(CharacterState.walk):
                        char.x += char.vel
                        char.direction = CharacterDirection.right

                else:
                    char.set_state(CharacterState.idle)

        # if enem.dead:
        #     enem.set_state(EnemyState.dead)
        # elif enem.bg == enem.def_bg and enem.quest:
        #     if abs(char.x - enem.x) <= 30 and enem.direction == CharacterDirection.left:
        #         if char.life > 0:
        #             enem.set_state(EnemyState.attack)
        #             if char.rotate.cur_eagle < 0.1:
        #                 char.rotate.rotate()
        #                 char.life -= 1
        #         else:
        #             enem.set_state(EnemyState.idle)
        #
        #     # elif char.x - enem.x >= 30 and enem.direction == EnemyDirection.right:
        #     #     enem.set_state(EnemyState.attack)
        #
        #     elif enem.rect.colliderect(char.char_rect) and enem.state != 1:
        #         if char.x < enem.x:
        #             logging.info("enemy walk left.")
        #
        #             if enem.set_state(EnemyState.walk):
        #                 enem.direction = CharacterDirection.left
        #                 enem.x -= enem.vel
        #
        #         elif char.x > enem.x:
        #             logging.info("enemy walk right.")
        #
        #             if enem.set_state(EnemyState.walk):
        #                 enem.x += enem.vel
        #                 enem.direction = CharacterDirection.right
        #
        #     else:
        #         enem.set_state(EnemyState.idle)
        #
        #
        # if keir.rect.colliderect(char.char_rect) and not keir.showed:
        #     char.quest_2 = True
        if sheila.rect.colliderect(char.char_rect) and not sheila.showed:
            char.quest = True
        if sheila.rect.colliderect(char.char_rect) and not sheila.showed and sheila.showed2:
            char.quest_2 = True
        if sheila.rect.colliderect(char.char_rect) and sh3 and box_showed:
            char.quest_3 = True
        # if mann.rect.colliderect(char.char_rect) and not mann.showed:
        #     char.quest = True
        # if brend.rect.colliderect(char.char_rect) and not brend.showed:
        #     char.quest_2 = True
        # if end_of_part2.colliderect(char.char_rect) and bgs_names[last_r] == 'lab' and brend.showed:
        #     part_end = True
        sheila.redraw_screen()
        char.redraw_screen()
        timeb += 1

        if not box_showed:
            game.decor()

        last_r = last + game.is_collided(char, last_r)
        bg = bgs[last_r]
        game.bg = bgs_names[last_r]
        sheila.bg = bgs_names[last_r]
        # if game.in_tavern:
        #     win.blit(pygame.image.load(ASSET_DIRECTORY + 'tavern_tree.png'), (0, 0))
        last = last_r

        for name, bullet in bullets.items():
            if bullet.delete:
                del_bullets.append(name)
            bullet.redraw_screen()
            if list(game.decors['ship2'].keys())[0].get_rect(topleft=list(game.decors['ship2'].values())[0]).colliderect(
                    bullet.rect) and not box_showed and bgs_names[last_r] == 'ship2':
                box = True
        for del_bullet in del_bullets:
            bullets.pop(del_bullet)
        del_bullets.clear()

        if first_time:
            if numbe == 255:
                win.blit(rectsi, (0, 0))
                win.blit(textsurface, (150, 200))
                sheila.x = 250
                char.quest = False
                char.quest_2 = False
                bgs_names = ['ship2', 'ship']
                bgs = [pygame.image.load(ASSET_DIRECTORY + 'ship2.png'),
                       pygame.image.load(ASSET_DIRECTORY + 'ship.png')]
                last_r = 1
                last = 1
                bg = bgs[last_r]
                char.x = 700
            if numbe != 0:
                numbe -= 3
                textsurface.set_alpha(numbe)
                rectsi.set_alpha(numbe)
                char.set_state(CharacterState.idle)
                win.blit(rectsi, (0, 0))
                win.blit(textsurface, (150, 200))
            else:
                win.blit(rectsi, (0, 0))
                first_time = False

        elif part_end:
            if numbe != 255:
                numbe += 3
                rectsi.set_alpha(numbe)
                char.set_state(CharacterState.idle)
                win.blit(rectsi, (0, 0))
            else:
                win.blit(rectsi, (0, 0))
                part3 = False
                part4 = True
                first_time = True
                part_end = False

        if char.life <= 0:
            char.set_state_force(CharacterState.dead)
            myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel.ttf', 100)
            textsurface = myfont.render('Вы проиграли', False, (255, 255, 255))
            win.blit(textsurface, (150, 200))

        # <<<<  ПРОСТО МЕГА ВАЖНО  >>>>>
        # if kadr == 384:
        #     kadr = 0
        # kadr += 1
        # win.blit(pygame.image.load(ASSET_DIRECTORY + 'spacebg.png'), (0 - kadr * 3, 0))

        pygame.display.update()
    elif part4:
        timeb += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.unicode == 'u':
                pass

            if event.type == pygame.KEYDOWN and event.unicode == 'q' and not char.quest_2:
                pass
            if event.type == pygame.KEYDOWN:
                all_events += event.unicode

        if char.life > 0 and not part_end and not first_time:
            if pressed_attack:
                logging.info("key pressed attack.")
                if char.state == CharacterState.idle:
                    char.set_state(CharacterState.attack)
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_s] and keys[pygame.K_d] and starship1.y < 416 and starship1.x < 800:
                    logging.info("key pressed walk down.")
                    starship1.x += starship1.vel
                    starship1.y += starship1.vel
                elif keys[pygame.K_s] and starship1.y < 416 and keys[pygame.K_a] and starship1.x > starship1.vel - 200:
                    starship1.y += starship1.vel
                    starship1.x -= starship1.vel
                elif keys[pygame.K_w] and starship1.y > 0 and keys[pygame.K_a] and starship1.x > starship1.vel - 200:
                    starship1.x -= starship1.vel
                    starship1.y -= starship1.vel
                elif keys[pygame.K_w] and starship1.y > 0 and keys[pygame.K_d] and starship1.x < 800:
                    starship1.y -= starship1.vel
                    starship1.x += starship1.vel

                elif keys[pygame.K_a] and starship1.x > starship1.vel - 200:
                    logging.info("key pressed walk left.")
                    starship1.x -= starship1.vel

                elif keys[pygame.K_d] and starship1.x < 800:
                    logging.info("key pressed walk right.")
                    starship1.x += starship1.vel

                elif keys[pygame.K_w] and starship1.y > 0:
                    logging.info("key pressed walk up.")
                    starship1.y -= starship1.vel

                elif keys[pygame.K_s] and starship1.y < 416:
                    logging.info("key pressed walk down.")
                    starship1.y += starship1.vel

        if kadr == 192:
            kadr = 0



        # 1153
        kadr += 1
        win.blit(pygame.image.load(ASSET_DIRECTORY + 'spacebg.png'), (0 - kadr * 6, 0))
        starship1.redraw_screen()
        aster = pygame.image.load(ASSET_DIRECTORY + 'asteroid1.png')
        if timeb <= 144:
            win.blit(aster, (316 - timeb * 8, 426))
            if collide(316 - timeb * 8, 426):
                first_time, numbe = True, 255

            win.blit(aster, (697 - timeb * 8, 36))
            if collide(697 - timeb * 8, 36):
                first_time, numbe = True, 255

            win.blit(aster, (904 - timeb * 8, 357))
            if collide(904 - timeb * 8, 357):
                first_time, numbe = True, 255

        if timeb <= 288:
            win.blit(aster, (316 + 1153 - timeb * 8, 38))
            if collide(316 + 1153 - timeb * 8, 38):
                first_time, numbe = True, 255

            win.blit(aster, (608 + 1153 - timeb * 8, 364))
            if collide(608 + 1153 - timeb * 8, 364):
                first_time, numbe = True, 255

            win.blit(aster, (956 + 1153 - timeb * 8, 225))
            if collide(956 + 1153 - timeb * 8, 225):
                first_time, numbe = True, 255

        if timeb <= 432:
            win.blit(aster, (316 + 2306 - timeb * 8, 38))
            if collide(316 + 2306 - timeb * 8, 38):
                first_time, numbe = True, 255

            win.blit(aster, (316 + 2306 - timeb * 8, 394))
            if collide(316 + 2306 - timeb * 8, 394):
                first_time, numbe = True, 255

            win.blit(aster, (787 + 2306 - timeb * 8, 219))
            if collide(787 + 2306 - timeb * 8, 219):
                first_time, numbe = True, 255

        if timeb <= 576:
            win.blit(aster, (134 + 3459 - timeb * 8, 270))
            if collide(134 + 3459 - timeb * 8, 270):
                first_time, numbe = True, 255

            win.blit(aster, (483 + 3459 - timeb * 8, 63))
            if collide(483 + 3459 - timeb * 8, 63):
                first_time, numbe = True, 255

            win.blit(aster, (949 + 3459 - timeb * 8, 344))
            if collide(949 + 3459 - timeb * 8, 344):
                first_time, numbe = True, 255

        if timeb <= 720:
            win.blit(aster, (316 + 4612 - timeb * 8, 200))
            if collide(316 + 4612 - timeb * 8, 200):
                first_time, numbe = True, 255

            win.blit(aster, (697 + 4612 - timeb * 8, 36))
            if collide(697 + 4612 - timeb * 8, 36):
                first_time, numbe = True, 255

            win.blit(aster, (904 + 4612 - timeb * 8, 357))
            if collide(904 + 4612 - timeb * 8, 357):
                first_time, numbe = True, 255

        if timeb <= 864:
            win.blit(aster, (316 + 5765 - timeb * 8, 38))
            if collide(316 + 5765 - timeb * 8, 38):
                first_time, numbe = True, 255

            win.blit(aster, (608 + 5765 - timeb * 8, 364))
            if collide(608 + 5765 - timeb * 8, 364):
                first_time, numbe = True, 255

            win.blit(aster, (956 + 5765 - timeb * 8, 225))
            if collide(956 + 5765 - timeb * 8, 225):
                first_time, numbe = True, 255

        if timeb <= 1008:
            win.blit(aster, (316 + 6918 - timeb * 8, 38))
            if collide(316 + 6918 - timeb * 8, 38):
                first_time, numbe = True, 255

            win.blit(aster, (316 + 6918 - timeb * 8, 394))
            if collide(316 + 6918 - timeb * 8, 394):
                first_time, numbe = True, 255

            win.blit(aster, (787 + 6918 - timeb * 8, 219))
            if collide(787 + 6918 - timeb * 8, 219):
                first_time, numbe = True, 255

        if timeb <= 1152:
            win.blit(aster, (134 + 8071 - timeb * 8, 370))
            if collide(134 + 8071 - timeb * 8, 370):
                first_time, numbe = True, 255

            win.blit(aster, (483 + 8071 - timeb * 8, 63))
            if collide(483 + 8071 - timeb * 8, 63):
                first_time, numbe = True, 255

            win.blit(aster, (949 + 8071 - timeb * 8, 344))
            if collide(949 + 8071 - timeb * 8, 344):
                first_time, numbe = True, 255

        logging.info(timeb)
        if timeb >= 1153 or all_events[-1:-8:-1] == 'mayoseh':
            part_end = True
        # 1153

        if first_time:
            if numbe == 255:
                win.blit(rectsi, (0, 0))
            if numbe != 0:
                numbe -= 3
                rectsi.set_alpha(numbe)
                char.set_state(CharacterState.idle)
                win.blit(rectsi, (0, 0))
            else:
                win.blit(rectsi, (0, 0))
                first_time = False
            starship1.x, starship1.y, timeb, kadr = 100, 245, 0, 0

        elif part_end:
            if numbe != 255:
                numbe += 3
                rectsi.set_alpha(numbe)
                char.set_state(CharacterState.idle)
                win.blit(rectsi, (0, 0))
            else:
                win.blit(rectsi, (0, 0))
                part4 = False
                part5 = True
                first_time = True
                part_end = False
            timeb = 1152

        # <<<<  ПРОСТО МЕГА ВАЖНО  >>>>>
        pygame.display.update()
    elif part5:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.unicode == 'u':
                pass

            if event.type == pygame.KEYDOWN and event.unicode == 'q' and not char.quest_2:
                pass

            if event.type == pygame.KEYDOWN and event.unicode == ' ':
                if char.quest:
                    n_text += 1
                elif char.quest_2:
                    n_text += 1
                elif char.quest_3:
                    if n_text % 2 == 0:
                        char.n_text += 3
                    if n_text % 2 != 0:
                        sheila.n_text += 3
                    n_text += 1
                # elif char.quest_2:
                #     if n_text % 2 == 0:
                #         char.n_text += 1
                #     if n_text % 2 != 0:
                #         keir.n_text += 1
                #     n_text += 1
            logging.info(event)

        if end:
            char.set_state(CharacterState.idle)
        elif char.quest and char.life > 0:
            sheila.win.blit(pygame.transform.scale(pygame.image.load(ASSET_DIRECTORY + 'panel.png'), (900, 300)),
                           (56, -50))
            char.set_state(CharacterState.idle)
            keys = pygame.key.get_pressed()
            if n_text == 1:
                print('yeah')
                n_text = 0
                char.n_text = 0
                planet.quest1_showed = True
                char.quest = False
            else:
                myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel2.ttf', 25)
                textsurface_2 = myfont.render('Базз:', False, (0, 0, 0))
                textline1 = myfont.render(planet.text1[n_text], False, (0, 0, 0))
                win.blit(textline1, (150, 85))
                win.blit(textsurface_2, (150, 35))
        elif char.quest_2 and char.life > 0:
            sheila.win.blit(pygame.transform.scale(pygame.image.load(ASSET_DIRECTORY + 'panel.png'), (900, 300)),
                            (56, -50))
            char.set_state(CharacterState.idle)
            keys = pygame.key.get_pressed()
            if n_text == 1:
                print('yeah')
                n_text = 0
                char.n_text = 0
                planet.quest2_showed = True
                char.quest_2 = False
            else:
                myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel2.ttf', 25)
                textsurface_2 = myfont.render('Базз:', False, (0, 0, 0))
                textline1 = myfont.render(planet.text2[n_text], False, (0, 0, 0))
                textline2 = myfont.render(planet.text2[n_text + 1], False, (0, 0, 0))
                textline3 = myfont.render(planet.text2[n_text + 2], False, (0, 0, 0))
                win.blit(textline2, (150, 110))
                win.blit(textline3, (150, 135))
                win.blit(textline1, (150, 85))
                win.blit(textsurface_2, (150, 35))
        elif char.quest_3:
            part_end = True

        elif char.life > 0 and not part_end and not first_time:
            if pressed_attack:
                logging.info("key pressed attack.")
                if char.state == CharacterState.idle:
                    char.set_state(CharacterState.attack)

            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a] and char.x > char.vel - 200:
                    logging.info("key pressed walk left.")

                    if char.set_state(CharacterState.walk):
                        char.direction = CharacterDirection.left
                        char.x -= char.vel

                elif keys[pygame.K_d] and char.x < 1100 - char.vel and bgs_names[last_r] != 'planet2':
                    logging.info("key pressed walk right.")

                    if char.set_state(CharacterState.walk):
                        char.x += char.vel
                        char.direction = CharacterDirection.right
                elif keys[pygame.K_d] and char.x < 875 - char.weight:
                    logging.info("key pressed walk right.")

                    if char.set_state(CharacterState.walk):
                        char.x += char.vel
                        char.direction = CharacterDirection.right

                else:
                    char.set_state(CharacterState.idle)

        char.redraw_screen()
        planet.redraw(char)
        timeb += 1

        game.decor()

        last_r = last + game.is_collided(char, last_r)
        bg = bgs[last_r]
        game.bg = bgs_names[last_r]
        planet.bg = bgs_names[last_r]

        last = last_r

        if first_time:
            if numbe == 255:
                win.blit(rectsi, (0, 0))
                # win.blit(textsurface, (150, 200))
                sheila.x = 250
                char.quest = False
                char.quest_2 = False
                char.quest_3 = False
                n_text = 0
                bgs_names = ['planet', 'planet2']
                bgs = [pygame.image.load(ASSET_DIRECTORY + 'planet.png'),
                       pygame.image.load(ASSET_DIRECTORY + 'planet2.png')]
                last_r = 0
                last = 0
                bg = bgs[last_r]
                char.x = 400
            if numbe != 0:
                numbe -= 3
                # textsurface.set_alpha(numbe)
                rectsi.set_alpha(numbe)
                char.set_state(CharacterState.idle)
                win.blit(rectsi, (0, 0))
                # win.blit(textsurface, (150, 200))
            else:
                win.blit(rectsi, (0, 0))
                first_time = False

        elif part_end:
            if numbe != 255:
                numbe += 3
                rectsi.set_alpha(numbe)
                char.set_state(CharacterState.idle)
                win.blit(rectsi, (0, 0))
            else:
                win.blit(rectsi, (0, 0))
                part5 = False
                part6 = True
                first_time = True
                part_end = False
        pygame.display.update()
    elif part6:
        if swim_char.quest:
            win.blit(pygame.image.load(ASSET_DIRECTORY + tab), (45, 212))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.unicode == 'u':
                pass

            if event.type == pygame.MOUSEBUTTONDOWN and swim_char.quest:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 51 <= mouse_x <= 101 and 415 <= mouse_y <= 542:
                    print('1')
                    piano_tabs.append('1')
                    tab = 'pianog1.png'
                    pygame.mixer.music.load(ASSET_DIRECTORY + '1.mp3')
                    pygame.mixer.music.play()
                elif 108 <= mouse_x <= 158 and 415 <= mouse_y <= 542:
                    print('2')
                    piano_tabs.append('2')
                    tab = 'pianog2.png'
                    pygame.mixer.music.load(ASSET_DIRECTORY + 'broken.mp3')
                    pygame.mixer.music.play()
                elif 165 <= mouse_x <= 207 and 415 <= mouse_y <= 542:
                    print('3')
                    piano_tabs.append('3')
                    tab = 'pianog3.png'
                    pygame.mixer.music.load(ASSET_DIRECTORY + '3.mp3')
                    pygame.mixer.music.play()
                elif 214 <= mouse_x <= 264 and 415 <= mouse_y <= 542:
                    print('4')
                    piano_tabs.append('4')
                    tab = 'pianog4.png'
                    pygame.mixer.music.load(ASSET_DIRECTORY + '4.mp3')
                    pygame.mixer.music.play()
                elif 270 <= mouse_x <= 320 and 415 <= mouse_y <= 542:
                    print('5')
                    piano_tabs.append('5')
                    tab = 'pianog5.png'
                    pygame.mixer.music.load(ASSET_DIRECTORY + 'broken.mp3')
                    pygame.mixer.music.play()
                elif 327 <= mouse_x <= 377 and 415 <= mouse_y <= 542:
                    print('6')
                    piano_tabs.append('6')
                    tab = 'pianog6.png'
                    pygame.mixer.music.load(ASSET_DIRECTORY + 'broken.mp3')
                    pygame.mixer.music.play()
                elif 384 <= mouse_x <= 426 and 415 <= mouse_y <= 542:
                    print('7')
                    piano_tabs.append('7')
                    tab = 'pianog7.png'
                    pygame.mixer.music.load(ASSET_DIRECTORY + '7.mp3')
                    pygame.mixer.music.play()
                elif 87 <= mouse_x <= 122 and 232 <= mouse_y <= 415:
                    print('1.1')
                    piano_tabs.append('1.1')
                    tab = 'pianog1.1.png'
                    pygame.mixer.music.load(ASSET_DIRECTORY + 'broken.mp3')
                    pygame.mixer.music.play()
                elif 144 <= mouse_x <= 179 and 232 <= mouse_y <= 415:
                    print('1.2')
                    piano_tabs.append('1.2')
                    tab = 'pianog1.2.png'
                    pygame.mixer.music.load(ASSET_DIRECTORY + '1.2.mp3')
                    pygame.mixer.music.play()
                elif 250 <= mouse_x <= 285 and 232 <= mouse_y <= 415:
                    print('1.3')
                    piano_tabs.append('1.3')
                    tab = 'pianog1.3.png'
                    pygame.mixer.music.load(ASSET_DIRECTORY + '1.3.mp3')
                    pygame.mixer.music.play()
                elif 306 <= mouse_x <= 341 and 232 <= mouse_y <= 415:
                    print('1.4')
                    piano_tabs.append('1.4')
                    tab = 'pianog1.4.png'
                    pygame.mixer.music.load(ASSET_DIRECTORY + '1.4.mp3')
                    pygame.mixer.music.play()
                elif 363 <= mouse_x <= 398 and 232 <= mouse_y <= 415:
                    print('1.5')
                    piano_tabs.append('1.5')
                    tab = 'pianog1.5.png'
                    pygame.mixer.music.load(ASSET_DIRECTORY + 'broken.mp3')
                    pygame.mixer.music.play()

            if event.type == pygame.MOUSEBUTTONUP and swim_char.quest:
                # mouse_x, mouse_y = pygame.mouse.get_pos()
                # if 51 <= mouse_x <= 101 and 415 <= mouse_y <= 542:
                #     print('1')
                # elif 108 <= mouse_x <= 158 and 415 <= mouse_y <= 542:
                #     print('2')
                # elif 165 <= mouse_x <= 207 and 415 <= mouse_y <= 542:
                #     print('3')
                # elif 214 <= mouse_x <= 264 and 415 <= mouse_y <= 542:
                #     print('4')
                # elif 270 <= mouse_x <= 320 and 415 <= mouse_y <= 542:
                #     print('5')
                # elif 327 <= mouse_x <= 377 and 415 <= mouse_y <= 542:
                #     print('6')
                # elif 384 <= mouse_x <= 426 and 415 <= mouse_y <= 542:
                #     print('7')
                # elif 87 <= mouse_x <= 122 and 232 <= mouse_y <= 415:
                #     print('1.1')
                # elif 144 <= mouse_x <= 179 and 232 <= mouse_y <= 415:
                #     print('1.2')
                # elif 250 <= mouse_x <= 285 and 232 <= mouse_y <= 415:
                #     print('1.3')
                # elif 306 <= mouse_x <= 341 and 232 <= mouse_y <= 415:
                #     print('1.4')
                # elif 363 <= mouse_x <= 398 and 232 <= mouse_y <= 415:
                #     print('1.5')
                tab = 'pianog.png'

            if event.type == pygame.KEYDOWN and event.unicode == 'q':
                if not swim_char.quest:
                    underwater.redraw(swim_char)
                else:
                    swim_char.quest = False

            if event.type == pygame.KEYDOWN and event.unicode == ' ':
                if swim_char.quest2:
                    n_text += 1
                # elif char.quest_2:
                #     n_text += 1
                # elif char.quest_3:
                #     if n_text % 2 == 0:
                #         char.n_text += 3
                #     if n_text % 2 != 0:
                #         sheila.n_text += 3
                #     n_text += 1
                pass
            logging.info(event)

        if end:
            char.set_state(CharacterState.idle)
        elif swim_char.quest and char.life > 0:
            sheila.win.blit(pygame.transform.scale(pygame.image.load(ASSET_DIRECTORY + 'panel.png'), (900, 300)),
                           (56, -50))
            swim_char.set_state(CharacterState.idle)
            keys = pygame.key.get_pressed()
            if piano_tabs[-1:-6:-1] == ['1.1', '5', '1.5', '6', '2']:
                print('yeah')
                # n_text = 0
                # char.n_text = 0
                underwater.quest1_showed = True
                swim_char.quest = False
                # char.quest = False

            myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel2.ttf', 25)
            textsurface_2 = myfont.render('Бумага у Дани...', False, (0, 0, 0))
            win.blit(textsurface_2, (150, 35))
        elif swim_char.quest2 and char.life > 0:
            sheila.win.blit(pygame.transform.scale(pygame.image.load(ASSET_DIRECTORY + 'panel.png'), (900, 300)),
                           (56, -50))
            keys = pygame.key.get_pressed()
            swim_char.set_state(CharacterState.idle)
            if n_text == 1:
                print('yeah')
                n_text = 0
                underwater.quest2_showed = True
                swim_char.quest2 = False
            else:
                myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel2.ttf', 25)
                textsurface_2 = myfont.render('Базз:', False, (0, 0, 0))
                textline1 = myfont.render(underwater.text2[0], False, (0, 0, 0))
                textline2 = myfont.render(underwater.text2[1], False, (0, 0, 0))
                textline3 = myfont.render(underwater.text2[2], False, (0, 0, 0))
                win.blit(textline2, (150, 110))
                win.blit(textline3, (150, 135))
                win.blit(textline1, (150, 85))
                win.blit(textsurface_2, (150, 35))

        if char.life > 0 and not part_end and not first_time and not swim_char.quest and not swim_char.quest2:
            if pressed_attack:
                logging.info("key pressed attack.")
                if char.state == CharacterState.idle:
                    char.set_state(CharacterState.attack)
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_s] and keys[pygame.K_d] and swim_char.y < 416 and swim_char.x < 800:
                    logging.info("key pressed walk down.")
                    swim_char.direction = CharacterDirection.right
                    swim_char.set_state(CharacterState.walk)
                    swim_char.x += swim_char.vel
                    swim_char.y += swim_char.vel
                elif keys[pygame.K_s] and swim_char.y < 416 and keys[pygame.K_a] and swim_char.x > swim_char.vel - 200:
                    swim_char.y += swim_char.vel
                    swim_char.x -= swim_char.vel
                    swim_char.set_state(CharacterState.walk)
                    swim_char.direction = CharacterDirection.left
                elif keys[pygame.K_w] and swim_char.y > 0 and keys[pygame.K_a] and swim_char.x > swim_char.vel - 200:
                    swim_char.x -= swim_char.vel
                    swim_char.set_state(CharacterState.walk)
                    swim_char.y -= swim_char.vel
                    swim_char.direction = CharacterDirection.left
                elif keys[pygame.K_w] and swim_char.y > 0 and keys[pygame.K_d] and swim_char.x < 800:
                    swim_char.direction = CharacterDirection.right
                    swim_char.y -= swim_char.vel
                    swim_char.set_state(CharacterState.walk)
                    swim_char.x += swim_char.vel

                elif keys[pygame.K_a] and swim_char.x > swim_char.vel - 200:
                    logging.info("key pressed walk left.")
                    swim_char.direction = CharacterDirection.left
                    swim_char.set_state(CharacterState.walk)
                    swim_char.x -= swim_char.vel

                elif keys[pygame.K_d] and swim_char.x < 800:
                    logging.info("key pressed walk right.")
                    swim_char.direction = CharacterDirection.right
                    swim_char.set_state(CharacterState.walk)
                    swim_char.x += swim_char.vel

                elif keys[pygame.K_w] and swim_char.y > 0:
                    logging.info("key pressed walk up.")
                    swim_char.y -= swim_char.vel
                    swim_char.set_state(CharacterState.walk)

                elif keys[pygame.K_s] and swim_char.y < 416:
                    logging.info("key pressed walk down.")
                    swim_char.set_state(CharacterState.walk)
                    swim_char.y += swim_char.vel
                else:
                    swim_char.set_state(CharacterState.idle)

        if swim_char.rect.colliderect(underwater_cube) and underwater.quest1_showed:
            part_end = True
        if swim_char.rect.colliderect(underwater_cube) and not underwater.quest2_showed:
            swim_char.quest2 = True

        swim_char.redraw_screen()

        game.decor()

        if first_time:
            if numbe == 255:
                win.blit(rectsi, (0, 0))
                # win.blit(textsurface, (150, 200))
                char.quest = False
                char.quest_2 = False
                char.quest_3 = False
                n_text = 0
                bgs_names = ['underwater1',
                             'underwater1']
                all_events = ''
                bgs = [pygame.image.load(ASSET_DIRECTORY + 'underwater1.png'),
                       pygame.image.load(ASSET_DIRECTORY + 'underwater1.png')]
                last_r = 0
                last = 0
                bg = bgs[last_r]
                char.x = 400
            if numbe != 0:
                numbe -= 3
                # textsurface.set_alpha(numbe)
                rectsi.set_alpha(numbe)
                char.set_state(CharacterState.idle)
                win.blit(rectsi, (0, 0))
                # win.blit(textsurface, (150, 200))
            else:
                win.blit(rectsi, (0, 0))
                first_time = False

        elif part_end:
            if numbe != 255:
                numbe += 3
                rectsi.set_alpha(numbe)
                char.set_state(CharacterState.idle)
                win.blit(rectsi, (0, 0))
            else:
                win.blit(rectsi, (0, 0))
                part6 = False
                part7 = True
                first_time = True
                part_end = False
        pygame.display.update()
    elif part7:
        if music:
            pygame.mixer.music.load(ASSET_DIRECTORY + 'bgmusic.mp3')
            pygame.mixer.music.play(-1)
            music = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.unicode == 'u':
                pass

            if event.type == pygame.KEYDOWN and event.unicode == 'q' and not char.quest_2:
                pass

            if event.type == pygame.KEYDOWN and event.unicode == ' ':
                if char.quest:
                    n_text += 1
                elif char.quest_2:
                    n_text += 3
                elif char.quest_3:
                    if n_text % 2 == 0:
                        char.n_text += 3
                    if n_text % 2 != 0:
                        sheila.n_text += 3
                    n_text += 1
                # elif char.quest_2:
                #     if n_text % 2 == 0:
                #         char.n_text += 1
                #     if n_text % 2 != 0:
                #         keir.n_text += 1
                #     n_text += 1
            logging.info(event)

        if end:
            char.set_state(CharacterState.idle)
        elif char.quest and char.life > 0:
            sheila.win.blit(pygame.transform.scale(pygame.image.load(ASSET_DIRECTORY + 'panel.png'), (900, 300)),
                           (56, -50))
            char.set_state(CharacterState.idle)
            keys = pygame.key.get_pressed()
            if n_text == 1:
                print('yeah')
                n_text = 0
                char.n_text = 0
                planet.quest1_showed = True
                char.quest = False
            else:
                myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel2.ttf', 25)
                textsurface_2 = myfont.render('Базз:', False, (0, 0, 0))
                textline1 = myfont.render(planet.text3[n_text], False, (0, 0, 0))
                win.blit(textline1, (150, 85))
                win.blit(textsurface_2, (150, 35))
        elif char.quest_2 and char.life > 0:
            sheila.win.blit(pygame.transform.scale(pygame.image.load(ASSET_DIRECTORY + 'panel.png'), (900, 300)),
                            (56, -50))
            char.set_state(CharacterState.idle)
            keys = pygame.key.get_pressed()
            if n_text == 15:
                print('end')
                n_text = 0
                char.n_text = 0
                planet.quest2_showed = True
                char.quest_2 = False
                part_end = True
            else:
                myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel2.ttf', 25)
                textsurface_2 = myfont.render('Кот:', False, (0, 0, 0))
                textline1 = myfont.render(planet.text4[n_text], False, (0, 0, 0))
                textline2 = myfont.render(planet.text4[n_text + 1], False, (0, 0, 0))
                textline3 = myfont.render(planet.text4[n_text + 2], False, (0, 0, 0))
                win.blit(textline2, (150, 110))
                win.blit(textline3, (150, 135))
                win.blit(textline1, (150, 85))
                win.blit(textsurface_2, (150, 35))

        elif char.life > 0 and not part_end and not first_time:
            if pressed_attack:
                logging.info("key pressed attack.")
                if char.state == CharacterState.idle:
                    char.set_state(CharacterState.attack)

            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a] and char.x > char.vel - 200:
                    logging.info("key pressed walk left.")

                    if char.set_state(CharacterState.walk):
                        char.direction = CharacterDirection.left
                        char.x -= char.vel

                elif keys[pygame.K_d] and char.x < 1100 - char.vel and bgs_names[last_r] != 'planet2':
                    logging.info("key pressed walk right.")

                    if char.set_state(CharacterState.walk):
                        char.x += char.vel
                        char.direction = CharacterDirection.right
                elif keys[pygame.K_d] and char.x < 875 - char.weight:
                    logging.info("key pressed walk right.")

                    if char.set_state(CharacterState.walk):
                        char.x += char.vel
                        char.direction = CharacterDirection.right

                else:
                    char.set_state(CharacterState.idle)

        char.redraw_screen()
        cat.redraw_screen()
        planet.redraw(char)
        timeb += 1

        game.decor()

        last_r = last + game.is_collided(char, last_r)
        bg = bgs[last_r]
        game.bg = bgs_names[last_r]
        planet.bg = bgs_names[last_r]
        cat.bg = bgs_names[last_r]

        last = last_r

        if bgs_names[last_r] == 'outside_planet2':
            game.right_rect = pygame.Rect(-100000, 315, 20, 350)
        else:
            game.right_rect = pygame.Rect(1100, 315, 20, 350)

        if first_time:
            if numbe == 255:
                win.blit(rectsi, (0, 0))
                # win.blit(textsurface, (150, 200))
                char.quest = False
                char.quest_2 = False
                char.quest_3 = False
                n_text = 0
                music = True
                bgs_names = ['outside_planet1',
                             'outside_planet2']
                all_events = ''
                bgs = [pygame.image.load(ASSET_DIRECTORY + 'outside_planet1.png'),
                       pygame.image.load(ASSET_DIRECTORY + 'outside_planet2.png')]
                last_r = 0
                last = 0
                planet.quest1_showed = False
                planet.quest2_showed = False
                bg = bgs[last_r]
                char.x = 400
            if numbe != 0:
                numbe -= 3
                # textsurface.set_alpha(numbe)
                rectsi.set_alpha(numbe)
                char.set_state(CharacterState.idle)
                win.blit(rectsi, (0, 0))
                # win.blit(textsurface, (150, 200))
            else:
                win.blit(rectsi, (0, 0))
                first_time = False

        elif part_end:
            if numbe != 255:
                numbe += 3
                rectsi.set_alpha(numbe)
                char.set_state(CharacterState.idle)
                win.blit(rectsi, (0, 0))
            else:
                win.blit(rectsi, (0, 0))
                first_time = False
                part_end = False
                end = True
        if end:
            win.blit(rectsi, (0, 0))
            myfont = pygame.font.Font(ASSET_DIRECTORY + 'pixel2.ttf', 50)
            textsurface = myfont.render('С 30 летием тебя!!!', False, (255, 255, 255))
            textsurface.set_alpha(numbe)
            win.blit(textsurface, (150, 200))
        pygame.display.update()


pygame.quit()
