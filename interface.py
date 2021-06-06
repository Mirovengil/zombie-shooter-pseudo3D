'''
Программа выводит интерфейс для взаимодействия с пользователем и
обрабатывает действия последнего до момента закрытия программы.
Возможно, будут предприняты действия по переводу структуры программы в
форму класса.
'''

import pygame
import game_map

STD_SIZE_Y = 640
STD_SIZE_X = 480

def draw_object(game_screen, obj, pictures):
    '''
    Выводит на экран элемент obj:
    {
            "name" : str -- название объекта (чтобы через него можно было корректно
            получать изображение объекта).
            "dist" : float -- расстояние от объекта под индексом sight до данного (в процентах).
            "move" : float -- смещение объекта от левого края поля зрения (в процентах).
            Подробнее см. ./docs/sight.png.  
    }
    '''

    object_name = obj['name']

    window_size_x = pygame.display.get_surface().get_width()
    window_size_y = pygame.display.get_surface().get_height()

    object_size_x = window_size_x * obj['dist']
    object_size_y = window_size_y * obj['dist']
    place_y = (window_size_y - object_size_y) // 2
    place_x = window_size_x * obj['move'] - object_size_x // 2

    #place = (place_x, place_y, place_x + object_size_x, place_y + object_size_y)
    game_screen.blit(pygame.transform.scale(pictures[object_name],\
    (int(object_size_x), int(object_size_y))), (place_x, place_y))
    
    #print(place_x, place_y)
    #print(object_size_x, object_size_y)
    #print(window_size_x, window_size_y)

def draw_game_map(game_screen, game_map, pictures):
    '''
    Выводит на экран game_screen игровую карту game_map : GameMap от первого лица.
    '''
    objects = game_map.get_sight()
    #print(objects)
    #input()
    for obj in objects:
        draw_object(game_screen, obj, pictures)

def main(game_screen, pictures):
    '''
    Основной цикл работы программы.
    '''
    game_is_finished = False
    while not game_is_finished:
        draw_game_map(screen, game_map, pictures)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_is_finished = True
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_a]:
                game_map.sight_dir -= 1
            if pressed_keys[pygame.K_d]:
                game_map.sight_dir += 1
            screen.fill((0, 0, 0))
            pygame.display.flip()
if __name__ == "__main__":
    pygame.init()
    game_map = game_map.GameMap()
    game_map.add_object('zombie', (0, 0), True)
    game_map.add_object('zombie', (0, 7))
    screen = pygame.display.set_mode((STD_SIZE_Y, STD_SIZE_X))
    pictures = dict()
    for pic in ['zombie']:
        pictures[pic] = pygame.image.load('./images/' + pic + '.png').convert_alpha()
    main(game_map, pictures)
