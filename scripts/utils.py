import pygame
from enum import Enum
from typing import List, Dict
from copy import deepcopy
import sys
import os
from typing import Tuple, Optional


def pygame_load_image(start_value: int, count_frames: int, pattern_name: str, size_image: Tuple[int, int],
                      max_number_len: Optional[int] = None ):
    if max_number_len is None:
        max_number_len = len(str(start_value+count_frames))

    return list(map(
        lambda i: pygame.transform.scale(pygame.image.load(
            pattern_name.format(str(i).zfill(max_number_len))), size_image),
        range(start_value, start_value+count_frames)
    ))


class NPCState(Enum):
    idle = 0
    talk = 1


class CharacterState(Enum):
    idle = 0
    walk = 1
    attack = 2
    dead = 3


class CharacterDirection(Enum):
    left = 0
    right = 1


class EnemyState(Enum):
    idle = 0
    dead = 1
    walk = 2
    attack = 3


class MirrorAnimation:
    left: List[pygame.Surface]
    right: List[pygame.Surface]

    def __init__(self, animation: List[pygame.Surface]):
        self.right = animation
        self.left = list(map(lambda i: pygame.transform.flip(i, True, False), animation))


class CounterAnimation:
    def __init__(self, max_frame_cnt, max_animation_cnt, animation_end_function=None, whitelist_reset=None, freeze_on_end=False):
        self._whitelist_reset = whitelist_reset
        self._max_frame_cnt = max_frame_cnt
        self._max_animation_cnt = max_animation_cnt
        self._frame_cnt = 0
        self._animation_cnt = 0
        self._animation_end_function = animation_end_function
        self.freeze_on_end = freeze_on_end

    def access_reset(self, state):
        return self._whitelist_reset is None or state in self._whitelist_reset

    @property
    def animation_cnt(self):
        return self._animation_cnt

    @property
    def frame_cnt(self):
        return self._frame_cnt

    def duplicate(self):
        new = deepcopy(self)
        new._frame_cnt = 0
        new._animation_cnt = 0

        return new

    def tick(self):
        self._frame_cnt += 1
        if self._frame_cnt >= self._max_frame_cnt:
            self._frame_cnt = 0

            if not self.freeze_on_end or self._animation_cnt != self._max_animation_cnt -1 :
                self._animation_cnt += 1

            if self._animation_cnt >= self._max_animation_cnt:
                if self._animation_end_function is None:
                    self._animation_cnt = 0
                else:
                    self._animation_end_function()


class RotateAnimation:
    def __init__(self, eagle, steps):
        self._eagle = eagle
        self.steps = steps
        self.cur_eagle = 0

    @property
    def eagle(self):
        return self._eagle

    def rotate(self):
        self.cur_eagle = self._eagle

    def tick(self):
        self.cur_eagle -= 0.1 + self._eagle / self.steps
        if self.cur_eagle <= 0:
            self.cur_eagle = 0


