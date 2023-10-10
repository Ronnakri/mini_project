import pygame 
import os
import random 

from os.path import isfile, join
from pygame.sprite import Group
from pygame import mixer

SCREEN_WIDTH, SCREEN_HEIGHT = 1100,600
BOTTOM_PANEL = 140
CHARACTER_POSTION_X, CHARACTER_POSTION_Y = (SCREEN_WIDTH / 4), 500

#COLOR
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (254, 0, 0)
GREEN = (1, 106, 112)
BLUE = (31, 65, 114)
PURPLE = (91, 8, 136)

#PATH FILE
ASSET_PATH = os.path.join(os.path.dirname(__file__), "assets")
CARD_PATH = os.path.join(ASSET_PATH, "cards")
BUTTON_PATH = os.path.join(ASSET_PATH, "button")
BG_PATH = os.path.join(ASSET_PATH, "background")
PANEL_PATH = os.path.join(ASSET_PATH, "tiles")
CHARACTER_PATH = os.path.join(ASSET_PATH, "sprite")
HEALTH_BAR_PATH = os.path.join(ASSET_PATH,"GUI", "health_bar")
GUI_PATH = os.path.join(ASSET_PATH, "GUI")
MUSIC_PATH = os.path.join(ASSET_PATH, "music")

pygame.init()
pygame.font.init()

FONT1 = pygame.font.SysFont('Futile Pro', 18)
FONT2 = pygame.font.SysFont('MinimalPixel2', 32)
FONT3 = pygame.font.SysFont('ThaleahFat', 60)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

FPS = 60

pygame.display.set_caption("GAMESUDInw")

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    SCREEN.blit(img, (x, y))

bg_image = pygame.image.load(os.path.join(BG_PATH, "3", "6.png")).convert_alpha()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH,SCREEN_HEIGHT - 30))

def draw_bg():
    SCREEN.blit(bg_image, (0, 0))
    img_cf = pygame.image.load(os.path.join(GUI_PATH, "character_frame1.png")).convert_alpha()
    img_cf2 = pygame.transform.flip(pygame.image.load(os.path.join(GUI_PATH, "character_frame2.png")), True, False).convert_alpha()
    SCREEN.blit(img_cf, (20 , 30))
    SCREEN.blit(img_cf2, (820, 30))


mixer.music.load(os.path.join(MUSIC_PATH,"bg12.mp3"))
mixer.music.play(-1)
mixer.music.set_volume(0.5)

panel_image = pygame.image.load(os.path.join(PANEL_PATH, "0.png")).convert_alpha()
panel_image = pygame.transform.scale(panel_image, ( SCREEN_WIDTH - 20 , 120))

def draw_panel():
    SCREEN.blit(panel_image, (10, SCREEN_HEIGHT - BOTTOM_PANEL - 20))

victory_image = pygame.image.load(os.path.join(GUI_PATH, "victory.png")).convert_alpha()
defeated_image = pygame.image.load(os.path.join(GUI_PATH, "defeated.png")).convert_alpha()

