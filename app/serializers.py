from rest_framework import serializers

from .models import *


class SpecializationSerializer(serializers.ModelSerializer):
    def get_image(self, specialization):
        return specialization.image.url.replace("minio", "localhost", 1)

    class Meta:
        model = Specialization
        fields = "__all__"


class ApplicantSerializer(serializers.ModelSerializer):
    specializations = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(self, applicant):
        return applicant.owner.username

    def get_moderator(self, applicant):
        if applicant.moderator:
            return applicant.moderator.username
            
    def get_specializations(self, applicant):
        items = SpecializationApplicant.objects.filter(applicant=applicant)
        serializer = SpecializationSerializer([item.specialization for item in items], many=True)
        return serializer.data

    class Meta:
        model = Applicant
        fields = '__all__'


class ApplicantsSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(self, applicant):
        return applicant.owner.username

    def get_moderator(self, applicant):
        if applicant.moderator:
            return applicant.moderator.username

    class Meta:
        model = Applicant
        fields = "__all__"


class SpecializationApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecializationApplicant
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'date_joined', 'password', 'username')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'username')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
