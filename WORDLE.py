import pygame
import sys
import time
import random
import nltk


nltk.download('words')

from nltk.corpus import words


english_words = words.words()


five_letter_words = [word for word in english_words if len(word) == 5]
wordy = random.choice(five_letter_words) * 6
wordx = wordy.upper()






pygame.init()
screen = pygame.display.set_mode((850,900))
pygame.display.set_caption('WORDLE')
running = True
icon = pygame.image.load('iconwordle.png')
pygame.display.set_icon(icon)
white = (255, 255, 255)
green = (83,141,78)
blue = (0, 0, 128)
red = (255,0,0)
black = (0,0,0)
yellow = (181,159,60)
gray = (80,80,80)

is_end_screen = False

row = 0
rows_logic = {0:5,1:10,2:15,3:20,4:25,5:30}
row_colors = None

won = False

last_tile_list = [5,10,15,20,25,30]

font = pygame.font.Font('HelveticaNeueBold.ttf', 75)
start_point = (0, 100)
end_point = (900,100)
text = font.render('Wordle', True, white)
textRect = text.get_rect()
textRect.center = (850 // 2, 50)

buttons_names = 'QWERTYUIOPASDFGHJKLZXCVBNM'
buttons_list = []

tile_list = []
current_tile = 0


win_average = None
last_win = 'n/a'
wins_list = []


stats = False



class Button:
    global buttons_names
    global stats

    def __init__(self, x, y, width, height, text, text_color, button_color, outline_color, action, image_path = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.outline_color = outline_color
        self.action = action
        self.outline = pygame.Rect(x-3, y-3, width + 6, height + 6)
        self.image = None

        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width,height))
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.outline_color, self.outline) 
        pygame.draw.rect(screen, self.button_color, self.rect)
        if self.image:
            screen.blit(self.image, (self.x, self.y))

        else:
            font = pygame.font.Font('HelveticaNeueBold.ttf', 30)
            if self.text == 'ENTER':
                font = pygame.font.Font('HelveticaNeueBold.ttf', 20)
            text = font.render(self.text, True, self.text_color)
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            if self.text in buttons_names:
                self.action(self.text)
            else:
                self.action()

class Tile:
    def __init__(self, x, y, color, outline_color,letter):
        self.color = color
        self.outline_color = outline_color
        self.letter = letter
        self.selected = False
        self.rect = pygame.Rect(x,y, 70, 70)
        self.outline = pygame.Rect(x-3,y-3,76,76)
    def draw(self, screen):
        pygame.draw.rect(screen, self.outline_color, self.outline)
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font('HelveticaNeueBold.ttf', 40)
        if self.letter:
            lettery = font.render(self.letter, True, white)
            letter_rect = lettery.get_rect(center=self.rect.center)
            screen.blit(lettery, letter_rect)
    def letter_delete(self):
        if self.letter:
            self.letter = ''


def create_tiles(x,y,color,outline_color,letter):
    global tile_list
    count= 0
    row = 0
    for i in range(0,30):
        row = i//5
        if count == 5:
            count = 0

        temp_tile = Tile(x + (80*count), y + (80*row), color, outline_color, letter)
        tile_list.append(temp_tile)
        count += 1

def add_letter(letterx):
    global current_tile
    global tile_list
    global rows_logic

    if current_tile < rows_logic[row]:
        tile_list[current_tile].letter = letterx
        current_tile += 1

def create_keyboard(listx,x ,y, width, height):
    global buttons_list
    count = 0
    coordinates = 0
    save_x = x
    for name in listx:
        if count == 10:
            y += 60
            x = save_x + 30
            save_x = x
            coordinates = 0
        if count == 19:
            y += 60
            x = save_x + 60
            save_x = x
            coordinates = 0

        temp_button = Button(x + (60*coordinates), y, 50, 50,name, white, black, white, add_letter)
        coordinates += 1
        count += 1
        buttons_list.append(temp_button)


create_keyboard(buttons_names, 130, 700, 40, 40)
create_tiles(227, 175, black, white,'')


def play_again():
    global won
    global row
    global current_tile
    global tile_list
    global wordx
    global is_end_screen
    global last_tile_list
    last_tile_list = [5,10,15,20,25,30]

    for i in tile_list:
        i.letter = ''
    for i in tile_list:
        i.color = black
    for i in buttons_list:
        i.button_color = black
    won = False
    row = 0
    current_tile = 0
    is_end_screen = False
    wordy = random.choice(five_letter_words) * 6
    wordx = wordy.upper()


def stat_screen():
    global stats
    global win_average
    global last_win
    global stats_rect
    stats = not stats
    