class Character2:
    animation_by_state: Dict[CharacterState, MirrorAnimation]

    def __init__(self, x, y, screen, ch, back, weight, height, asset_directory):
        self.life = 15
        self.char = pygame.transform.scale(pygame.image.load(asset_directory + ch), (weight, height))
        self.quest = False
        self.quest_2 = False
        self.rotate = RotateAnimation(15.0, 7)
        self.n_text = 0
        self.text = ['С кем на этот раз надо разобраться?',
                     'У кого я могу получить больше информации о нём?',
                     'Помните, мои услуги не дешёвые.']

        self.text_2 = ['Здравствуй Кейр, мне нужно разузнать о демоне.',
                       'Спасибо тебе за помощь.']

        self.animation_by_state = {
            CharacterState.attack: MirrorAnimation(
                pygame_load_image(1, 6,  os.path.join(asset_directory, "biker_attack{}.png"), (weight, height))
            ),
            CharacterState.idle: MirrorAnimation(
                pygame_load_image(1, 4, os.path.join(asset_directory, "biker_idle{}.png"), (weight, height))
            ),
            CharacterState.walk: MirrorAnimation(
               pygame_load_image(1, 6, os.path.join(asset_directory, "biker_run{}.png"), (weight, height))
            ),
            CharacterState.dead: MirrorAnimation(
                pygame_load_image(1, 4, os.path.join(asset_directory, "biker_idle{}.png"), (weight, height))
            ),

        }
        self.animation_screen_state = 0

        self.counter_animation_by_state = {
            # CharacterState.attack: CounterAnimation(
            #     5, 7,
            #     animation_end_function=lambda: self.set_state_force(CharacterState.idle),
            #     whitelist_reset=(CharacterState.attack2,),
            # ),
            # CharacterState.attack2: CounterAnimation(
            #     5, 7,
            #     animation_end_function=lambda: self.set_state_force(CharacterState.idle),
            #     whitelist_reset=(CharacterState.attack3,),
            # ),
            # CharacterState.attack3: CounterAnimation(
            #     5, 7,
            #     animation_end_function=lambda: self.set_state_force(CharacterState.idle),
            #     whitelist_reset=(),
            # ),
            CharacterState.attack: CounterAnimation(4, 6, animation_end_function=lambda: self.set_state_force(CharacterState.idle), whitelist_reset=()),
            CharacterState.idle: CounterAnimation(5, 4),
            CharacterState.walk: CounterAnimation(5, 6),
            CharacterState.dead: CounterAnimation(5, 4, freeze_on_end=True),
        }

        self.mirror_char = pygame.transform.flip(self.char, True, False)
        self.x = x
        self.y = y
        self.char_rect = self.char.get_rect(topleft=(x, y))
        self.win = screen
        self.vel = 6
        self.bg = back

        self.direction = CharacterDirection.left
        self.state = CharacterState.idle
        self.counter_animation = self.counter_animation_by_state[self.state].duplicate()

        self.time = 0.67

    def set_state_force(self, state):
        if self.state != state:
            self.state = state
            self.counter_animation = self.counter_animation_by_state[self.state].duplicate()

    def set_state(self, state):
        if self.counter_animation.access_reset(state):
            self.set_state_force(state)
            return True
        else:
            return False

    def attack(self, enemy):
        if self.char_rect.colliderect(enemy.rect):
            return True
        else:
            return False

    def redraw_screen(self):
        if self.direction == CharacterDirection.left:
            anim = self.animation_by_state[self.state].left[self.counter_animation.animation_cnt]
        else:
            anim = self.animation_by_state[self.state].right[self.counter_animation.animation_cnt]

        # anim = pygame.transform.rotate(anim, self.rotate.cur_eagle)
        self.win.blit(anim, (self.x, self.y))

        self.counter_animation.tick()
        self.rotate.tick()
        self.char_rect = self.char.get_rect(topleft=(self.x, self.y))


class PlanetQuests:
    def __init__(self):
        self.quest1_showed = False
        self.quest2_showed = False
        self.bg = 'planet'
        # text len <= 42
        self.text1 = ['Хм, надо осмотреть местность...',
                      ''
                      ]
        self.text2 = ['Судя по этому... тотему на этой планете есть жизнь,',
                      'надо забраться в воду, пойду переоденусь.',
                      ''
                      ]
        self.text3 = ['Котики?',
                      ''
                      ]
        self.text4 = ['Грёбанные людишки добрались и до этой планеты...',
                      '',
                      '',
                      'Вы правда верите, что земля вам пренадлежала всегда?',
                      'За долго до появления того корабля, жизнь на Земле',
                      'играла совсем другими красками, котики любили и уважали',
                      'Землю, но через 5000 лет к нам пожалавал незванный гость',
                      'Огромная тарелка с надписью, блин, как же её там, А',
                      '"J.E.S.U.S.", она привезла нам не понятных существ',
                      'Но на следующий день она устроила геноцид, нам',
                      'пришлось покинуть родную планету, оставив лишь',
                      'недоразвитую часть нашей расы, но вы...',
                      'ВЫ СОБИРАЕТЕСЬ И ЭТУ ПЛАНЕТУ ЗАБРАТЬ???',
                      'НУ НЕТ, ЕСЛИ НЕ НАМ ТО НИ КОМУ!!!',
                      ''
                      ]
        self.quest1_rect = pygame.Rect(744, 281, 132, 206)
        self.quest2_rect = pygame.Rect(539, 306, 180, 166)
        self.quest3_rect = pygame.Rect(-22, 303, 275, 158)
        self.quest4_rect = pygame.Rect(600, 281, 132, 206)

    def redraw(self, char):
        if self.bg != 'outside_planet1' and self.bg != 'outside_planet2':
            if self.quest1_rect.colliderect(char.char_rect) and not self.quest1_showed:
                char.quest = True
            elif self.quest2_rect.colliderect(char.char_rect) and not self.quest2_showed and self.bg == 'planet2':
                char.quest_2 = True
            elif self.quest3_rect.colliderect(char.char_rect) and self.quest2_showed and self.bg == 'planet':
                char.quest_3 = True
        else:
            if self.quest4_rect.colliderect(char.char_rect) and not self.quest1_showed:
                char.quest = True
            elif self.quest4_rect.colliderect(char.char_rect) and not self.quest2_showed and self.bg == 'outside_planet2':
                char.quest_2 = True


