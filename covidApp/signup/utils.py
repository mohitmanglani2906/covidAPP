from .models import Account, UserToken
import jwt, datetime

def checkIfUserExits(userEmail):
    userData = Account.objects.filter(userEmail=userEmail)
    if userData:
        return True
    return False

def createJWTToken(userEmail):
    payload = {
        'email': userEmail
    }
    jwt_token = {'token': jwt.encode(payload, "COVID19API")}
    stringJWTToken = jwt_token["token"].decode('utf-8')
    try:
        userTokenObject = UserToken.objects.get(userEmail=userEmail)
    except:
        userTokenObject = None
    if userTokenObject:
        userTokenObject.token = stringJWTToken
        userTokenObject.lastUpdated = datetime.datetime.now()
        userTokenObject.save()
        print("User Token Exists")
    else:
        userTokenObject = UserToken()
        userTokenObject.token = stringJWTToken
        userTokenObject.userEmail = userEmail
        userTokenObject.save()
    return stringJWTToken
