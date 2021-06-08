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

INF = 10 ** 10

def draw_sight_dir(screen, degrees, pictures):
    '''
    Отрисовывает направление взгляда игрока в левом нижнем углу (для удобства
    ориентации в пространстве).
    '''
    image = pictures['sight_dir']
    IMG_SIZE_X = image.get_rect().width
    IMG_SIZE_Y = image.get_rect().height
    image = pygame.transform.rotate(image, degrees)
    window_size_x = pygame.display.get_surface().get_width()
    window_size_y = pygame.display.get_surface().get_height()
    STD_SIGHT_DIR_PLACE_X = IMG_SIZE_X
    STD_SIGHT_DIR_PLACE_Y = window_size_y - IMG_SIZE_Y
    rect = image.get_rect()
    rect.center = (STD_SIGHT_DIR_PLACE_X, STD_SIGHT_DIR_PLACE_Y)
    screen.blit(image, rect)
    

def draw_object(game_screen, obj, pictures):
    '''
    Выводит на экран элемент obj:
    {
            "name" : str -- название объекта (чтобы через него можно было корректно
            получать изображение объекта).
            "dist" : float -- расстояние от объекта под индексом sight до данного (в процентах).
            "move" : float -- смещение объекта от левого края поля зрения (в процентах).
            Подробнее см. ./docs/sight.png.
            'prior' : float -- приоритет вывода (сначала отрисовываются картинки с наименьшим
            приоритетом).
    }
    '''
    object_name = obj['name']
    window_size_x = pygame.display.get_surface().get_width()
    window_size_y = pygame.display.get_surface().get_height()
    if obj['dist'] < 0.4:
        object_name = object_name + "_very_long"
    elif obj['dist'] < 0.7:
        object_name = object_name + "_long"
    object_size_y = window_size_y * obj['dist']
    object_size_x = window_size_x * obj['dist']
    place_y = (window_size_y - object_size_y) // 2
    place_x = window_size_x * obj['move'] - object_size_x // 2
    game_screen.blit(pygame.transform.scale(pictures[object_name],\
    (int(object_size_x), int(object_size_y))), (place_x, place_y))


def draw_player_data(game_screen, data, pictures):
    '''
        Выводит на экран game_screen информацию data.
        pictures['info_font'] -- шрифт для данного вывода.
        pictures['info_font_color'] -- цвет оного шрифта.
        Учитывается смещение из-за "компаса", который показывает
        направление взгляда.
        data должна иметь следующий вид:
        {
            'name' : str -- название объекта, за который ведётся просмотр.
            'hp' : int -- количество единиц жизни у него.
            coords : (float, float) -- координата, где расположен объект.
        }
    '''
    text = []
    text.append('object: ' + data['name'])
    text.append('hp: ' + str(data['hp']))
    text.append('angle: ' + str(data['angle']))
    text.append('coordinates: ' + str(data['coords']))
    window_size_x = pygame.display.get_surface().get_width()
    window_size_y = pygame.display.get_surface().get_height()
    sight_dir_size_x = pictures['sight_dir'].get_rect().width * 1.5
    sight_dir_size_y =  pictures['sight_dir'].get_rect().height
    text_height = sight_dir_size_y * 0.5
    for i in text:
        rez = pictures['info_font'].render(i, False, pictures['info_font_color'])
        text_height += rez.get_height()
        info_top_side = window_size_y - text_height
        game_screen.blit(rez, (sight_dir_size_x + 10, info_top_side))

def draw_line_of_horisont(screen, pictures):
    '''
    Отрисовывает небольшую "линию горизонта": делает небо синим, землю -- зелёной.
    Возможно, в будущем будут добавлены биомы, но пока что -- так-с.
    И рисует Солнце*
    '''
    window_size_x = pygame.display.get_surface().get_width()
    window_size_y = pygame.display.get_surface().get_height()
    pygame.draw.rect(screen, pictures['sky_color'], (0, 0, window_size_x, window_size_y // 2))
    pygame.draw.rect(screen, pictures['dirt_color'], (0, window_size_y // 2, window_size_x, window_size_y))

def draw_game_map(game_screen, game_map, pictures):
    '''
    Выводит на экран game_screen игровую карту game_map : GameMap от первого лица.
    '''
    objects = game_map.get_sight()
    objects.sort(key=lambda a: a['prior'], reverse=True)
    draw_line_of_horisont(game_screen, pictures)
    #print(objects)
    #input()
    for obj in objects:
        draw_object(game_screen, obj, pictures)
    draw_sight_dir(game_screen, game_map.sight_dir, pictures)
    draw_player_data(game_screen, game_map.get_data_of_sighter(), pictures)

def main(game_screen, pictures):
    '''
    Основной цикл работы программы.
    '''
    timer = pygame.time.get_ticks()
    game_is_finished = False
    while not game_is_finished:
        draw_game_map(screen, game_map, pictures)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_is_finished = True
            pressed_keys = pygame.key.get_pressed()
            if pygame.time.get_ticks() - timer >= 100:
                if pressed_keys[pygame.K_a]:
                    game_map.sight_dir -= 1
                if pressed_keys[pygame.K_d]:
                    game_map.sight_dir += 1
                if pressed_keys[pygame.K_w]:
                    game_map.move_obj(1)
                if pressed_keys[pygame.K_s]:
                    game_map.move_obj(-1)
                if pressed_keys[pygame.K_b]:
                   game_map.sight_dir += 180
                timer = pygame.time.get_ticks()
                screen.fill((0, 0, 0))
                pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    game_map = game_map.GameMap()
    game_map.add_object('zombie', (0, 0), True)
    game_map.add_object('zombie', (0, 7))
    game_map.add_object('zombie', (0, -7))
    game_map.add_object('tree', (3, 5))
    game_map.add_object('tree', (-4, -2))
    game_map.add_object('sun', (INF, 2 * INF))
    screen = pygame.display.set_mode((STD_SIZE_Y, STD_SIZE_X))
    pictures = dict()
    for pic in ['zombie', 'sight_dir', 'tree', 'zombie_long', 'zombie_very_long', 'tree_long', 'tree_very_long', 'sun']:
        pictures[pic] = pygame.image.load('./images/' + pic + '.png').convert_alpha()
    pictures['info_font'] = pygame.font.SysFont('ubuntu', 14)
    pictures['info_font_color'] = (255, 255, 255)
    pictures['dirt_color'] = (65, 174, 60)
    pictures['sky_color'] = (39, 154, 214)
    pictures['back_color'] = (10, 10, 10)
    main(game_map, pictures)
