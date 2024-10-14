import random

from django.core.management.base import BaseCommand
from minio import Minio

from ...models import *
from .utils import random_date, random_timedelta


def add_users():
    User.objects.create_user("user", "user@user.com", "1234", first_name="user", last_name="user")
    User.objects.create_superuser("root", "root@root.com", "1234", first_name="root", last_name="root")

    for i in range(1, 10):
        User.objects.create_user(f"user{i}", f"user{i}@user.com", "1234", first_name=f"user{i}", last_name=f"user{i}")
        User.objects.create_superuser(f"root{i}", f"root{i}@root.com", "1234", first_name=f"user{i}", last_name=f"user{i}")

    print("Пользователи созданы")


def add_specializations():
    Specialization.objects.create(
        name="ИУ4",
        description="Кафедра ИУ4 'Проектирование и технология производства электронной аппаратуры' осуществляет обучение по направлению, сочетающему в себе решение задач в областях конструирования, технологии производства и сквозной цифровизации промышленности. Основное внимание уделяется проведению сквозного (комплексного) схемотехнического, конструкторского и технологического проектирования электронной аппаратуры при активном использовании автоматизированных средств.",
        budget_place=66,
        budget_passing_score=239,
        paid_place=35,
        space_time=28654,
        image="1.png"
    )

    Specialization.objects.create(
        name="ИУ5",
        description="Системы обработки данных – это комплекс взаимодействующих методов и средств сбора и обработки электронной информации, необходимых для управления объектами с помощью электронно-вычислительных машин (ЭВМ) и других средств информационной техники.",
        budget_place=75,
        budget_passing_score=296,
        paid_place=81,
        space_time=329761,
        image="2.png"
    )

    Specialization.objects.create(
        name="ИУ8",
        description="Информационная безопасность — практика предотвращения несанкционированного доступа, использования, раскрытия, искажения, изменения, исследования, записи или уничтожения информации.",
        budget_place=59,
        budget_passing_score=281,
        paid_place=55,
        space_time=306347,
        image="3.png"
    )

    Specialization.objects.create(
        name="РК9",
        description="Кафедра занимается спектром технологий, которые являются составными частями концепции «Индустрия 4.0». Решаются задачи разработки интегрированных систем компьютерной автоматизации производственных процессов на разных уровнях, от станков с ЧПУ до интеллектуальных систем управления производством.",
        budget_place=48,
        budget_passing_score=260,
        paid_place=60,
        space_time=254823,
        image="4.png"
    )

    Specialization.objects.create(
        name="МТ4",
        description="Кафедра «Метрология и взаимозаменяемость», созданная в 1931 г., осуществляет подготовку бакалавров по профилю «Метрология и метрологическое обеспечение». Магистерская программа «Метрология и метрологическое обеспечение».",
        budget_place=66,
        budget_passing_score=239,
        paid_place=35,
        space_time=28654,
        image="5.png"
    )

    Specialization.objects.create(
        name="СМ1",
        description="Данное направление специализируется на управляемых баллистических ракетах на твердом топливе и развертываемых космических конструкциях. Ведущее место в учебной и научной работе кафедры занимают вопросы динамики и прочности конструкций. Только представь, какой высокой квалификации должны быть специалисты, отвечающие за такую ответственную задачу!",
        budget_place=60,
        budget_passing_score=195,
        paid_place=15,
        space_time=105632,
        image="6.png"
    )

    client = Minio("minio:9000", "minio", "minio123", secure=False)
    client.fput_object('images', '1.png', "app/static/images/1.png")
    client.fput_object('images', '2.png', "app/static/images/2.png")
    client.fput_object('images', '3.png', "app/static/images/3.png")
    client.fput_object('images', '4.png', "app/static/images/4.png")
    client.fput_object('images', '5.png', "app/static/images/5.png")
    client.fput_object('images', '6.png', "app/static/images/6.png")
    client.fput_object('images', 'default.png', "app/static/images/default.png")

    print("Услуги добавлены")


def add_applicants():
    users = User.objects.filter(is_superuser=False)
    moderators = User.objects.filter(is_superuser=True)

    if len(users) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    specializations = Specialization.objects.all()

    for _ in range(30):
        status = random.randint(2, 5)
        add_applicant(status, specializations, users, moderators)

    add_applicant(1, specializations, users, moderators)

    print("Заявки добавлены")


def add_applicant(status, specializations, users, moderators):
    applicant = Applicant.objects.create()
    applicant.status = status

    if applicant.status in [3, 4]:
        applicant.date_complete = random_date()
        applicant.date_formation = applicant.date_complete - random_timedelta()
        applicant.date_created = applicant.date_formation - random_timedelta()
    else:
        applicant.date_formation = random_date()
        applicant.date_created = applicant.date_formation - random_timedelta()

    applicant.owner = random.choice(users)
    applicant.moderator = random.choice(moderators)

    applicant.name = "Макаров Сергей Владимирович"
    applicant.birthday_date = 2004

    priority = 1
    for specialization in random.sample(list(specializations), 3):
        item = SpecializationApplicant(
            applicant=applicant,
            specialization=specialization,
            value=priority
        )
        item.save()
        priority += 1

    applicant.save()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()
        add_specializations()
        add_applicants()

