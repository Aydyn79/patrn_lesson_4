from frame.templator import render
from logs.config_client_log import LOGGER
from patterns.create_pattern import Engine

site = Engine()

class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 OK', render('page.html', date=request.get('date', None))

class Contact_us:
    def __call__(self, request):
        return '200 OK', render('contact.html', date=request.get('date', None))

# контроллер - список сервисов
class ServicesList:
    def __call__(self, request):
        LOGGER.info('Список видов сервисов')
        try:
            equipment = site.find_equipment_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('service_list.html',
                                    objects_list=equipment.services,
                                    name=equipment.name, id=equipment.id)
        except KeyError:
            return '200 OK', 'Ни одного сервиса еще не добавлено'


# контроллер создания сервиса
class CreateService:
    equipment_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            equipment = None
            if self.equipment_id != -1:
                equipment = site.find_equipment_by_id(int(self.equipment_id))

                service = site.create_service('record', name, equipment)
                site.services.append(service)

            return '200 OK', render('service_list.html',
                                    objects_list=equipment.services,
                                    name=equipment.name,
                                    id=equipment.id)

        else:
            try:
                self.equipment_id = int(request['request_params']['id'])
                equipment = site.find_equipment_by_id(int(self.equipment_id))

                return '200 OK', render('create_service.html',
                                        name=equipment.name,
                                        id=equipment.id)
            except KeyError:
                return '200 OK', 'Пока не добавлено никакого оборудования'


# контроллер создания категории
class CreateEquipment:
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            equipment_id = data.get('equipment_id')
            equipment = None
            if equipment_id:
                equipment = site.find_equipment_by_id(int(equipment_id))

            new_equipment = site.create_equipment(name, equipment)

            site.equipments.append(new_equipment)

            return '200 OK', render('index.html', objects_list=site.equipments)
        else:
            equipments = site.equipments
            return '200 OK', render('create_equipment.html',
                                    equipments=equipments)


# контроллер списка оборудования
class EquipmentList:
    def __call__(self, request):
        LOGGER.log('Список оборудования')
        return '200 OK', render('equipment_list.html',
                                objects_list=site.equipments)


# контроллер копирования сервиса
class CopyService:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_service = site.get_service(name)
            if old_service:
                new_name = f'copy_{name}'
                new_service = old_service.clone()
                new_service.name = new_name
                site.services.append(new_service)

            return '200 OK', render('service_list.html',
                                    objects_list=site.services,
                                    name=new_service.equipment.name)
        except KeyError:
            return '200 OK', 'Ни одного сервиса еще не добавлено'