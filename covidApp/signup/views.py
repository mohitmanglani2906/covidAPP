from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher
from .models import Account
from .serializers import AccountSerializers
from .utils import checkIfUserExits, createJWTToken

class SignUpUser(APIView):
    def post(self,request):
        serializeUserData = AccountSerializers(data=request.data, context={'request': request})
        userExits  = checkIfUserExits(request.data["userEmail"])
        print("userExits___ %s", userExits)
        if userExits:
            return Response({"success": False, "message": "User account already exits!"})
        if serializeUserData.is_valid():
            data =  serializeUserData.validated_data
            bcrypt = BCryptSHA256PasswordHasher()
            new_password = bcrypt.encode(data["password"], bcrypt.salt())
            serializeUserData.save(password=new_password)
            return Response({"success":True, "message":"Account Created!"})
        return Response({"success":False, "message":"Something Went Wrong!"})


class LoginUser(APIView):
    def post(self, request):
        userEmail = request.data["userEmail"]
        password = request.data["password"]
        try:
            userEmailExits = Account.objects.get(userEmail=userEmail)
        except Exception as e:
            userEmailExits = None
        if userEmailExits is not None:
            bcrypt = BCryptSHA256PasswordHasher()
            if bcrypt.verify(password, userEmailExits.password) in ["True", "true", True]:
                jwt_token  = createJWTToken(userEmail)
                return Response({"success": True, "message": "You are Loggedin!", "token": jwt_token})
            else:
                return Response({"success": False, "message": "You are't authenticated!"})
        else:
            return Response({"success": True, "message": "User does not Exits!"})



