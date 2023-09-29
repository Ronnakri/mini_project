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
        self.mouse_over = False
        self.card_index = card_index
        self.image_list = []  
        for i in range(4):
            img = pygame.image.load(f"C:\\Users\\Ronnakrit\\Desktop\\Python\\assets\\cards\\{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() // 5, img.get_height() // 5))
            self.image_list.append(img)
        self.image = self.image_list[card_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def draw_card(self):
        if self.mouse_over:
            self.rect.y = self.y_original - 50
        else:
            self.rect.y = self.y_original
        SCREEN.blit(self.image, self.rect)
    
    def handle_mouse_hovel(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.mouse_over = True
        else:
            self.mouse_over = False    
    

BG = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

random_card1 = random.randint(0,3)
random_card2 = random.randint(0,3)
random_card3 = random.randint(0,3)

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
                for card in card_list:
                    card.handle_mouse_hovel()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                clicked = False 
        
        draw_window()
        pygame.draw.rect(SCREEN, WHITE, BG)
        
    pygame.quit()

if __name__ == "__main__":
    main()