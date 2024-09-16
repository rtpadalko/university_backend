from django.shortcuts import render

specializations = [
    {
        "id": 1,
        "name": "ИУ4",
        "description": 'Кафедра ИУ4 "Проектирование и технология производства электронной аппаратуры" осуществляет обучение по направлению, сочетающему в себе решение задач в областях конструирования, технологии производства и сквозной цифровизации промышленности. Основное внимание уделяется проведению сквозного (комплексного) схемотехнического, конструкторского и технологического проектирования электронной аппаратуры при активном использовании автоматизированных средств.',
        "budget_place": 66,
        "budget_passing_score": 239,
        "paid_place": 35,
        "price": 28654,
        "image": "http://localhost:9000/images/1.png"
    },
    {
        "id": 2,
        "name": "ИУ5",
        "description": "Системы обработки данных – это комплекс взаимодействующих методов и средств сбора и обработки электронной информации, необходимых для управления объектами с помощью электронно-вычислительных машин (ЭВМ) и других средств информационной техники.",
        "budget_place": 75,
        "budget_passing_score": 296,
        "paid_place": 81,
        "price": 329761,
        "image": "http://localhost:9000/images/2.png"
    },
    {
        "id": 3,
        "name": "ИУ8",
        "description": "Информационная безопасность — практика предотвращения несанкционированного доступа, использования, раскрытия, искажения, изменения, исследования, записи или уничтожения информации",
        "budget_place": 59,
        "budget_passing_score": 281,
        "paid_place": 55,
        "price": 306347,
        "image": "http://localhost:9000/images/3.png"
    },
    {
        "id": 4,
        "name": "РК9",
        "description": "Кафедра занимается спектром технологий, которые являются составными частями концепции «Индустрия 4.0». Решаются задачи разработки интегрированных систем компьютерной автоматизации производственных процессов на разных уровнях, от станков с ЧПУ до интеллектуальных систем управления производством.",
        "budget_place": 48,
        "budget_passing_score": 260,
        "paid_place": 60,
        "price": 254823,
        "image": "http://localhost:9000/images/4.png"
    },
    {
        "id": 5,
        "name": "МТ4",
        "description": "Кафедра «Метрология и взаимозаменяемость», созданная в 1931 г., осуществляет подготовку бакалавров по профилю «Метрология и метрологическое обеспечение». Магистерская программа «Метрология и метрологическое обеспечение».",
        "budget_place": 22,
        "budget_passing_score": 211,
        "paid_place": 5,
        "price": 164834,
        "image": "http://localhost:9000/images/5.png"
    },
    {
        "id": 6,
        "name": "СМ1",
        "description": "Данное направление специализируется на управляемых баллистических ракетах на твердом топливе и развертываемых космических конструкциях. Ведущее место в учебной и научной работе кафедры занимают вопросы динамики и прочности конструкций. Только представь, какой высокой квалификации должны быть специалисты, отвечающие за такую ответственную задачу!",
        "budget_place": 60,
        "budget_passing_score": 195,
        "paid_place": 15,
        "price": 105632,
        "image": "http://localhost:9000/images/6.png"
    }
]

draft_order = {
    "id": 123,
    "status": "Черновик",
    "date_created": "14 сентября 2024г",
    "specializations": [
        {
            "id": 1,
            "name": "ИУ4",
            "description": "Кафедра ИУ4 'Проектирование и технология производства электронной аппаратуры' осуществляет обучение по направлению, сочетающему в себе решение задач в областях конструирования, технологии производства и сквозной цифровизации промышленности. Основное внимание уделяется проведению сквозного (комплексного) схемотехнического, конструкторского и технологического проектирования электронной аппаратуры при активном использовании автоматизированных средств.",
            "budget_place": 66,
            "budget_passing_score": 239,
            "paid_place": 35,
            "price": 28654,
            "image": "http://localhost:9000/images/1.png",
            "priority": 2
        },
        {
            "id": 2,
            "name": "ИУ5",
             "description": "Системы обработки данных – это комплекс взаимодействующих методов и средств сбора и обработки электронной информации, необходимых для управления объектами с помощью электронно-вычислительных машин (ЭВМ) и других средств информационной техники.",
            "budget_place": 75,
            "budget_passing_score": 296,
            "paid_place": 81,
            "price": 329761,
            "image": "http://localhost:9000/images/2.png",
            "priority": 1
        },
        {
            "id": 3,
            "name": "ИУ8",
            "description": "Информационная безопасность — практика предотвращения несанкционированного доступа, использования, раскрытия, искажения, изменения, исследования, записи или уничтожения информации",
            "budget_place": 59,
            "budget_passing_score": 281,
            "paid_place": 55,
            "price": 306347,
            "image": "http://localhost:9000/images/3.png",
            "priority": 3
        }
    ]
}


def getSpecializationById(specialization_id):
    for specialization in specializations:
        if specialization["id"] == specialization_id:
            return specialization


def searchSpecializations(specialization_name):
    res = []

    for specialization in specializations:
        if specialization_name.lower() in specialization["name"].lower():
            res.append(specialization)

    return res


def getDraftOrder():
    return draft_order


def getOrderById(order_id):
    return draft_order


def index(request):
    name = request.GET.get("name", "")
    specializations = searchSpecializations(name)
    draft_order = getDraftOrder()

    context = {
        "specializations": specializations,
        "name": name,
        "specializations_count": len(draft_order["specializations"]),
        "draft_order": draft_order
    }

    return render(request, "home_page.html", context)


def specialization(request, specialization_id):
    context = {
        "id": specialization_id,
        "specialization": getSpecializationById(specialization_id),
    }

    return render(request, "specialization_page.html", context)


def order(request, order_id):
    context = {
        "order": getOrderById(order_id),
    }

    return render(request, "order_page.html", context)
