import pygame
import random


SCREEN_WIDTH, SCREEN_HEIGHT = 1100,600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
pygame.font.init()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

FPS = 60

pygame.display.set_caption("GAMESUDINW")

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
    
drop_zone = pygame.Rect((SCREEN_WIDTH / 2) - 20, 150, 50, 75,)
BG = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

random_card1 = random.randint(0,1)
random_card2 = random.randint(0,1)
random_card3 = random.randint(0,1)

card1 = Card(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT - 220, random_card1)  
card2 = Card(SCREEN_WIDTH / 2 , SCREEN_HEIGHT - 220, random_card2)
card3 = Card(SCREEN_WIDTH / 2 + 150 , SCREEN_HEIGHT - 220, random_card3)
card_list = [card1, card2, card3]


clicked = False

def draw_window():
    
    for card in card_list:
        card.draw_card()
    
    pygame.display.update()

def main():
    global clicked
    is_drop_zone_occupied = False
    card_in_drop_zone = None
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
                    if card.rect.collidepoint(event.pos) and card.in_drop_zone == False and is_drop_zone_occupied == False :
                        card.x_original, card.y_original = drop_zone.centerx, drop_zone.centery
                        card.in_drop_zone = True
                        is_drop_zone_occupied = True
                        card_in_drop_zone = card
            elif event.type == pygame.MOUSEBUTTONUP:
                clicked = False 
        
        draw_window()
        pygame.draw.rect(SCREEN, WHITE, BG)
        pygame.draw.rect(SCREEN, BLACK, drop_zone, 2, border_radius = 10)
    pygame.quit()

if __name__ == "__main__":
    main()