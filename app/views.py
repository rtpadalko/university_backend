from django.contrib.auth import authenticate
from django.utils.dateparse import parse_datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import *
from .permissions import *
from .serializers import *
from .utils import identity_user


def get_draft_applicant(request):
    user = identity_user(request)

    print(user)

    if user is None:
        return None


    applicant = Applicant.objects.filter(owner=user).filter(status=1).first()

    return applicant


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'query',
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING
        )
    ]
)
@api_view(["GET"])
def search_specializations(request):
    query = request.GET.get("query", "")

    specialization = Specialization.objects.filter(status=1).filter(name__icontains=query)

    serializer = SpecializationSerializer(specialization, many=True)

    draft_applicant = get_draft_applicant(request)

    resp = {
        "specializations": serializer.data,
        "specializations_count": SpecializationApplicant.objects.filter(applicant=draft_applicant).count() if draft_applicant else None,
        "draft_applicant_id": draft_applicant.pk if draft_applicant else None
    }

    return Response(resp)


@api_view(["GET"])
def get_specialization_by_id(request, specialization_id):
    if not Specialization.objects.filter(pk=specialization_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    specialization = Specialization.objects.get(pk=specialization_id)
    serializer = SpecializationSerializer(specialization, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_specialization(request, specialization_id):
    if not Specialization.objects.filter(pk=specialization_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    specialization = Specialization.objects.get(pk=specialization_id)

    image = request.data.get("image")
    if image is not None:
        specialization.image = image
        specialization.save()

    serializer = SpecializationSerializer(specialization, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_specialization(request):
    specialization = Specialization.objects.create()

    serializer = SpecializationSerializer(specialization)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsModerator])
def delete_specialization(request, specialization_id):
    if not Specialization.objects.filter(pk=specialization_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    specialization = Specialization.objects.get(pk=specialization_id)
    specialization.status = 2
    specialization.save()

    specialization = Specialization.objects.filter(status=1)
    serializer = SpecializationSerializer(specialization, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_specialization_to_applicant(request, specialization_id):
    if not Specialization.objects.filter(pk=specialization_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    specialization = Specialization.objects.get(pk=specialization_id)

    draft_applicant = get_draft_applicant(request)

    if draft_applicant is None:
        draft_applicant = Applicant.objects.create()
        draft_applicant.date_created = timezone.now()
        draft_applicant.owner = identity_user(request)
        draft_applicant.save()

    if SpecializationApplicant.objects.filter(applicant=draft_applicant, specialization=specialization).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    item = SpecializationApplicant.objects.create()
    item.applicant = draft_applicant
    item.specialization = specialization
    item.save()

    serializer = ApplicantSerializer(draft_applicant)
    return Response(serializer.data["specializations"])


@api_view(["POST"])
@permission_classes([IsModerator])
def update_specialization_image(request, specialization_id):
    if not Specialization.objects.filter(pk=specialization_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    specialization = Specialization.objects.get(pk=specialization_id)

    image = request.data.get("image")
    if image is not None:
        specialization.image = image
        specialization.save()

    serializer = SpecializationSerializer(specialization)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_applicants(request):
    status_id = int(request.GET.get("status", 0))
    date_formation_start = request.GET.get("date_formation_start")
    date_formation_end = request.GET.get("date_formation_end")

    applicants = Applicant.objects.exclude(status__in=[1, 5])

    user = identity_user(request)
    if not user.is_staff:
        applicants = applicants.filter(owner=user)

    if status_id > 0:
        applicants = applicants.filter(status=status_id)

    if date_formation_start and parse_datetime(date_formation_start):
        applicants = applicants.filter(date_formation__gte=parse_datetime(date_formation_start))

    if date_formation_end and parse_datetime(date_formation_end):
        applicants = applicants.filter(date_formation__lt=parse_datetime(date_formation_end))

    serializer = ApplicantsSerializer(applicants, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_applicant_by_id(request, applicant_id):
    user = identity_user(request)

    if not Applicant.objects.filter(pk=applicant_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    applicant = Applicant.objects.get(pk=applicant_id)
    serializer = ApplicantSerializer(applicant, many=False)

    return Response(serializer.data)


@swagger_auto_schema(method='put', request_body=ApplicantSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_applicant(request, applicant_id):
    user = identity_user(request)

    if not Applicant.objects.filter(pk=applicant_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    applicant = Applicant.objects.get(pk=applicant_id)
    serializer = ApplicantSerializer(applicant, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, applicant_id):
    user = identity_user(request)

    if not Applicant.objects.filter(pk=applicant_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    applicant = Applicant.objects.get(pk=applicant_id)

    applicant.status = 2
    applicant.date_formation = timezone.now()
    applicant.save()

    serializer = ApplicantSerializer(applicant, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, applicant_id):
    if not Applicant.objects.filter(pk=applicant_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    applicant = Applicant.objects.get(pk=applicant_id)

    if applicant.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    applicant.status = request_status
    applicant.date_complete = timezone.now()
    applicant.moderator = identity_user(request)
    applicant.save()

    serializer = ApplicantSerializer(applicant, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_applicant(request, applicant_id):
    user = identity_user(request)

    if not Applicant.objects.filter(pk=applicant_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    applicant = Applicant.objects.get(pk=applicant_id)

    if applicant.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    applicant.status = 5
    applicant.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_specialization_from_applicant(request, applicant_id, specialization_id):
    user = identity_user(request)

    if not Applicant.objects.filter(pk=applicant_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not SpecializationApplicant.objects.filter(applicant_id=applicant_id, specialization_id=specialization_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = SpecializationApplicant.objects.get(applicant_id=applicant_id, specialization_id=specialization_id)
    item.delete()

    applicant = Applicant.objects.get(pk=applicant_id)

    serializer = ApplicantSerializer(applicant, many=False)
    specializations = serializer.data["specializations"]

    if len(specializations) == 0:
        applicant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(specializations)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_specialization_applicant(request, applicant_id, specialization_id):
    user = identity_user(request)

    if not Applicant.objects.filter(pk=applicant_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not SpecializationApplicant.objects.filter(specialization_id=specialization_id, applicant_id=applicant_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = SpecializationApplicant.objects.get(specialization_id=specialization_id, applicant_id=applicant_id)

    serializer = SpecializationApplicantSerializer(item, many=False)

    return Response(serializer.data)


@swagger_auto_schema(method='PUT', request_body=SpecializationApplicantSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_specialization_in_applicant(request, applicant_id, specialization_id):
    user = identity_user(request)

    if not Applicant.objects.filter(pk=applicant_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not SpecializationApplicant.objects.filter(specialization_id=specialization_id, applicant_id=applicant_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = SpecializationApplicant.objects.get(specialization_id=specialization_id, applicant_id=applicant_id)

    serializer = SpecializationApplicantSerializer(item, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    serializer = UserSerializer(user)

    response = Response(serializer.data, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=True)

    return response


@swagger_auto_schema(method='post', request_body=UserRegisterSerializer)
@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    serializer = UserSerializer(user)

    response = Response(serializer.data, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=True)

    return response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, settings.JWT["ACCESS_TOKEN_LIFETIME"])

    return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(method='PUT', request_body=UserSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    if not User.objects.filter(pk=user_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = identity_user(request)

    if user.pk != user_id:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, many=False, partial=True)
    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)
