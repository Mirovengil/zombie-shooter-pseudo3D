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
        self.sight_dir = 0

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
        left_side_of_vision = self.sight_dir - 45
        right_side_of_vision = self.sight_dir + 45
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
            all_len_of_sight = math.pi * self.objects[self.sight].sight_len / 2
            polar_angle = math.atan2(obj[1].coords[0], obj[1].coords[1])
            if  not left_side_of_vision <= polar_angle <= right_side_of_vision:
                continue
            #print(polar_angle)
            elem['move'] = (polar_angle  - left_side_of_vision) / (right_side_of_vision - left_side_of_vision)
            objects_in_sight.append(elem)
        return objects_in_sight
