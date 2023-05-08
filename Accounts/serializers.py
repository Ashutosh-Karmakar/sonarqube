from rest_framework import serializers
from .models import NewUser

#here we just need to add the fields required for registeration that can be brought from the api
#we need to overide the save method of the modelserializer class
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields=['email','username','password']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    def save(self):
        account = NewUser(
            email = self.validated_data['email'],
            username = self.validated_data['username']
        )
        password = self.validated_data['password']
        account.set_password(password)
        account.save()
        return account