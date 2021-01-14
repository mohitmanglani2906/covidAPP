from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests,json, datetime
from datetime import timedelta
import plotly.graph_objects as go
import base64
from .utils import sendCovidData

class FetchCovidData(APIView):

    def get(self, request):
        country = request.GET.get('country', None)
        startDate = request.GET.get('startDate', None)
        endDate = request.GET.get('endDate', None)

        try:
            if not endDate or not startDate:
                endDate = datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y')
                startDate = datetime.datetime.strftime(datetime.datetime.now() + timedelta(days=-14), '%d-%m-%Y')
            if not country:
                country = "Brazil"
            startDateObj = datetime.datetime.strptime(startDate, '%d-%m-%Y').date()
            endDateObj = datetime.datetime.strptime(endDate, '%d-%m-%Y').date()
            print(startDateObj)
            print(endDateObj)
            generalResponse = json.loads(requests.get("https://corona-api.com/countries?include=timeline").content)
            countrySpecifiedJSON = {}
            newTimeLineJson = []
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
            print("____________________________++++++++++++++++++++++++++++++++++++++++++++++++_________________________%s",countrySpecifiedJSON)
            return Response({"success": True, "data": countrySpecifiedJSON})

        except Exception as e:
            print(e)
            return Response({"success": False, "data": {}, "message":"Something went wrong."})

    def post(self, request):

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
            sendCovidData("16itmohit.manglani@gmail.com", base64.b64encode(fig.to_image(format="png")).decode())

            return Response({"success": True, "message": "Image exported successfully"})

        except Exception as e:
            print(e)
            return Response({"success": False, "message": "Image not exported successfully"})
