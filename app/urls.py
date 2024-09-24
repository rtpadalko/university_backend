from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('specializations/<int:specialization_id>/', specialization_details, name="specialization_details"),
    path('specializations/<int:specialization_id>/add_to_applicant/', add_specialization_to_draft_applicant, name="add_specialization_to_draft_applicant"),
    path('applicants/<int:applicant_id>/delete/', delete_applicant, name="delete_applicant"),
    path('applicants/<int:applicant_id>/', applicant)
]
