from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Account
from .serializers import AccountSerializers
from .utils import checkIfUserExits

# Create your views here.

class SignUpUser(APIView):
    def post(self,request):
        serializeUserData = AccountSerializers(data=request.data, context={'request': request})
        userExits  = checkIfUserExits(request.data["userEmail"])
        print("userExits___ %s", userExits)
        if userExits:
            return Response({"success": False, "message": "User account already exits!"})
        if serializeUserData.is_valid():
            serializeUserData.save()
            return Response({"success":True, "message":"Account Created!"})
        return Response({"success":False, "message":"Something Went Wrong!"})


class LoginUser(APIView):
    def post(self, request):
        userEmail = request.data["userEmail"]
        password = request.data["password"]
        userEmailExits = Account.objects.get(userEmail=userEmail)
        if userEmailExits is not None:
            userEmailPassword = Account.objects.get(password=password)
            print("userEmailPassword__%s", userEmailPassword)
            if userEmailPassword is not None:
                return Response({"success": True, "message": "You are Loggedin!"})
            else:
                return Response({"success": False, "message": "You are't authenticated!"})
        else:
            return Response({"success": True, "message": "User does not Exits!"})