class UnderWater:
    def __init__(self):
        self.quest1_showed = False
        self.quest2_showed = False
        self.bg = 'underwater1'
        # text len <= 42
        self.text1 = ['Хм, надо осмотреть местность...',
                      ''
                      ]
        self.text2 = ['Скорее всего я смогу открыть проход с помощью',
                      'пианино со странной бумагой',
                      '(чтобы использовать пианино нажми q)'
                      ]
        self.quest1_rect = pygame.Rect(582, 256, 50, 39)
        self.quest2_rect = pygame.Rect(539, 306, 180, 166)
        self.quest3_rect = pygame.Rect(-22, 303, 275, 158)

    def redraw(self, char):
        if self.quest1_rect.colliderect(char.rect) and not self.quest1_showed:
            char.quest = True
            print('hooh')
        elif self.quest2_rect.colliderect(char.rect) and not self.quest2_showed and self.bg == 'planet2':
            char.quest_2 = True
        elif self.quest3_rect.colliderect(char.rect) and self.quest2_showed and self.bg == 'planet':
           char.quest_3 = True


class SwimmingCharacter:
    def __init__(self, x, y, screen, asset_directory):
        self.weight = 160
        self.height = 160
        self.quest = False
        self.quest2 = False
        self.rotate = RotateAnimation(15.0, 7)
        self.direction = CharacterDirection.right
        self.swimmingcharacter_sprite = pygame.transform.scale(pygame.image.load(asset_directory + 'buzz_swimming1.png'),
                                                    (self.weight, self.height))
        self.rect = self.swimmingcharacter_sprite.get_rect(topleft=(x, y))
        self.win = screen
        self.vel = 3
        self.x = x
        self.y = y
        self.bg = None
        self.state = CharacterState.idle

        self.animation_by_state = {CharacterState.idle: MirrorAnimation(pygame_load_image
                                                                  (1, 6,
                                                                   os.path.join(asset_directory, "buzz_swimmingidle{}.png"),
                                                                   (self.weight, self.height))),
                                   CharacterState.walk: MirrorAnimation(pygame_load_image
                                                                  (1, 8,
                                                                   os.path.join(asset_directory, "buzz_swimming{}.png"),
                                                                   (self.weight, self.height)))
                                   }
        self.counter_animation_by_state = {
            CharacterState.idle: CounterAnimation(6, 6),
            CharacterState.walk: CounterAnimation(6, 8),
        }

        self.counter_animation = self.counter_animation_by_state[self.state].duplicate()

    def redraw_screen(self):
        if self.direction == CharacterDirection.left:
            anim = self.animation_by_state[self.state].left[self.counter_animation.animation_cnt]
        else:
            anim = self.animation_by_state[self.state].right[self.counter_animation.animation_cnt]

        # anim = pygame.transform.rotate(anim, self.rotate.cur_eagle)
        self.win.blit(anim, (self.x, self.y))

        self.counter_animation.tick()
        self.rotate.tick()
        self.rect = self.swimmingcharacter_sprite.get_rect(topleft=(self.x, self.y))

    def set_state_force(self, state):
        if self.state != state:
            self.state = state
            self.counter_animation = self.counter_animation_by_state[self.state].duplicate()

    def set_state(self, state):
        if self.counter_animation.access_reset(state):
            self.set_state_force(state)
            return True
        else:
            return False


