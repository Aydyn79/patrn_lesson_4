from datetime import date
from views import Index, About, Contact_us, CreateService, CreateEquipment, EquipmentList, CopyService, ServicesList


def add_date(request):
    request['date'] = date.today()


def add_key(request):
    request['key'] = '$S$C33783772bRXEx1aCsvY.dqgaaSu76XmVlKrW9Qu8IQlvxHlmzLf'


fronts = [add_date, add_key]

routes = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contact_us(),
    '/service_list/': ServicesList(),
    '/create_service/': CreateService(),
    '/create_equipment/': CreateEquipment(),
    '/equipment_list/': EquipmentList(),
    '/copy_service/': CopyService()
}
