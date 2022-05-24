

from copy import deepcopy

# нулевой пользователь
from quopri import decodestring


class AbsUser:
    pass


# Заказчик
class Customer(AbsUser):
    pass


# Партнёр компании
class Partner(AbsUser):
    pass


class UserFactory:
    types = {
        'customer': Customer,
        'partner': Partner
    }

    # Фабричный метод
    @classmethod
    def create(cls, role):
        return cls.types[role]()


# порождающий паттерн Прототип
class ServicePrototype:
    # прототип вида оборудования

    def clone(self):
        return deepcopy(self)

# вид оборудования
class Service(ServicePrototype):

    def __init__(self, name, equipment):
        self.name = name
        self.equipment = equipment
        self.equipment.services.append(self)


# Пуско-наладочные работы
class CommissioningWorks(Service):
    pass

# Строительно-монтажные работы
class InstalationWorks(Service):
    pass

# Строительно-монтажные работы
class TechnicalMaintenance(Service):
    pass

# Офшорное программирование
class OffshoreProgramming(Service):
    pass

# фабрика сервисов
class ServiceFactory:
    types = {
        'сommissioning': CommissioningWorks,
        'instalation': InstalationWorks,
        'maintenance': TechnicalMaintenance,
        'programming': OffshoreProgramming,
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, equipment):
        return cls.types[type_](name, equipment)

# категория
class Equipment:
    auto_id = 0

    def __init__(self, name, equipment):
        self.id = Equipment.auto_id
        Equipment.auto_id += 1
        self.name = name
        self.equipment = equipment
        self.services = []

    def services_count(self):
        result = len(self.services)
        if self.services:
            result += self.equipment.services_count()
        return result


# основной интерфейс проекта
class Engine:
    def __init__(self):
        self.customers = []
        self.partners = []
        self.services = []
        self.equipments = []

    @staticmethod
    def create_user(role):
        return UserFactory.create(role)

    @staticmethod
    def create_equipment(name, equipment=None):
        return Equipment(name, equipment)

    def find_equipment_by_id(self, id):
        for item in self.equipments:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_service(type_, name, equipment):
        return ServiceFactory.create(type_, name, equipment)

    def get_service(self, name):
        for item in self.services:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# # порождающий паттерн Синглтон
# class SingletonByName(type):
#
#     def __init__(cls, name, bases, attrs, **kwargs):
#         super().__init__(name, bases, attrs)
#         cls.__instance = {}
#
#     def __call__(cls, *args, **kwargs):
#         if args:
#             name = args[0]
#         if kwargs:
#             name = kwargs['name']
#
#         if name in cls.__instance:
#             return cls.__instance[name]
#         else:
#             cls.__instance[name] = super().__call__(*args, **kwargs)
#             return cls.__instance[name]
#
#
# class Logger(metaclass=SingletonByName):
#
#     def __init__(self, name):
#         self.name = name
#
#     @staticmethod
#     def log(text):
#         print('log--->', text)
