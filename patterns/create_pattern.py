
import os
import sys
from copy import deepcopy

# нулевой пользователь
from datetime import datetime
from quopri import decodestring


# "Безымянный" сиглтон
class UnnamedSingleForLogger(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(UnnamedSingleForLogger, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=UnnamedSingleForLogger):
    @staticmethod
    def log(text):
        # Прописываем путь лог-файла
        PATH = os.path.dirname(os.path.abspath(__file__))
        PATH = os.path.join(PATH, 'views.log')
        # Сохраняем текущий стандартный вывод,
        # чтобы можно было вернуть sys.stdout после завершения перенаправления
        stdout_fileno = sys.stdout
        # Направляем вывод sys.stdout в лог-файл
        sys.stdout = open(PATH, 'a', encoding="utf-8")
        # Печатаем в лог-файле текст лога
        sys.stdout.write(f"{datetime.now().strftime('%H:%M:%S - %d.%m.%Y ')} {text} \n")
        # Выводим текст лога на фактический сохраненный обработчик
        stdout_fileno.write(f"{datetime.now().strftime('%H:%M:%S - %d.%m.%Y ')} {text} \n")
        # Закрываем файл
        sys.stdout.close()
        # Восстанавливаем sys.stdout в наш старый сохраненный обработчик файлов
        sys.stdout = stdout_fileno




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

# Оборудование
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
        if self.equipment:
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




if __name__ == "__main__":
    logger1 = Logger()
    logger2 = Logger()

    print(logger1, logger2)

    logger1.log('Привет')
    logger2.log('Здорово')