class Fighter1():
    def __init__(self, x, y, name, max_hp, strenght, max_stamina, resistance):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.stamina = max_stamina
        self.max_stamina = max_stamina
        self.strenght = strenght
        self.resistance = resistance
        self.original_resist = resistance
        self.alive = True
        self.animation_list = []
        self.action = 0 # 0:idle 1:run 2:attack 3:hit 4:death 
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.x = x
        self.y = y
        self.fall_count = 0
        
        #load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(os.path.join(CHARACTER_PATH,f"{self.name}","idle",f"{i}.png")).convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        
        #load run images 
        temp_list = []
        for i in range(5):
            img = pygame.image.load(os.path.join(CHARACTER_PATH,f"{self.name}","run",f"{i}.png")).convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #load attack images
        temp_list = []
        for i in range(5):
            img = pygame.image.load(os.path.join(CHARACTER_PATH,f"{self.name}","attack",f"{i}.png")).convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #load hurt images
        temp_list = []
        for i in range(2):
            img = pygame.image.load(os.path.join(CHARACTER_PATH,f"{self.name}","hurt",f"{i}.png")).convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #load death images
        temp_list = []
        for i in range(5):
            img = pygame.image.load(os.path.join(CHARACTER_PATH,f"{self.name}","death",f"{i}.png")).convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_character(self):
        animation_cooldown = 150
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()
    
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def perform_action(self, target, action_type, action_value, damage_color):
        rand = random.randint(0, 10)
        damage = rand + action_value - target.resistance
        if damage < 0:
            damage = 0
        target.hp -= damage
        target.hurt()
        target.resistance = target.original_resist
        if target.hp < 1:
            target.hp = 0
            target.alive = False    
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.centery, str(damage), damage_color)
        damage_text_group.add(damage_text)
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def attack(self, target, damage_value):
        self.perform_action(target, "attack", damage_value, RED)

    def potion(self, heal_value, heal_color):
        if self.hp > 0:
            if self.max_hp - self.hp > heal_value:
                heal_amount = heal_value
            else:
                heal_amount = self.max_hp - self.hp
        self.hp += heal_amount
        heal_text = DamageText(self.rect.centerx, self.rect.centery, str(heal_amount), heal_color)
        damage_text_group.add(heal_text)
    
    def defence(self, defense_value, defense_color):
        self.resistance += defense_value
        damage_text = DamageText(self.rect.centerx, self.rect.centery, str(defense_value), defense_color)
        damage_text_group.add(damage_text)
        self.update_time = pygame.time.get_ticks()

    def attack1(self, target):
        self.attack(target, random.randint(5, 15))

    def attack2(self, target):
        self.attack(target, random.randint(10, 20))

    def attack3(self, target):
        self.attack(target, random.randint(20, 30))

    def attack4(self, target):
        self.attack(target, random.randint(40, 50))

    def attack5(self, target):
        damage = int(0.65 * target.hp)
        self.hp = self.hp * 0.35
        target.hp -= damage 
        target.hurt()
        target.resistance = target.original_resist
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), RED)
        damage_text_group.add(damage_text)
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def potion1(self):
        self.potion(25, GREEN)

    def potion2(self):
        self.potion(5, GREEN)

    def potion3(self):
        self.potion(100, GREEN)

    def potion4(self):
        self.potion(50, GREEN)

    def defence1(self):
        self.defence(5, BLUE)

    def defence2(self):
        self.defence(10, BLUE)

    def defence3(self):
        self.defence(15, BLUE)

    def defence4(self):
        self.defence(20, BLUE)

    def defence5(self):
        self.defence(25, BLUE)
    
    def special1(self, target):
        damage = target.hp // 2
        self.hp = self.hp // 2
        target.hp -= damage
        target.hurt()
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), PURPLE)
        damage_text_group.add(damage_text)
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def special2(luckyguy):
        luckyguys = [FINN, HOBBIT]
        luckyguy = random.choice(luckyguys)
        damage = luckyguy.max_hp
        luckyguy.hp -= damage
        luckyguy.hurt()
        luckyguy.alive = False
        luckyguy.death()
        damage_text = DamageText(luckyguy.rect.centerx, luckyguy.rect.y, str(damage), PURPLE)
        damage_text_group.add(damage_text)
        luckyguy.frame_index = 0
        luckyguy.update_time = pygame.time.get_ticks()
    
    def special3(self):
        self.resistance += 9998
        damage_text = DamageText(self.rect.centerx, self.rect.y, str(self.resistance), PURPLE)
        damage_text_group.add(damage_text)
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def death(self):
        self.action = 4
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        self.hp = self.max_hp
        self.stamina = self.max_stamina
        self.resistance = self.resistance
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def draw_character(self):
        SCREEN.blit(self.image, self.rect)
    
