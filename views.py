from frame.templator import render
from patterns.create_pattern import Engine,Logger
from patterns.struct_pattern import Debug, AppRoute

log = Logger()
site = Engine()

routes = {}

@AppRoute(routes, '/')
class Index:
    @Debug()
    def __call__(self, request):
        print(request)
        return '200 OK', render('index.html', objects_list=site.equipments, date=request.get('date', None))

@AppRoute(routes=routes, url='/about/')
class About:
    @Debug()
    def __call__(self, request):
        return '200 OK', render('page.html', date=request.get('date', None))

@AppRoute(routes=routes, url='/contacts/')
class Contact_us:
    def __call__(self, request):
        return '200 OK', render('contact.html', date=request.get('date', None))

# контроллер - список сервисов
@AppRoute(routes=routes, url='/service_list/')
class ServicesList:
    def __call__(self, request):
        log.log('Список видов сервисов')
        try:
            equipment = site.find_equipment_by_id(
                int(request['request_params']['id']))

            return '200 OK', render('service_list.html',
                                    objects_list=equipment.services,
                                    name=equipment.name, id=equipment.id)
        except KeyError:
            return '200 OK', 'Ни одного сервиса еще не добавлено'


# контроллер создания сервиса
@AppRoute(routes=routes, url='/create_service/')
class CreateService:
    equipment_id = -1
    @Debug()
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            log.log(name)

            equipment = None
            if self.equipment_id != -1:
                equipment = site.find_equipment_by_id(int(self.equipment_id))
                service = site.create_service('remote_support', name, equipment)
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
@AppRoute(routes=routes, url='/create_equipment/')
class CreateEquipment:
    @Debug()
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
            log.log(new_equipment.id)
            site.equipments.append(new_equipment)
            return '200 OK', render('index.html', objects_list=site.equipments)
        else:
            equipments = site.equipments
            return '200 OK', render('create_equipment.html',
                                    equipments=equipments)


# контроллер списка оборудования
@AppRoute(routes=routes, url='/equipment_list/')
class EquipmentList:
    @Debug()
    def __call__(self, request):
        print(site.equipments)
        return '200 OK', render('equipment_list.html',
                                objects_list=site.equipments)

    def show_list(self):
        for item in site.equipments:
            print(item.services_count())


# контроллер копирования сервиса
@AppRoute(routes=routes, url='/copy_service/')
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
#      _________________________________________________________________________________________     #
#  Здесь живет непеределанный код!!!

@AppRoute(routes=routes, url='/student-list/')
class CustomerListView(ListView):
    queryset = site.customers
    template_name = 'customer_list.html'


@AppRoute(routes=routes, url='/create-student/')
class CustomerCreateView(CreateView):
    template_name = 'customer_student.html'

    def create_customer(self, data: dict):
        name = data['name']
        # СДЕЛАТЬ ДОПОЛНИТЕЛЬНОЕ ПОЛЕ В БРАУЗЕРЕ ПОД РОЛЬ
        role = data['role']
        name = site.decode_value(name)
        role = site.decode_value(role)
        new_obj = site.create_user(role, name)
        site.customers.append(new_obj)


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()