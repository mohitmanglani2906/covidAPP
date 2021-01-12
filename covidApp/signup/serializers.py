from rest_framework_mongoengine import serializers
from .models import Account

class AccountSerializers(serializers.DocumentSerializer):
    class Meta:
        model = Account
        fields = '__all__'