class Character:
    animation_by_state: Dict[CharacterState, MirrorAnimation]

    def __init__(self, x, y, screen, ch, back, weight, height, asset_directory):
        self.life = 15
        self.char = pygame.transform.scale(pygame.image.load(asset_directory + ch), (weight, height))
        self.quest = False
        self.quest_2 = False
        self.quest_3 = False
        self.rotate = RotateAnimation(15.0, 7)
        self.n_text = 0
        self.weight = weight
        self.text = [
                     'Разве моя смерть в одиночестве сравнится с',
                     'будущем людей. Думаю ответ очевиден. И да,',
                     'зови меня просто Баззом на корабле'
                     ''
                    ]

        self.text_2 = ['???',
                       '',
                       '',
                       'Хех, ну и как же это что-то связано',
                       'с моей службой стране?',
                       '',
                       'Cпасибо, Шейла, хоть и врядли',
                       'оно пригодится',
                       '', 'А если ты тут, кто управляет кораблём?', '', '']

        self.animation_by_state = {
            CharacterState.attack: MirrorAnimation(
                pygame_load_image(1, 6,  os.path.join(asset_directory, "buzz_attack{}.png"), (weight, height))
            ),
            CharacterState.idle: MirrorAnimation(
                pygame_load_image(1, 4, os.path.join(asset_directory, "buzz_idle{}.png"), (weight, height))
            ),
            CharacterState.walk: MirrorAnimation(
               pygame_load_image(1, 6, os.path.join(asset_directory, "buzz_run{}.png"), (weight, height))
            ),
            CharacterState.dead: MirrorAnimation(
                pygame_load_image(1, 4, os.path.join(asset_directory, "buzz_idle{}.png"), (weight, height))
            ),

        }
        self.animation_screen_state = 0

        self.counter_animation_by_state = {
            # CharacterState.attack: CounterAnimation(
            #     5, 7,
            #     animation_end_function=lambda: self.set_state_force(CharacterState.idle),
            #     whitelist_reset=(CharacterState.attack2,),
            # ),
            # CharacterState.attack2: CounterAnimation(
            #     5, 7,
            #     animation_end_function=lambda: self.set_state_force(CharacterState.idle),
            #     whitelist_reset=(CharacterState.attack3,),
            # ),
            # CharacterState.attack3: CounterAnimation(
            #     5, 7,
            #     animation_end_function=lambda: self.set_state_force(CharacterState.idle),
            #     whitelist_reset=(),
            # ),
            CharacterState.attack: CounterAnimation(4, 6, animation_end_function=lambda: self.set_state_force(CharacterState.idle), whitelist_reset=()),
            CharacterState.idle: CounterAnimation(5, 4),
            CharacterState.walk: CounterAnimation(5, 6),
            CharacterState.dead: CounterAnimation(5, 4, freeze_on_end=True),
        }

        self.mirror_char = pygame.transform.flip(self.char, True, False)
        self.x = x
        self.y = y
        self.char_rect = self.char.get_rect(topleft=(x, y))
        self.win = screen
        self.vel = 6
        self.bg = back

        self.direction = CharacterDirection.left
        self.state = CharacterState.idle
        self.counter_animation = self.counter_animation_by_state[self.state].duplicate()

        self.time = 0.67

    def set_state_force(self, state):
        if self.state != state:
            self.state = state
            self.counter_animation = self.counter_animation_by_state[self.state].duplicate()

    def set_state(self, state):
        if self.counter_animation.access_reset(state):
            self.set_state_force(state)
            return True
        else:
            return False

    def attack(self, enemy):
        if self.char_rect.colliderect(enemy.rect):
            return True
        else:
            return False

    def redraw_screen(self):
        if self.direction == CharacterDirection.left:
            anim = self.animation_by_state[self.state].left[self.counter_animation.animation_cnt]
        else:
            anim = self.animation_by_state[self.state].right[self.counter_animation.animation_cnt]

        # anim = pygame.transform.rotate(anim, self.rotate.cur_eagle)
        self.win.blit(anim, (self.x, self.y))

        self.counter_animation.tick()
        self.rotate.tick()
        self.char_rect = self.char.get_rect(topleft=(self.x, self.y))


class RandomNPC:
    def __init__(self, x, y, screen, weight, height, npc, asset_directory, n, lr, default):
        self.win = screen
        self.x = x
        self.y = y
        self.bg = None
        self.default = default
        self.lr = lr

        self.animation_by_state = MirrorAnimation(pygame_load_image
                                                  (1, n, os.path.join(asset_directory, "%s{}.png" % npc),
                                                   (weight, height))),
        self.counter_animation_by_state = CounterAnimation(7, n)

        self.counter_animation = self.counter_animation_by_state.duplicate()

    def redraw_screen(self):
        if self.default == self.bg:
            if self.lr == 'r':
                anim = self.animation_by_state[0].right[self.counter_animation.animation_cnt]
            else:
                anim = self.animation_by_state[0].left[self.counter_animation.animation_cnt]
            self.win.blit(anim, (self.x, self.y))

            self.counter_animation.tick()


