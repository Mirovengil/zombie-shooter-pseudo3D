'''
Модуль содержит реализацию класса игровой карты и методов для работы с ней.
'''

import game_object 
import math
import random

PRECISION = 5
WALL_POINTS_FREQ = 1.5
EPS = 10 ** -6

class Biom:
    '''
    Класс игрового биома.
    Биом является кругом, внутри которого находится уникальное окружение (извиняюсь
    за каламбур).
    От этого зависит цвет неба и земли.
    В будущем, возможно, он будет влиять на типы появляющихся монстров, что
    является ещё одним поводом для выноса его в отдельный класс.
    Был бы нормальный язык -- была бы структура.
    type : str -- тип биома. Носит вид строки для того, чтобы проще было обращаться к его
    характеристикам.
    center : (int, int) -- координаты центра биома на карте.
    radius : float -- радиус биома.
    '''
    STD_BIOM = "wood"

    types = ['wood', 'desert']

    def __init__(self, center, radius, biom_type=None):
        if biom_type is None:
            biom_type = random.randint(0, len(Biom.types) - 1)
            biom_type = Biom.types[biom_type]
        self.type = biom_type
        if radius <= 0:
            raise ValueError('Хахаха, юморишь, разрывная!! Давай нормальный радиус ставь у биома.')
        self.radius = radius
        self.center = center

    def is_in(self, coords):
        '''
        При условии, что координата coords : (float, float) принадлежит биому,
        возвращает истину.
        '''
        dist_to_point = get_dist_between_points(self.center, coords)
        if dist_to_point <= self.radius:
            return True
        else:
            return False

def get_point_on_circle_by_angle(center, radius, angle):
    '''
    Возвращает точку на окружности с центром в точке center : (float, float) и радиусом
    radius : float, если эту окружность считать единичной и провести угол angle : int,
    то в оную точку попадёт прямая, соответствующая углу.
    '''
    

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
    return round(value, PRECISION)

