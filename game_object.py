'''
Модуль реализует работу игровых объектов.
Он содержит класс объекта и методы для его обработки.
'''

FEATURES = {
    "zombie" : {
        'is_visible' : True,
        'hp' : 15,
        'sight_len' : 10,
        'resizable' : True
    },
    "tree" : {
        'is_visible' : True,
        'hp' : 15,
        'sight_len' : None,
        "resizable" : True,
    },
    'sun' : {
        'is_visible' : True,
        'hp' : 1,
        'sight_len': None,
        'resizable' : False,
    },
}

class GameObject:
    '''
    Класс игрового объекта.
    coords : (int, int) -- координаты на карте.
    name : str -- название объекта.
    is_visible : bool -- истина, если при попадании в поле зрения объект отображается (для
    реализации всевозможных ловушек/невидимок/триггеров).
    hp : int -- здоровье объекта (у построек, соответственно, -- прочность).
    sight_len : int -- радиус зрения (подробнее можно узнать в ./docs/sight.png. 
    '''
    def __init__(self, name, coords):
        if not name in FEATURES:
            raise ValueError('''
            Разрывная!! Юморишь!! 
            Создайте нормального монстра, предусмотренного игрой.
            ''')
        self.name = name
        self.coords = coords
        self.is_visible = FEATURES[name]['is_visible']
        self.hp = FEATURES[name]['hp']
        self.sight_len = FEATURES[name]['sight_len']
        self.resizable = FEATURES[name]['resizable']