class Professor:
    def __init__(self, x, y, screen, weight, height, asset_directory):
        self.professor_sprite = pygame.transform.scale(pygame.image.load(asset_directory + 'professor_idle1.png'),
                                                  (weight, height))
        self.rect = self.professor_sprite.get_rect(topleft=(x, y))
        self.win = screen
        self.x = x
        self.y = y
        self.bg = None
        self.state = NPCState.idle
        self.default = 'lab'
        self.showed = False
        self.n_text = 0
        self.text = ['Коллеги, здесь и прямо сейчас происходит история,',
                     'это новый шаг человечества к его процветанию.',
                     'Отдавая свои жизни вы даёте возможность будущему',
                     'поколению наслаждаться бейсболом, радоваться просмотру',
                     'комедии, обретать любовь. Не дайте погаснуть миру',
                     'человека, как земному.',
                     'От лица 8 милллиардов людей говорю вам "Спасибо".',
                     'Отправка через 10 минут, просьба быть готовым ', 'к этому времени.',
                     '']

        self.animation_by_state = {NPCState.idle: MirrorAnimation(pygame_load_image
                                                  (1, 4, os.path.join(asset_directory, "professor_idle{}.png"),
                                                   (weight, height))),
                                   NPCState.talk: MirrorAnimation(pygame_load_image
                                                  (1, 6, os.path.join(asset_directory, "professor_talk{}.png"),
                                                   (weight, height)))}
        self.counter_animation_by_state = {
            NPCState.idle: CounterAnimation(6, 4),
            NPCState.talk: CounterAnimation(5, 6),
        }

        self.counter_animation = self.counter_animation_by_state[self.state].duplicate()

    def redraw_screen(self):
        if self.default == self.bg:
            self.rect = self.professor_sprite.get_rect(topleft=(self.x, self.y))
            anim = self.animation_by_state[self.state].left[self.counter_animation.animation_cnt]
            self.win.blit(anim, (self.x, self.y))

            self.counter_animation.tick()
        else:
            self.rect = self.professor_sprite.get_rect(topleft=(-1000, -1000))

    def set_state_force(self, state):
        if self.state != state:
            self.state = state
            self.counter_animation = self.counter_animation_by_state[self.state].duplicate()

    def set_state(self, state):
        if self.counter_animation.access_reset(state):
            self.set_state_force(state)
            return True
        else:
            return False


class Mann:
    def __init__(self, x, y, screen, weight, height, asset_directory):
        self.mann_sprite = pygame.transform.scale(pygame.image.load(asset_directory + 'man1_idle1.png'),
                                                  (weight, height))
        self.rect = self.mann_sprite.get_rect(topleft=(x, y))
        self.win = screen
        self.x = x
        self.y = y
        self.bg = None
        self.state = NPCState.idle
        self.default = 'locker_room'
        self.showed = False
        self.n_text = 0
        self.text = [
                     'Ну что, доктор Вольф Эдмундс, мы владеем судьбой',
                     'человечества, не страшно ли будет остаться одному,',
                     'если планета не будет пригодна для жизни?', '', '', '']

        self.animation_by_state = {NPCState.idle: MirrorAnimation(pygame_load_image
                                                  (1, 6, os.path.join(asset_directory, "man1_idle{}.png"),
                                                   (weight, height))),
                                   NPCState.talk: MirrorAnimation(pygame_load_image
                                                  (1, 6, os.path.join(asset_directory, "man1_talk{}.png"),
                                                   (weight, height)))}
        self.counter_animation_by_state = {
            NPCState.idle: CounterAnimation(6, 6),
            NPCState.talk: CounterAnimation(5, 6),
        }

        self.counter_animation = self.counter_animation_by_state[self.state].duplicate()

    def redraw_screen(self):
        if self.default == self.bg:
            self.rect = self.mann_sprite.get_rect(topleft=(self.x, self.y))
            anim = self.animation_by_state[self.state].left[self.counter_animation.animation_cnt]
            self.win.blit(anim, (self.x, self.y))

            self.counter_animation.tick()
        else:
            self.rect = self.mann_sprite.get_rect(topleft=(-1000, -1000))

    def set_state_force(self, state):
        if self.state != state:
            self.state = state
            self.counter_animation = self.counter_animation_by_state[self.state].duplicate()

    def set_state(self, state):
        if self.counter_animation.access_reset(state):
            self.set_state_force(state)
            return True
        else:
            return False