def end_screen():
    global wordx
    x = 200
    y = 125
    width = 450
    height = 500
    end_screen_rect = pygame.Rect(x,y,width,height)
    end_screen_outline = pygame.Rect(x-3,y-3,width+6,height+6)
    pygame.draw.rect(screen,white,end_screen_outline)
    pygame.draw.rect(screen,black, end_screen_rect)

    text = None
    if won:
        text = font.render('You won!', True, green)
    else:
        text = font.render("You lost!", True, red)
    word_font = pygame.font.Font('HelveticaNeueBold.ttf', 25)
    word_text = None
    word_render = wordx[:5].lower()
    
    word_text = word_font.render(f'The word was: {word_render} ', True, white)
    word_rect = word_text.get_rect()
    word_rect.center = (425, 325)
    
    screen.blit(word_text, word_rect)
    

    text_rect = text.get_rect()
    text_rect.center = (425,250)
    screen.blit(text, text_rect)

def delete_letter():
    global row
    global current_tile
    global rows_logic
    if row == 0:
        if current_tile > 0:
            current_tile -= 1  
            tile_list[current_tile].letter_delete()
    else:
        if current_tile > rows_logic[row - 1]:
            current_tile -= 1  
            tile_list[current_tile].letter_delete()
    tile_list[current_tile].draw(screen)
def check_win():
    global row_colors
    global won
    global row
    global last_win
    global wins_list
    global win_average

    if black not in row_colors and yellow not in row_colors:
        won = True
        last_win = row 
        wins_list.append(last_win)
        win_average = sum(wins_list) / len(wins_list)
        win_average = "%.2f" % win_average
        win_average = str(win_average)

def enter():
    global tile_list
    global row
    global last_tile_list
    global row_colors
    global wordx

    row_letters = [i.letter for i in tile_list[:current_tile]]
    input = ''.join(row_letters)

    for letter in input:
        if letter not in wordx:
            for button in buttons_list:
                if button.text == letter:
                    button.button_color = gray

    if current_tile in last_tile_list:
        for indx, char in enumerate(input):
            if char in wordx:
                tile_list[indx].color = yellow
            if char in wordx and char == wordx[indx]:
                tile_list[indx].color = green

        row_colors = [i.color for i in tile_list[(0 +(5*row)):current_tile]]
        row += 1
        check_win()
        last_tile_list.pop(0)
    
                
def show_stats():
    global last_win
    global win_average

    x = 200
    y = 125
    width = 450
    height = 500
    end_screen_rect = pygame.Rect(x,y,width,height)
    end_screen_outline = pygame.Rect(x-3,y-3,width+6,height+6)
    pygame.draw.rect(screen,white,end_screen_outline)
    pygame.draw.rect(screen,black, end_screen_rect)
    stats_font = pygame.font.Font('HelveticaNeueBold.ttf', 30)
    info_font = pygame.font.Font('HelveticaNeueBold.ttf', 20)

    stats_surface = font.render("STATISTICS", True, white)
    stats_rect = stats_surface.get_rect()
    stats_rect.center = (425,200)

    last_win_surface = info_font.render(f"Last win: {last_win}", True, white)
    last_win_rect = last_win_surface.get_rect()
    last_win_rect.center = (400, 300)

    win_average_surface = info_font.render(f"Win average: {win_average}", True, white)
    win_average_rect = win_average_surface.get_rect()
    win_average_rect.center = (400, 350)

    screen.blit(stats_surface, stats_rect)
    screen.blit(last_win_surface, last_win_rect)
    screen.blit(win_average_surface, win_average_rect)

button_image = 'flip.png'

delete_button = Button(640, 820, 77, 50, '-',white, black, white, delete_letter, button_image)
enter_button = Button(110,820,100,50,'ENTER', white,black,white, enter)

stats_button = Button(750, 25, 50,50,'?',white,black,white, stat_screen)
play_again_button = Button(345, 480, 160,50, "Play again", green, black, green, play_again)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                for button in buttons_list:
                    button.is_clicked(pos)
                delete_button.is_clicked(pos)
                enter_button.is_clicked(pos)
                play_again_button.is_clicked(pos)
                
                if stats_button.is_clicked(pos):
                    stats_button.action()
                    time.sleep(0.1)
                    

    screen.fill('black')
    screen.blit(text,textRect)

    if not stats:
        if won or row == 6 and not won:
            is_end_screen =  True
            if is_end_screen:
                end_screen()
                play_again_button.draw(screen)
                stats_button.draw(screen)
            
        else:
            delete_button.draw(screen)
            enter_button.draw(screen)
            stats_button.draw(screen)

            for button in buttons_list:
                button.draw(screen)
            for tile in tile_list:
                tile.draw(screen)
    if stats:
        show_stats()
        stats_button.draw(screen)
        

    pygame.draw.line(screen, white, start_point, end_point, 1)
    pygame.display.update()


pygame.quit()