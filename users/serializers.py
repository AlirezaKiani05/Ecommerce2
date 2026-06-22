from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Country,Profile
User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    country_name = serializers.CharField(source='country.name', read_only=True)

    class Meta:
        model = Profile
        
        fields = ['username', 'email', 'phone_number', 'country_name', 'avatar']
        
        


class RegisterSerializer(serializers.ModelSerializer):
    
    phone_number = serializers.CharField(
        write_only=True, 
        required=True,
        validators=[
            RegexValidator(
                regex=r'^989\d{9}$',
                message="Phone number must start with 989 and be exactly 12 digits long (e.g., 989123456789)."

            )
        ]
    )
    
    
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[MinLengthValidator(8, message="Must be at least 8 characters.")]
    )
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), 
        write_only=True, 
        required=False
    )
    
    username = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message="Username can only contain English letters, numbers, and underscores."
            )
        ]
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone_number', 'country']

    
    def validate_password(self, value):
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one number.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        phone_number = validated_data.pop('phone_number', None)
        country_obj = validated_data.pop('country', None)
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()


        profile = user.profile
        if phone_number:
            profile.phone_number = phone_number
        if country_obj:
            profile.country = country_obj
        
        profile.save()

        return user

 
# class RegisterSerializer(serializers.ModelSerializer):

#     email = serializers.EmailField(required=True,
#                                    validators=[UniqueValidator(
#                                        queryset=User.objects.all())]
#                                    )
#     password_1 = serializers.CharField(required=True, write_only=True)
#     password_2 = serializers.CharField(required=True, write_only=True)

#     class Meta:
#         model = User
#         fields = ('email', 'username', 'first_name',
#                   'last_name', 'password_1', 'password_2')
#         extra_kwargs = {
#             'first_name': {'required': False},
#             'last_name': {'required': False}
#         }

#     def validate(self, attrs):
#         if attrs['password_1'] != attrs['password_2']:
#             raise serializers.ValidationError({
#                 'password': 'Passwords did not match.'
#             })
#         return super().validate(attrs)

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data.get('first_name', ''),
#             last_name=validated_data.get('last_name', ''),
#             password=validated_data['password_1']
#         )
#         return user    