class GameMap:
    '''
    Класс для обработки игровой карты и событий, происходящих на ней.
    Карта представляет собой ось декартовых координат, на которой расположены объекты.
    objects : [GameObject] -- список всех объектов, находящихся на карте.
    sight : int -- индекс объекта, от лица которого ведётся наблюдение (пока работает так,
    чтобы проверить корректность работы поля зрения ото всех элементов).
    sight_dir : int -- направление взгляда (как на окружности из тригонометрии:
    вверх -- 90 градусов).
    bioms : [Biom] -- массив биомов на карте. 
    '''

    #Константа, определяющая размер поля зрения игрока.
    #Если угол зрения равен 90, то HALF_OF_VISION_ANGLE = 45 (идёт отклонение от
    #направления взгляда на величину HALF_OF_VISION_ANGLE).
    HALF_OF_VISION_ANGLE = 45

    
    def __init__ (self):
        self.objects = []
        self.sight = None
        self.sight_dir = 90
        self.bioms = []

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
                'prior' : float -- приоритет вывода (сначала отрисовываются картинки с наименьшим
                приоритетом).
            }
        ]
        '''
        self.sight_dir = degree(self.sight_dir)
        left_side_of_vision = degree(self.sight_dir - GameMap.HALF_OF_VISION_ANGLE)
        right_side_of_vision = degree(self.sight_dir + GameMap.HALF_OF_VISION_ANGLE)
        objects_in_sight = []
        for obj in enumerate(self.objects):
            if obj[0] == self.sight:
                continue
            if not obj[1].is_visible:
                continue
            if get_dist_between_points(self.objects[self.sight].coords, obj[1].coords)\
            > self.objects[self.sight].sight_len and obj[1].resizable:
                continue
            elem = dict()
            elem['prior'] = get_dist_between_points(self.objects[self.sight].coords, obj[1].coords)
            elem['name'] = obj[1].name
            if obj[1].resizable:
                elem['dist'] = 1 - (get_dist_between_points(self.objects[self.sight].coords, obj[1].coords)\
                / self.objects[self.sight].sight_len)
            else:
                elem['dist'] = 1
            obj_x = obj[1].coords[0]
            obj_y = obj[1].coords[1]
            sight_x = self.objects[self.sight].coords[0]
            sight_y = self.objects[self.sight].coords[1]
            obj_x -= sight_x
            obj_y -= sight_y
            polar_angle = math.atan2(obj_y, obj_x)
            polar_angle = degree(polar_angle * 180 / math.pi)
            if not left_side_of_vision <= polar_angle <= right_side_of_vision and not\
            degree(left_side_of_vision + 90) <= degree(polar_angle + 90) <= degree(right_side_of_vision + 90):
                continue
            if left_side_of_vision < right_side_of_vision:
                elem['move'] = (polar_angle - left_side_of_vision) / (right_side_of_vision - left_side_of_vision)
            else:
                elem['move'] = (degree(polar_angle + 90) - degree(left_side_of_vision + 90)) / (degree(right_side_of_vision + 90) - degree(left_side_of_vision + 90))
            objects_in_sight.append(elem)
        return objects_in_sight

    def move_obj(self, way, obj_index=None):
        '''
        Перемещает объект под индексом obj_index : int на расстояние way : float.
        Перемещает в том направлении, куда смотрит объект (просто шаг вперёд).
        '''
        sight_angle = round(self.sight_dir * math.pi / 180, PRECISION)
        if obj_index is None:
            obj_index = self.sight
        obj = self.objects[obj_index]
        x = obj.coords[0]
        y = obj.coords[1]
        x = x + round(way * math.cos(sight_angle), PRECISION)
        y = y + round(way * math.sin(sight_angle), PRECISION)
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

    def get_biom_info(self):
        '''
        Возвращает тип биома (str), в котором на данный момент находится игрок.
        Основной тип биома -- STD_BIOM (значение можно посмотреть/поменять в классе биома).
        '''
        biom_info = dict()
        for i in self.bioms:
            if i.is_in(self.objects[self.sight].coords):
                biom_info['type'] = i.type
        if not 'type' in biom_info:
            biom_info['type'] = Biom.STD_BIOM
        right_angle_of_vision = degree(self.sight_dir - GameMap.HALF_OF_VISION_ANGLE)
        left_angle_of_vision = degree(self.sight_dir + GameMap.HALF_OF_VISION_ANGLE)
        
        #left_dist_from_player_to_side_of_biom
        return biom_info

    def add_biom(self, center, radius, biom_type=None):
        '''
        Добавляет на игровую карту биом типа bioms_type : str (если не указывать, будет
        выбран случайный тип биома) с центром в точке center : (float, float); радиус
        биома равен radius : float.
        '''
        self.bioms.append(Biom(center, radius, biom_type))

    def add_wall(self, start_point, finish_point):
        '''
        Добавляет на карту стену, которая идёт от точки start_point : (float, float) до точки
        finish_point : (float, float).
        Реализация следующая:
        Стена представляется в виде набора точек, которые лежат на расстоянии 1 / WALL_POINTS_FREQ
        друг от друга и все принадлежат отрезку (start_point, finish_point), который является стеной.
        '''
        x1 = start_point[0]
        y1 = start_point[1]
        x2 = finish_point[0]
        y2 = finish_point[1]
        line_a = y2 - y1
        line_b = x1 - x2
        line_c = -line_a * x1 - line_b * y1
        #количество точек, расположенных на отрезке стены.
        points_number = int(get_dist_between_points(start_point, finish_point) * WALL_POINTS_FREQ)
        x_change = 0
        left = x1
        right = x2
        while (right - left) >= EPS:
            temp_x = (left + right) / 2
            temp_y = (line_a * temp_x + line_c) / (-line_b)
            if get_dist_between_points(start_point, (temp_x, temp_y)) < 1 / WALL_POINTS_FREQ:
                left = temp_x
            else:
                right = temp_x
        x_change = (left + right) / 2 - x1
        now_point_x = x1
        while now_point_x < x2:
            now_point_y = (line_a * now_point_x + line_c) / (-line_b)
            self.add_object('wall', (now_point_x, now_point_y))
            now_point_x += x_change
