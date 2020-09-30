from rest_framework import serializers
from . models import File,Interview,User,CommentsPYQ,CommentsExp,emailVerify
from rest_framework_jwt.settings import api_settings

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"

class interviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = "__all__"

class emailSerializer(serializers.ModelSerializer):
    class Meta:
        model = emailVerify
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        #fields = ('role','username',)

class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.role='Student'
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        # not changing the roll number (as it is a primary key) and role
        for (key, value) in validated_data.items():
            if key not in ['rollNumber','role']:
                setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

    class Meta:
        model = User
        fields = ('username','rollNumber','password','role','token','email')

class CommentsPYQSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsPYQ
        fields= "__all__"        

class CommentsExpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsExp
        fields= "__all__"                
