import pygame 
import os
import random 

from os.path import isfile, join

SCREEN_WIDTH, SCREEN_HEIGHT = 1100,600
BOTTOM_PANEL = 140
CHARACTER_POSTION_X, CHARACTER_POSTION_Y = (SCREEN_WIDTH / 4), 500


COLOR_RED = (228, 59, 68)
COLOR_RED2 = (162, 38, 51)
COLOR_BLACK = (12, 9, 22)
COLOR_BLACK2 = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
pygame.font.init()

FONT = pygame.font.SysFont('Futile Pro', 18)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

FPS = 60
X_VEL = 3
Y_VEL = 0

pygame.display.set_caption("GAMESUDINW")

current_fighter = 1
total_fighters = 2
action_cooldown = 0
action_wait_time = 200
attack = False

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    SCREEN.blit(img, (x, y))



bg_image = pygame.image.load(f"C:\\Users\\Ronnakrit\\Desktop\\Python\\assets\\background\\3\\6.png").convert_alpha()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH,SCREEN_HEIGHT - 30))
def draw_bg():
    SCREEN.blit(bg_image, (0, 0))
    #draw_text(f'{FINN.name}' , FONT, COLOR_BLACK2, CHARACTER_POSTION_X, CHARACTER_POSTION_Y - 100)
    #draw_text(f'{HOBBIT.name}' , FONT, COLOR_BLACK2, (CHARACTER_POSTION_X * 3), CHARACTER_POSTION_Y - 100)
    pygame.draw.rect(SCREEN, BLACK, drop_zone, 2, border_radius = 10)
    

panel_image = pygame.image.load(f"C:\\Users\\Ronnakrit\\Desktop\\Python\\assets\\tiles\\0.png").convert_alpha()
panel_image = pygame.transform.scale(panel_image, ( SCREEN_WIDTH - 20 , 120))

def draw_panel():
    SCREEN.blit(panel_image, (10, SCREEN_HEIGHT - BOTTOM_PANEL - 20))

sword_image = pygame.image.load(f"C:\\Users\\Ronnakrit\\Desktop\\Python\\assets\\sprite\\sword\\sword.png").convert_alpha()

class Fighter1():
    def __init__(self, x, y, name, max_hp, strength):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.alive = True
        self.animation_list = []
        self.action = 0 # 0:idle 1:run 2:attack 3:hit 4:death 
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.x = x
        self.y = y
        self.vel = X_VEL
        self.fall_count = 0
        
        #load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f"C:\\Users\\Ronnakrit\\Desktop\\Python\\assets\\sprite\\{self.name}\\idle\\{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        
        #load run images 
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f"C:\\Users\\Ronnakrit\\Desktop\\Python\\assets\\sprite\\{self.name}\\run\\{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        #load attack images
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f"C:\\Users\\Ronnakrit\\Desktop\\Python\\assets\\sprite\\{self.name}\\attack\\{i}.png").convert_alpha()
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
            self.idle()
    
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def attack(self, target):
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        if target.hp < 1:
            target.hp = 0
            target.alive = False
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def draw_character(self):
        SCREEN.blit(self.image, self.rect)
    
class Fighter2():
    def __init__(self, x, y, name, max_hp, strength):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.alive = True
        self.animation_list = []
        self.action = 0 # 0:idle 1:run 2:attack 3:hit 4:death  
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.x = x
        self.y = y
        self.vel = X_VEL
        self.fall_count = 0
        
        #load idle images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"C:\\Users\\Ronnakrit\\Desktop\\Python\\assets\\sprite\\{self.name}\\idle\\{i}.png").convert_alpha()
            img = pygame.transform.flip(pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3)), True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        
        #load run images 
        temp_list= []
        for i in range(10):
            img = pygame.image.load(f"C:\\Users\\Ronnakrit\\Desktop\\Python\\assets\\sprite\\{self.name}\\run\\{i}.png").convert_alpha()
            img = pygame.transform.flip(pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3)), True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        #load attack images
        temp_list= []
        for i in range(16):
            img = pygame.image.load(f"C:\\Users\\Ronnakrit\\Desktop\\Python\\assets\\sprite\\{self.name}\\attack\\{i}.png").convert_alpha()
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
            self.idle()
    
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def attack(self, target):
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        if target.hp < 1:
            target.hp = 0
            target.alive = False
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def draw_character(self):
        SCREEN.blit(self.image, self.rect)

class HealtBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        
    def draw(self, hp):
        self.hp = hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(SCREEN, COLOR_BLACK2, (self.x - 5, self.y - 5, 160, 25), border_radius = 5)
        pygame.draw.rect(SCREEN, COLOR_RED, (self.x, self.y, 150 * ratio, 15), border_radius = 5)

class Card():
    def __init__(self, x, y, card_index):
        self.x_original = x
        self.y_original = y
        self.card_index = card_index
        self.in_drop_zone = False
        self.image_list = []  
        for i in range(4):
            img = pygame.image.load(f"C:\\Users\\Ronnakrit\\Desktop\\Python\\assets\\cards\\{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() // 5, img.get_height() // 5))
            self.image_list.append(img)
        self.image = self.image_list[card_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def draw_card(self):
        if self.in_drop_zone == False:
            SCREEN.blit(self.image, self.rect)
        else:
            self.image = pygame.transform.scale(self.image_list[self.card_index], (50, 75))
            self.rect = self.image.get_rect()
            self.rect.center = (drop_zone.centerx, drop_zone.centery)
            SCREEN.blit(self.image, self.rect)
            


FINN = Fighter1(CHARACTER_POSTION_X, CHARACTER_POSTION_Y, 'finn', 200, 10)
HOBBIT = Fighter2(CHARACTER_POSTION_X * 3, CHARACTER_POSTION_Y, 'hobbit', 200, 10)

FINN_health_bar = HealtBar(10, 430, FINN.hp, FINN.max_hp)
HOBBIT_health_bar = HealtBar(940, 430, HOBBIT.hp, HOBBIT.max_hp)

drop_zone = pygame.Rect((SCREEN_WIDTH / 2) - 20, 150, 50, 75,)

random_card1 = random.randint(0,3)
random_card2 = random.randint(0,3)
random_card3 = random.randint(0,3)

card1 = Card(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT - 220, random_card1)  
card2 = Card(SCREEN_WIDTH / 2 , SCREEN_HEIGHT - 220, random_card2)
card3 = Card(SCREEN_WIDTH / 2 + 150 , SCREEN_HEIGHT - 220, random_card3)
card_list = [card1, card2, card3]




def draw_window():
    
    HOBBIT.update_character()
    HOBBIT.draw_character()
    FINN.update_character()
    FINN.draw_character()
    for card in card_list:
        card.draw_card()
    
    pygame.display.update()


def main():

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                for card in card_list:
                    if card.rect.collidepoint(event.pos) and card.in_drop_zone == False:
                        card.in_drop_zone = True
                        card.x_original, card.y_original = drop_zone.centerx, drop_zone.centery
                        
            else:
                clicked = False 
            
        draw_window()
        draw_bg()
        draw_panel()
        FINN_health_bar.draw(FINN.hp)
        HOBBIT_health_bar.draw(HOBBIT.hp) 
        
        attack = False
        target = None
        pygame.mouse.set_visible(True)
        pos = pygame.mouse.get_pos()
        if HOBBIT.rect.collidepoint(pos):
            pygame.mouse.set_visible(False)
            SCREEN.blit(sword_image, pos)
            if clicked == True:
                attack = True
                target = HOBBIT


        #player action
        if FINN.alive == True:
            global current_fighter, action_cooldown
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    if attack == True and target != None:
                        FINN.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
        #enemy action
        if current_fighter == 2:
            if HOBBIT.alive == True:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    HOBBIT.attack(FINN)
                    current_fighter += 1
                    action_cooldown = 0
            else:
                current_fighter += 1
        if current_fighter > total_fighters:
            current_fighter = 1  
        
          
    
    pygame.quit()

if __name__ == "__main__":
    main()