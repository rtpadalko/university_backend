from rest_framework import serializers

from .models import *


class SpecializationSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, specialization):
        return specialization.image.url.replace("minio", "localhost", 1)
        
    class Meta:
        model = Specialization
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class ApplicantsSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(self, applicant):
        return applicant.owner.username

    def get_moderator(self, applicant):
        if applicant.moderator:
            return applicant.moderator.username

        return ""

    class Meta:
        model = Applicant
        fields = "__all__"


class ApplicantSerializer(serializers.ModelSerializer):
    specializations = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(self, applicant):
        return applicant.owner.username

    def get_moderator(self, applicant):
        return applicant.moderator.username if applicant.moderator else ""
    
    def get_specializations(self, applicant):
        items = SpecializationApplicant.objects.filter(applicant=applicant)
        return [{**SpecializationSerializer(item.specialization).data, "value": item.value} for item in items]
    
    class Meta:
        model = Applicant
        fields = "__all__"


class SpecializationApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecializationApplicant
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)