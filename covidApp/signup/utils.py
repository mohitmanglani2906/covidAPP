from .serializers import AccountSerializers
from .models import Account

def checkIfUserExits(userEmail):
    userData = Account.objects.filter(userEmail=userEmail)
    if userData:
        return True
    return False