class Brend:
    def __init__(self, x, y, screen, weight, height, asset_directory):
        self.brend_sprite = pygame.transform.scale(pygame.image.load(asset_directory + 'man1_idle1.png'),
                                                  (weight, height))
        self.rect = self.brend_sprite.get_rect(topleft=(x, y))
        self.win = screen
        self.x = x
        self.y = y
        self.bg = None
        self.state = NPCState.idle
        self.default = 'lab'
        self.showed = False
        self.n_text = 0
        self.text = [
                     'Буду ждать твоего рапорта о планете) Мне ',
                     'хотелось столько провести времени с тобой, мне будет',
                     'тебя не хватать, люблю тебя, надеюсь свидимся.', '', '', '']

        self.animation_by_state = {NPCState.idle: MirrorAnimation(pygame_load_image
                                                  (1, 4, os.path.join(asset_directory, "brend_idle{}.png"),
                                                   (weight, height))),
                                   NPCState.talk: MirrorAnimation(pygame_load_image
                                                  (1, 6, os.path.join(asset_directory, "brend_talk{}.png"),
                                                   (weight, height)))}
        self.counter_animation_by_state = {
            NPCState.idle: CounterAnimation(6, 4),
            NPCState.talk: CounterAnimation(5, 6),
        }

        self.counter_animation = self.counter_animation_by_state[self.state].duplicate()

    def redraw_screen(self):
        if self.default == self.bg:
            self.rect = self.brend_sprite.get_rect(topleft=(self.x, self.y))
            anim = self.animation_by_state[self.state].left[self.counter_animation.animation_cnt]
            self.win.blit(anim, (self.x, self.y))

            self.counter_animation.tick()
        else:
            self.rect = self.brend_sprite.get_rect(topleft=(-1000, -1000))

    def set_state_force(self, state):
        if self.state != state:
            self.state = state
            self.counter_animation = self.counter_animation_by_state[self.state].duplicate()

    def set_state(self, state):
        if self.counter_animation.access_reset(state):
            self.set_state_force(state)
            return True
        else:
            return False


class Bullet:
    def __init__(self, x, y, screen, asset_directory, lr):
        self.x = x
        self.y = y
        self.win = screen
        self.weight = 70
        self.delete = False
        self.lr = lr
        self.height = 70
        self.time = 0
        self.bullet_sprite = pygame.transform.scale(pygame.image.load(asset_directory + 'bullet01.png'),
                                                    (80, 80))
        self.rect = self.bullet_sprite.get_rect(topleft=(x, y))

        self.animation_by_state = MirrorAnimation(pygame_load_image(1, 30, os.path.join(asset_directory, "bullet{}.png"),
                                                                    (self.weight, self.height), max_number_len=2))
        self.counter_animation_by_state = CounterAnimation(2, 30)
        self.counter_animation = self.counter_animation_by_state.duplicate()

    def redraw_screen(self):
        self.time += 1
        if self.time > 16:
            if self.x < -100 or self.x > 1112:
                self.delete = True
            elif self.lr == CharacterDirection.left:
                self.x -= 8
                self.rect = self.bullet_sprite.get_rect(topleft=(self.x, self.y))
                anim = self.animation_by_state.left[self.counter_animation.animation_cnt]
                self.win.blit(anim, (self.x, self.y))

                self.counter_animation.tick()
            else:
                self.x += 8
                self.rect = self.bullet_sprite.get_rect(topleft=(self.x + 80, self.y))
                anim = self.animation_by_state.right[self.counter_animation.animation_cnt]
                self.win.blit(anim, (self.x + 80, self.y))

                self.counter_animation.tick()