class Fighter2():
    def __init__(self, x, y, name, max_hp, strength, max_stamina, resistance):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.stamina = max_stamina
        self.max_stamina = max_stamina
        self.resistance = resistance
        self.original_resist = resistance
        self.alive = True
        self.animation_list = []
        self.action = 0 # 0:idle 1:run 2:attack 3:hit 4:death  
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.x = x
        self.y = y
        self.fall_count = 0
        
        #load idle images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(os.path.join(CHARACTER_PATH,f"{self.name}","idle",f"{i}.png")).convert_alpha()
            img = pygame.transform.flip(pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3)), True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        
        #load run images 
        temp_list= []
        for i in range(10):
            img = pygame.image.load(os.path.join(CHARACTER_PATH,f"{self.name}","run",f"{i}.png")).convert_alpha()
            img = pygame.transform.flip(pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3)), True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #load attack images
        temp_list= []
        for i in range(16):
            img = pygame.image.load(os.path.join(CHARACTER_PATH,f"{self.name}","attack",f"{i}.png")).convert_alpha()
            img = pygame.transform.flip(pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3)), True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #load hurt images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(os.path.join(CHARACTER_PATH,f"{self.name}","hurt",f"{i}.png")).convert_alpha()
            img = pygame.transform.flip(pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3)), True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #load death images
        temp_list = []
        for i in range(12):
            img = pygame.image.load(os.path.join(CHARACTER_PATH,f"{self.name}","death",f"{i}.png")).convert_alpha()
            img = pygame.transform.flip(pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3)), True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update_character(self):
        animation_cooldown = 125
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()
    
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        rand = random.randint(20, 60)
        damage = rand - target.resistance
        if damage < 0:
            damage = 0
        target.hp -= damage
        target.resistance = target.original_resist
        target.hurt()
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), RED)
        damage_text_group.add(damage_text)
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def potion(self):
        self.have_potion = 3
        if self.hp // self.max_hp < 0.5 and self.have_potion > 0:
            if self.max_hp - self.hp > 100:
                heal_amount = 100
            else:
                heal_amount = self.max_hp - self.hp
            self.hp += heal_amount
            self.have_potion -= 1
            heal_text = DamageText(self.rect.centerx, self.rect.centery, str(heal_amount), GREEN)
            damage_text_group.add(heal_text)

    def defence(self):
        rand = random.randint(0, 25)
        self.resistance += rand
        damage_text = DamageText(self.rect.centerx, self.rect.centery, str(rand), BLUE)
        damage_text_group.add(damage_text)
        self.update_time = pygame.time.get_ticks()

    def special(self, target):
        damage = int(0.65 * target.hp)
        self.hp = self.hp * 0.7
        target.hp -= damage
        target.hurt()
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), RED)
        damage_text_group.add(damage_text)
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def hurt(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 4
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        self.hp = self.max_hp
        self.stamina = self.max_stamina
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
    
    def draw_character(self):
        SCREEN.blit(self.image, self.rect)

class HealthBar():
    def __init__(self, x, y, hp, max_hp, stamina, max_stamina):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        self.stamina = stamina
        self.max_stamina = max_stamina
        img_border_h = pygame.image.load(os.path.join(HEALTH_BAR_PATH,"border2.png")).convert_alpha()
        img_border_h = pygame.transform.scale(img_border_h, (img_border_h.get_width() * 5, img_border_h.get_height() * 5))
        img_border_s = pygame.image.load(os.path.join(HEALTH_BAR_PATH,"border3.png")).convert_alpha()
        img_border_s = pygame.transform.scale(img_border_s, (img_border_s.get_width() * 2, img_border_s.get_height() * 2))
        img_health = pygame.image.load(os.path.join(HEALTH_BAR_PATH, "red.png")).convert_alpha()
        img_health = pygame.transform.scale(img_health, (img_health.get_width() * 5, img_health.get_height() * 5))
        img_stamina = pygame.image.load(os.path.join(HEALTH_BAR_PATH, "orange.png")).convert_alpha()
        img_stamina = pygame.transform.scale(img_stamina, (img_stamina.get_width() * 2, img_stamina.get_height() * 2))
        self.img_border_health = img_border_h
        self.img_health = img_health
        self.img_border_stamina = img_border_s
        self.img_stamina = img_stamina
        self.rect = self.img_health.get_rect()
    
    def draw(self, hp, stamina):
        self.hp = hp
        self.stamina = stamina
        ratio_health = self.hp / self.max_hp
        ratio_stamina = self.stamina / self.max_stamina
        health_bar = int(self.img_health.get_width() * ratio_health)
        stamina_bar = int(self.img_stamina.get_width() * ratio_stamina)
        SCREEN.blit(self.img_border_health, (self.x + 80, self.y + 15))
        SCREEN.blit(self.img_border_stamina, (self.x + 75, self.y + 55))
        SCREEN.blit(self.img_health, (self.x + 80, self.y + 25), (0, 0, health_bar, self.img_health.get_height()))
        SCREEN.blit(self.img_stamina, (self.x + 80, self.y + 60), (0, 0, stamina_bar, self.img_stamina.get_height()))
        
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = FONT3.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        rand_y = random.randint(0, 5)
        rand_x = random.randint(0, 5)
        self.rect.y -= rand_y
        self.rect.x -= rand_x
        self.counter += 1
        if self.counter > 45:
            self.kill()

damage_text_group = pygame.sprite.Group()

class Card():
    def __init__(self, x, y, card_index):
        self.x_original = x
        self.y_original = y
        self.mouse_over = False
        self.raised = False
        self.pressed = False
        self.card_index = card_index
        self.image_list = []  
        for i in range(17):
            img = pygame.image.load(os.path.join(CARD_PATH, f"{i}.png")).convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() // 5, img.get_height() // 5))
            self.image_list.append(img)
        self.image = self.image_list[card_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def draw_card(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.rect.y = self.y_original - 50
            self.raised = True
            if self.raised == True:
                if pygame.mouse.get_pressed()[0]:
                    self.pressed = True
            else:
                if self.pressed == True:
                    self.pressed = False
        else:
            self.rect.y = self.y_original
            self.raised = False
        SCREEN.blit(self.image, self.rect) 

class Button:
    def __init__(self, x, y):
        self.pressed = False
        self.x = x
        self.y = y
        self.image_list = []
        self.image_index = 0
        for i in range(2):
            self.image = pygame.image.load(os.path.join(BUTTON_PATH, f"retry{i+1}.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
            self.image_list.append(self.image)
        self.image = self.image_list[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self):
        SCREEN.blit(self.image, (self.x, self.y))
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image_index = 1
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    FINN.reset()
                    HOBBIT.reset()
                    self.pressed = False
        else:
            self.image_index = 0
        self.image = self.image_list[self.image_index]

button1 = Button(SCREEN_WIDTH // 2 - 15, 270)

#character define
FINN = Fighter1(CHARACTER_POSTION_X, CHARACTER_POSTION_Y, 'finn', 1, 10, 10, 2)
HOBBIT = Fighter2(CHARACTER_POSTION_X * 3, CHARACTER_POSTION_Y, 'hobbit', 50, 10, 20, 5)

FINN_health_bar = HealthBar(20, 30, FINN.hp, FINN.max_hp, FINN.stamina, FINN.max_stamina)
HOBBIT_health_bar = HealthBar(820, 30, HOBBIT.hp, HOBBIT.max_hp, HOBBIT.stamina, HOBBIT.max_stamina)


def random_card():
    card_prob = [
        (0, 80), # sword 1 
        (1, 30), # sword 2
        (2, 20), # sword 3
        (3, 10), # sword 4
        (4, 2), # sword 5
        (5, 50), # potion 1
        (6, 20), # potion 2
        (7, 10), # potion 3
        (8, 20), # potion 4
        (9, 80), # shield 1
        (10, 80), # shield 2 
        (11, 30), # shield 3
        (12, 20), # shield 4
        (13, 10), # shield 5
        (14, 2), # special 1
        (15, 2), # special 2
        (16, 2), # special 3
    ]
    selected_cards = []
    for _ in range(3):
        total_weight = sum(prob for _, prob in card_prob)
        random_value = random.randint(0, total_weight - 1)
        cumulative_weight = 0
        selected_card = None
        for card_index, weight in card_prob:
            cumulative_weight += weight
            if random_value < cumulative_weight:
                selected_card = card_index
                break
    
        selected_cards.append(selected_card)
    return selected_cards
                    
current_turn = 1 # 1 is player, 2 is enemy
total_fighters = 2
action_cooldown, turn_cooldown = 0, 0
turn_wait_time = 100
action_wait = 50
attack = False
clicked = False
player_cards_randomized = False
game_over = 0 # 1 is player win, -1 is enemy win

def draw_window():
    
    HOBBIT.update_character()
    HOBBIT.draw_character()
    FINN.update_character()
    FINN.draw_character()
       
    pygame.display.update()

def main():

    clicked = False
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                clicked = False 
        
        draw_window()
        draw_bg()
        draw_panel()
        FINN_health_bar.draw(FINN.hp, FINN.stamina)
        HOBBIT_health_bar.draw(HOBBIT.hp, HOBBIT.stamina)
        damage_text_group.update()
        damage_text_group.draw(SCREEN)
        
        global game_over
        if game_over == 0:
            if FINN.alive:
                global current_turn, turn_cooldown, action_cooldown, player_cards_randomized
                if current_turn == 1:
                    turn_cooldown += 1
                    if turn_cooldown >= turn_wait_time:
                        if player_cards_randomized == False:
                            card_indices = random_card()
                            card_list = [Card(SCREEN_WIDTH / 2 - 150 + i * 150, SCREEN_HEIGHT -220, index ) for i, index in enumerate(card_indices)]
                            player_cards_randomized = True
                        for card in card_list:
                            card.draw_card()
                            if card.pressed:
                                card_actions = {
                                    0: FINN.attack1,
                                    1: FINN.attack2,
                                    2: FINN.attack3,
                                    3: FINN.attack4,
                                    4: FINN.attack5,
                                    5: FINN.potion1,
                                    6: FINN.potion2,
                                    7: FINN.potion3,
                                    8: FINN.potion4,
                                    9: FINN.defence1,
                                    10: FINN.defence2,
                                    11: FINN.defence3,
                                    12: FINN.defence4,
                                    13: FINN.defence5,
                                    14: FINN.special1,
                                    15: FINN.special2,
                                    16: FINN.special3
                                    }
                                if 0 <= card.card_index <= 16:
                                    action_cooldown += 1
                                    if action_cooldown >= action_wait:
                                        card_action = card_actions[card.card_index]
                                        if card.card_index < 5 or card.card_index == 14:
                                            card_action(HOBBIT)
                                        else:
                                            card_action()
                                            
                                        if card.card_index < 5:
                                            FINN.stamina -= 1
                                            if FINN.stamina < 1:
                                                FINN.stamina = 0
                                                if FINN.stamina == 0:
                                                    FINN.hp = FINN.hp // 2
                                                    FINN.stamina = FINN.max_stamina
                                            else:
                                                current_turn += 1
                                        elif 8 < card.card_index < 14:
                                            FINN.stamina -= 0.5
                                            if FINN.stamina < 1:
                                                FINN.stamina = 0
                                                if FINN.stamina == 0:
                                                    FINN.hp = FINN.hp // 2
                                                    FINN.stamina = FINN.max_stamina
                                            else:
                                                current_turn += 1
                                        turn_cooldown = 0
                                        action_cooldown = 0
                                        player_cards_randomized = False
            else:               
                game_over = -1

            if current_turn == 2:
                if HOBBIT.alive == True:
                    turn_cooldown += 1
                    if turn_cooldown >= turn_wait_time:
                        random_action = random.choice(["attack", "defence", "potion", "special1"])
                        if random_action == "attack":
                            HOBBIT.attack(FINN)
                        elif random_action == "defence":
                            HOBBIT.defence()
                        elif random_action == "potion":
                            HOBBIT.potion()
                        elif random_action == "special1":
                            HOBBIT.special(FINN)
                        
                        current_turn += 1
                        turn_cooldown = 0
                
                else:
                    current_turn += 1
                    game_over = 1
            
            if current_turn > total_fighters:
                current_turn = 1
            
        if game_over != 0:
            if game_over == -1:
                SCREEN.blit(defeated_image, (SCREEN_WIDTH / 2 - 200, 100))
            if game_over == 1:
                SCREEN.blit(victory_image, (SCREEN_WIDTH / 2, 100))
            if button1.draw():
                current_turn = 1
                action_cooldown = 0
                game_over = 0   
    pygame.quit()

if __name__ == "__main__":
    main()