from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect
from django.utils import timezone

from app.models import Specialization, Applicant, SpecializationApplicant


def index(request):
    specialization_name = request.GET.get("specialization_name", "")
    specializations = Specialization.objects.filter(status=1)

    if specialization_name:
        specializations = specializations.filter(name__icontains=specialization_name)

    draft_applicant = get_draft_applicant()

    context = {
        "specialization_name": specialization_name,
        "specializations": specializations
    }

    if draft_applicant:
        context["specializations_count"] = len(draft_applicant.get_specializations())
        context["draft_applicant"] = draft_applicant

    return render(request, "home_page.html", context)


def add_specialization_to_draft_applicant(request, specialization_id):
    specialization = Specialization.objects.get(pk=specialization_id)

    draft_applicant = get_draft_applicant()

    if draft_applicant is None:
        draft_applicant = Applicant.objects.create()
        draft_applicant.owner = get_current_user()
        draft_applicant.date_created = timezone.now()
        draft_applicant.save()

    if SpecializationApplicant.objects.filter(applicant=draft_applicant, specialization=specialization).exists():
        return redirect("/")

    item = SpecializationApplicant(
        applicant=draft_applicant,
        specialization=specialization
    )
    item.save()

    return redirect("/")


def specialization_details(request, specialization_id):
    context = {
        "specialization": Specialization.objects.get(id=specialization_id)
    }

    return render(request, "specialization_page.html", context)


def delete_applicant(request, applicant_id):
    if not Applicant.objects.filter(pk=applicant_id).exists():
        return redirect("/")

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM specialization_applicant WHERE applicant_id = %s", [applicant_id])
        cursor.execute("DELETE FROM applicants WHERE id = %s", [applicant_id])

    return redirect("/")


def applicant(request, applicant_id):
    if not Applicant.objects.filter(pk=applicant_id).exists():
        return redirect("/")

    context = {
        "applicant": Applicant.objects.get(id=applicant_id),
    }

    return render(request, "applicant_page.html", context)


def get_draft_applicant():
    return Applicant.objects.filter(status=1).first()


def get_current_user():
    return User.objects.filter(is_superuser=False).first()