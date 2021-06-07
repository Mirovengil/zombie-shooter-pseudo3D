'''
Модуль содержит реализацию класса игровой карты и методов для работы с ней.
'''

import game_object 
import math

def get_dist_between_points(one_point, other_point):
    '''
    Возвращает расстояние между двумя точками one_point : (int, int) и
    other_point : (int, int) на декартовой оси координат.
    '''
    x1 = one_point[0] 
    x2 = other_point[0]
    y1 = one_point[1] 
    y2 = other_point[1]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 

def degree(value):
    '''
    Приводит значение к промежутку от 0 до 360.
    '''
    if (value < 0):
        value += 360
    if (value > 360):
        value %= 360
    return round(value, 5)

class GameMap:
    '''
    Класс для обработки игровой карты и событий, происходящих на ней.
    Карта представляет собой ось декартовых координат, на которой расположены объекты.
    objects : [GameObject] -- список всех объектов, находящихся на карте.
    sight : int -- индекс объекта, от лица которого ведётся наблюдение (пока работает так,
    чтобы проверить корректность работы поля зрения ото всех элементов).
    sight_dir : int -- направление взгляда (как на окружности из тригонометрии:
    вверх -- 90 градусов). 
    '''
    def __init__ (self):
        self.objects = []
        self.sight = None
        self.sight_dir = 90

    def add_object(self, name, coords, sight=False):
        '''
        Добавляет на игровую карту, в точку coords : (int, int) объект name : str.
        Если sight : bool истинно, то наблюдение ведётся от лица данного объекта.
        '''
        self.objects.append(game_object.GameObject(name, coords))
        if sight:
            self.sight = len(self.objects) - 1

    def get_sight(self):
        '''
        Возвращает поле зрения, содержащее попавшие в него объекты,  в
        следующем формате:
        [
            {
                "name" : str -- название объекта (чтобы через него можно было корректно
                получать изображение объекта).
                "dist" : float -- расстояние от объекта под индексом sight до данного (в процентах).
                "move" : float -- смещение объекта от левого края поля зрения (в процентах).
                Подробнее см. ./docs/sight.png.  
            }
        ]
        '''
        self.sight_dir = degree(self.sight_dir)
        left_side_of_vision = degree(self.sight_dir - 45)
        right_side_of_vision = degree(self.sight_dir + 45)
        objects_in_sight = []
        for obj in enumerate(self.objects):
            if obj[0] == self.sight:
                continue
            if not obj[1].is_visible:
                continue
            if get_dist_between_points(self.objects[self.sight].coords, obj[1].coords)\
            > self.objects[self.sight].sight_len:
                continue
            elem = dict()
            elem['name'] = obj[1].name
            elem['dist'] = 1 - (get_dist_between_points(self.objects[self.sight].coords, obj[1].coords)\
             / self.objects[self.sight].sight_len)
            obj_x = obj[1].coords[0]
            obj_y = obj[1].coords[1]
            sight_x = self.objects[self.sight].coords[0]
            sight_y = self.objects[self.sight].coords[1]
            obj_x -= sight_x
            obj_y -= sight_y
            polar_angle = math.atan2(obj_y, obj_x)
            polar_angle = degree(polar_angle * 180 / math.pi)
            if left_side_of_vision > right_side_of_vision:
                #Это возможно только в случае, если left_side_of_vision принадлежит
                #четвёртой четверти, а right_side_of_vision -- первой.
                #Чтобы это исправить, развернём все углы на 120 градусов.
                left_side_of_vision = degree(left_side_of_vision - 120)
                right_side_of_vision = degree(right_side_of_vision - 120)
                polar_angle = degree(polar_angle - 120)
            if not left_side_of_vision <= polar_angle <= right_side_of_vision:
                continue
            elem['move'] = (polar_angle - left_side_of_vision) / (right_side_of_vision - left_side_of_vision)

            objects_in_sight.append(elem)
        return objects_in_sight

    def move_obj(self, way, obj_index=None):
        '''
        Перемещает объект под индексом obj_index : int на расстояние way : float.
        Перемещает в том направлении, куда смотрит объект (просто шаг вперёд).
        '''
        sight_angle = round(self.sight_dir * math.pi / 180, 5)
        if obj_index is None:
            obj_index = self.sight
        obj = self.objects[obj_index]
        x = obj.coords[0]
        y = obj.coords[1]
        x = x + round(way * math.cos(sight_angle), 5)
        y = y + round(way * math.sin(sight_angle), 5)
        self.objects[obj_index].coords = (x, y)

    def get_data_of_sighter(self):
        '''
        Возвращает информацию о том объекте, который находится под
        индексом sight.
        В следующем формате: {
            'name' : str -- название объекта, за который ведётся просмотр.
            'hp' : int -- количество единиц жизни у него.
            coords : (int, int) -- координата, где расположен объект.
        }
        '''
        info = dict()
        info['name'] = self.objects[self.sight].name
        info['hp'] = self.objects[self.sight].hp
        info['coords'] = (int(self.objects[self.sight].coords[0]), int(self.objects[self.sight].coords[1]))
        info['angle'] = self.sight_dir
        return info