class Sheila:
    def __init__(self, x, y, screen, weight, height, asset_directory):
        self.sheila_sprite = pygame.transform.scale(pygame.image.load(asset_directory + 'man1_idle1.png'),
                                                    (weight, height))
        self.rect = self.sheila_sprite.get_rect(topleft=(x, y))
        self.win = screen
        self.x = x
        self.y = y
        self.bg = None
        self.state = NPCState.idle
        self.alph = 255
        self.default = 'ship'
        self.showed = False
        self.showed2 = False
        self.n_text = 0
        self.text = [
                     'Пссс, Вольф, то есть Базз, пойдём со мной', '', '',
                     'Так, тут нас не услышат, я тебе хочу ',
                     'кое-что показать и...', '',
                     'Да никто другой не поймёт меня, ты же служил?',
                     'так сейчас... ВОТ! я проснулась на 3 недели',
                     'раньше вас и соорудила его.',
                     'Не что, а кто, его зовут Саймон, он сделан',
                     'из микроволновки и УФ лампы.',
                     'Опробуй его на этих коробках.',
                     'Служу Америке!!!',
                     '',
                     '',
                     'Ой...', '', '', '', '', '']

        self.animation_by_state = {NPCState.idle: MirrorAnimation(pygame_load_image
                                                  (1, 4, os.path.join(asset_directory, "sheila{}.png"),
                                                   (weight, height))),
                                   }
        self.counter_animation_by_state = {
            NPCState.idle: CounterAnimation(6, 4)
        }

        self.counter_animation = self.counter_animation_by_state[self.state].duplicate()

    def redraw_screen(self):
        if self.default == self.bg:
            self.rect = self.sheila_sprite.get_rect(topleft=(self.x, self.y))
            anim = self.animation_by_state[self.state].right[self.counter_animation.animation_cnt]
            anim.set_alpha(self.alph)
            self.win.blit(anim, (self.x, self.y))

            self.counter_animation.tick()
        else:
            self.rect = self.sheila_sprite.get_rect(topleft=(-1000, -1000))

    def set_state_force(self, state):
        if self.state != state:
            self.state = state
            self.counter_animation = self.counter_animation_by_state[self.state].duplicate()

    def set_state(self, state):
        if self.counter_animation.access_reset(state):
            self.set_state_force(state)
            return True
        else:
            return False


class BigStarship:
    def __init__(self, x, y, screen, asset_directory):
        self.weight = 329
        self.height = 160
        self.bigstarship_sprite = pygame.transform.scale(pygame.image.load(asset_directory + 'big_starship1.png'),
                                                    (self.weight, self.height))
        self.rect1 = pygame.Rect(x + 131, y + 27, 185, 116)
        self.rect2 = pygame.Rect(x + 57, y + 14, 106, 76)
        self.rect3 = pygame.Rect(x + 5, y + 24, 63, 47)
        self.win = screen
        self.vel = 7
        self.x = x
        self.y = y
        self.bg = None
        self.state = CharacterState.idle

        self.animation_by_state = {CharacterState.idle: MirrorAnimation(pygame_load_image
                                                                  (1, 3,
                                                                   os.path.join(asset_directory, "big_starship{}.png"),
                                                                   (self.weight, self.height))),
                                   }
        self.counter_animation_by_state = {
            CharacterState.idle: CounterAnimation(3, 3)
        }

        self.counter_animation = self.counter_animation_by_state[self.state].duplicate()

    def redraw_screen(self):
        self.rect1 = pygame.Rect(self.x + 131, self.y + 27, 165, 116)
        self.rect2 = pygame.Rect(self.x + 57, self.y + 14, 106, 76)
        self.rect3 = pygame.Rect(self.x + 5, self.y + 34, 63, 37)
        # pygame.draw.rect(self.win, 'red', self.rect1)
        # pygame.draw.rect(self.win, 'red', self.rect2)
        # pygame.draw.rect(self.win, 'red', self.rect3)
        # pygame.draw.rect(self.win, 'red', self.rect1)
        # pygame.draw.rect(self.win, 'yellow', self.rect2)
        # pygame.draw.rect(self.win, 'blue', self.rect3)
        anim = self.animation_by_state[self.state].right[self.counter_animation.animation_cnt]
        self.win.blit(anim, (self.x, self.y))

        self.counter_animation.tick()

    def set_state_force(self, state):
        if self.state != state:
            self.state = state
            self.counter_animation = self.counter_animation_by_state[self.state].duplicate()

    def set_state(self, state):
        if self.counter_animation.access_reset(state):
            self.set_state_force(state)
            return True
        else:
            return False
