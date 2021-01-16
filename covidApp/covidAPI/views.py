from rest_framework.views import APIView
from rest_framework.response import Response
import requests, datetime
from datetime import timedelta
import plotly.graph_objects as go
import base64, json
from .utils import sendCovidData
from signup.models import UserToken, Account

class AuthenticateFetchCovidData(APIView):

    currentUser = None
    userExists = False

    def processGET(self, request):
        pass

    def processPOST(self, request):
        pass

    def checkUserExistsWithToken(self, token):
        print("Token____ %s",token)
        userToken = None
        try:
            userToken =  UserToken.objects.get(token=token)
        except:
            userToken = None
        if userToken and userToken.userEmail:
            return True, userToken.userEmail
        return False, None

    def checkUserAuthentication(self):
        userExistsWithToken = False

        if self.request.headers and "Authorization" in self.request.headers and self.request.headers["Authorization"]:
            token = self.request.headers["Authorization"].replace("Bearer ", "")
            self.userExists, self.currentUser = self.checkUserExistsWithToken(token)

    def get(self, request):

        self.checkUserAuthentication()

        if self.userExists and self.currentUser:
            return Response(json.loads(self.processGET(request)))
        else:
            return  Response({"success": False, "message": "You are't authenticated!"})

    def post(self, request):

        self.checkUserAuthentication()

        if self.userExists and self.currentUser:
            return Response(json.loads(self.processPOST(request)))
        else:
            return Response({"success": False, "message": "You are't authenticated!"})

class FetchCovidData(AuthenticateFetchCovidData):

    def processGET(self, request):
        country = request.GET.get('country', None)
        startDate = request.GET.get('startDate', None)
        endDate = request.GET.get('endDate', None)

        try:
            if not endDate or not startDate:
                endDate = datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y')
                startDate = datetime.datetime.strftime(datetime.datetime.now() + timedelta(days=-14), '%d-%m-%Y')
            if not country:
                currentUser = self.currentUser
                try:
                    userObject = Account.objects.get(userEmail=currentUser)
                    if userObject and userObject.country:
                        country = userObject.country
                except:
                    userObject = None
                    return json.dumps({"success": False, "data": {}, "message": "Something went wrong."})

            startDateObj = datetime.datetime.strptime(startDate, '%d-%m-%Y').date()
            endDateObj = datetime.datetime.strptime(endDate, '%d-%m-%Y').date()

            generalResponse = json.loads(requests.get("https://corona-api.com/countries?include=timeline").content)
            countrySpecifiedJSON = {}
            newTimeLineJson = []
            if generalResponse and "data" in generalResponse:
                for GR in generalResponse["data"]:
                    if "name" in GR and GR["name"] and GR["name"] == country:
                        countrySpecifiedJSON = GR
                        for countryKey, countryValue in countrySpecifiedJSON.items():
                            print("__Keys___ %s", countryKey)
                            if countryKey == "timeline" and countryValue:
                                for time in countryValue:
                                    for timeKey, timeValue in time.items():
                                        if timeKey == "date" and timeValue:
                                            if datetime.datetime.strptime(timeValue,'%Y-%m-%d').date() >= startDateObj and datetime.datetime.strptime(timeValue, '%Y-%m-%d').date() <= endDateObj:
                                                newTimeLineJson.append(time)
                        if newTimeLineJson:
                            countrySpecifiedJSON["timeline"] = newTimeLineJson
                        else:
                            countrySpecifiedJSON["timeline"] = []

            return json.dumps({"success": True, "data": countrySpecifiedJSON})

        except Exception as e:
            print(e)
            return json.dumps({"success": False, "data": {}, "message": "Something went wrong."})

    def processPOST(self, request):

        try:
            generalResponse = json.loads(requests.get("https://corona-api.com/countries").content)
            countries = []
            calculatedData = []
            print("Total___ %s", len(generalResponse["data"]))
            for GR in generalResponse["data"]:
                if "latest_data" in GR and GR["latest_data"]:
                    print("_Country__ %s", GR["name"])
                    if "calculated" in GR["latest_data"] and GR["latest_data"]["calculated"] and "cases_per_million_population" in GR["latest_data"]["calculated"] and GR["latest_data"]["calculated"]["cases_per_million_population"]:
                        calculatedData.append(GR["latest_data"]["calculated"]["cases_per_million_population"])
                        if "name" in GR and GR["name"]:
                            countries.append(GR["name"])
            print(countries)
            print(len(countries))
            print(calculatedData)
            print(len(calculatedData))
            fig = go.Figure([
                go.Bar(name="Cases per million population", x = countries, y=calculatedData)
            ])
            fig.update_layout(title_text='Covid19 API Data')
            sendCovidData(self.currentUser, base64.b64encode(fig.to_image(format="png")).decode())

            return json.dumps({"success": True, "message": "Image exported successfully"})

        except Exception as e:
            print(e)
            return json.dumps({"success": False, "message": "Image not exported successfully"})
