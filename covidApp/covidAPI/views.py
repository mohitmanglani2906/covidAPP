from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests,json, datetime
from datetime import timedelta
import plotly.graph_objects as go
# Create your views here.

class FetchCovidData(APIView):

    def get(self, request):
        country = request.GET.get('country', None)
        startDate = request.GET.get('startDate', None)
        endDate = request.GET.get('endDate', None)

        try:
            if not endDate or not startDate:
                endDate = datetime.datetime.strftime(datetime.datetime.now().date(), '%d-%m-%Y')
                startDate = datetime.datetime.strftime(datetime.datetime.now().date() + timedelta(days=-14), '%d-%m-%Y')
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
                                        if datetime.datetime.strptime(timeValue,
                                                                      '%Y-%m-%d').date() >= startDateObj and datetime.datetime.strptime(
                                                timeValue, '%Y-%m-%d').date() <= endDateObj:
                                            print("timeValue____________ %s", timeValue)
                                            newTimeLineJson.append(time)
                    if newTimeLineJson:
                        countrySpecifiedJSON["timeline"] = newTimeLineJson
                    else:
                        countrySpecifiedJSON["timeline"] = []
            print("____________________________++++++++++++++++++++++++++++++++++++++++++++++++_________________________%s",countrySpecifiedJSON)
            return Response({"success": True, "data": countrySpecifiedJSON})

        except Exception as e:
            print(e)
            return Response({"success": False, "data": {}})

    def post(self, request):

        try:
            generalResponse = json.loads(requests.get("https://corona-api.com/countries").content)
            # print("generalResponse___ %s", generalResponse)
            # countries = ['Afghanistan', 'Albania', 'Åland Islands', 'American Samoa', 'Algeria', 'Andorra', 'Angola', 'Anguilla', 'Antigua and Barbuda', 'Antarctica', 'Australia', 'Austria', 'Bahrain', 'Bangladesh', 'Benin', 'Belize', 'Argentina', 'Armenia', 'Bosnia and Herzegovina', 'Aruba', 'Azerbaijan', 'Bahamas', 'Brunei ', 'Bonaire, Sint Eustatius and Saba', 'Belarus', 'Barbados', 'British Indian Ocean Territory', 'Bermuda', 'Belgium', 'Cameroon', 'Bhutan', 'Bolivia', 'Cambodia', 'CAR', 'Botswana', 'Chad', 'Bulgaria', 'Bouvet Island', 'Brazil', 'Cocos (Keeling) Islands', 'Colombia', 'Canada', 'Burkina Faso', 'Burundi', 'Costa Rica', 'Cape Verde', 'Cayman Islands', 'Cook Islands', 'China', 'Curaçao', 'Cyprus', 'Christmas Island', 'Chile', 'Dominican Republic', 'Comoros', 'Congo', 'DRC', 'Dominica', 'Equatorial Guinea', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Eritrea', 'Czechia', 'Denmark', 'Djibouti', 'Fiji', 'Faroe Islands', 'El Salvador', 'Egypt', 'French Southern Territories', 'French Polynesia', 'Ecuador', 'Ghana', 'Estonia', 'Ethiopia', 'Germany', 'Falkland Islands', 'Finland', 'Grenada', 'France', 'Guadeloupe', 'Gabon', 'French Guiana', 'Guinea', 'Gambia', 'Guinea-Bissau', 'Honduras', 'Gibraltar', 'Georgia', 'Greece', 'Greenland', 'Vatican City', 'Guatemala', 'Indonesia', 'Guernsey', 'India', 'Guam', 'Isle of Man', 'Israel', 'Guyana', 'Hong Kong', 'Haiti', 'Heard Island and McDonald Islands', 'Jersey', 'Hungary', 'Iceland', 'Iran', 'Iraq', 'Ireland', 'Italy', 'Jamaica', 'Japan', "Korea, Democratic People's Republic of", 'Latvia', 'Liechtenstein', 'Madagascar', 'Malta', 'Mayotte', 'Mongolia', 'Myanmar', 'New Caledonia', 'Niue', 'Jordan', 'S. Korea', 'Lebanon', 'Lithuania', 'Malawi', 'Marshall Islands', 'Kenya', 'Mexico', 'Kyrgyzstan', 'Montenegro', 'Kiribati', 'Liberia', 'Laos', 'Macao', 'Libya', 'Maldives', 'North Macedonia', 'Mauritania', 'Mali', 'Mauritius', 'Namibia', 'Pakistan', 'Moldova', 'New Zealand', 'Morocco', 'Norfolk Island', 'Nepal', 'Paraguay', 'Niger', 'Monaco', 'Mozambique', 'Netherlands', 'Norway', 'Nigeria', 'Portugal', 'Oman', 'Russia', 'Saint Lucia', 'San Marino', 'Palau', 'Seychelles', 'Peru', 'Slovenia', 'Puerto Rico', 'South Sudan', 'Rwanda', 'Svalbard and Jan Mayen', 'Saint Martin', 'Taiwan', 'Sao Tome and Principe', 'Togo', 'Sierra Leone', 'Turkey', 'Solomon Islands', 'Ukraine', 'Spain', 'Uruguay', 'Swaziland', 'British Virgin Islands', 'Tajikistan', 'Tokelau', 'Turkmenistan', 'United Arab Emirates', 'Uzbekistan', 'U.S. Virgin Islands', 'Zimbabwe', 'Kazakhstan', 'Kuwait', 'Lesotho', 'Luxembourg', 'Malaysia', 'Martinique', 'Micronesia, Federated States of', 'Montserrat', 'Nauru', 'Nicaragua', 'Northern Mariana Islands', 'Panama', 'Pitcairn', 'Réunion', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Vincent Grenadines', 'Senegal', 'Sint Maarten', 'South Africa', 'Sudan', 'Switzerland', 'Thailand', 'Trinidad and Tobago', 'Tuvalu', 'USA', 'Venezuela', 'Papua New Guinea', 'Poland', 'Romania', 'Saint Kitts and Nevis', 'Samoa', 'Serbia', 'Slovakia', 'South Georgia and the South Sandwich Islands', 'Suriname', 'Syria', 'Timor-Leste', 'Tunisia', 'Uganda', 'United States Minor Outlying Islands', 'Vietnam', 'Palestine', 'Philippines', 'Qatar', 'Saint Barth', 'Saint Pierre Miquelon', 'Saudi Arabia', 'Singapore', 'Somalia', 'Sri Lanka', 'Sweden', 'Tanzania', 'Tonga', 'Turks and Caicos', 'UK', 'Vanuatu', 'Wallis and Futuna', 'Zambia', 'Western Sahara', 'Yemen']
            # activeCase = [53584, 63971, 102369, 8586, 18254, 15, 176, 28614, 382258, 95879, 523302, 3363, 11332, 1730921, 162288, 115633, 6068, 224827, 8004, 173, 213993, 884, 656, 664263, 26848, 825, 173896, 392, 4973, 16768, 2589, 209131, 8133833, 1801903, 668193, 8279, 1019, 180061, 362, 87536, 4464, 27638, 645892, 183282, 1150, 7127, 19496, 109, 5296, 220223, 15007, 1556, 835454, 182725, 5877, 53, 48905, 150753, 17340, 221506, 56230, 33805, 128616, 1941119, 29, 38790, 132, 2786838, 8776, 9740, 14221, 13980, 3857, 2478, 127945, 3240, 239780, 145179, 29, 27, 143243, 836718, 10479879, 32, 403, 501073, 6588, 9284, 10386, 343656, 5898, 1292614, 603739, 152539, 2289021, 13637, 286752, 49899, 2346, 18001, 14529, 6232, 1442, 131186, 40, 308670, 69114, 222391, 160446, 9027, 4, 98334, 1534039, 82380, 52819, 1779, 41, 46, 105378, 14159, 86597, 15611, 7664, 539, 28602, 504293, 149662, 2222, 452988, 265268, 116535, 3924, 1070, 22334, 878263, 55903, 101331, 489293, 130780, 3425269, 462, 2628, 583, 1037350, 139713, 39, 3662, 9784, 1025, 834, 1066, 3978, 2834, 2336476, 17, 1119314, 2111782, 26901, 114, 13308, 77611, 17, 22297, 163019, 154841, 5937, 48027, 138224, 6184, 13, 6097, 279196, 9359, 21533, 1555, 1246643, 23316, 484506, 10547, 7273, 23123096, 116983, 819, 1390385, 673271, 34, 2, 361782, 209069, 7064, 12462, 49, 162350, 37808, 1515, 148171, 489736, 146068, 16, 363949, 58929, 4726, 48949, 489471, 509, 994, 3118518, 1, 4, 28596, 10, 2105]
            # recoveredCase = [44137, 37981, 69403, 7724, 14825, 13, 152, 25837, 355530, 92645, 467718, 3222, 10419, 1518715, 149873, 81625, 5479, 209522, 6331, 153, 196284, 399, 554, 45744, 24892, 469, 138087, 374, 4885, 13310, 1994, 137842, 7207483, 1632614, 568580, 5872, 773, 138631, 316, 82229, 3985, 2057, 606055, 138888, 860, 5846, 14760, 101, 5154, 210844, 12022, 803, 662429, 155713, 5789, 47, 43356, 119212, 4842, 190350, 54631, 23007, 113563, 1545500, 27, 31000, 123, 203072, 2242, 9549, 9995, 13233, 3677, 2400, 58788, 2119, 226215, 9989, 28, 15, 131017, 688739, 10110634, 451, 425006, 6040, 8468, 8814, 203972, 5726, 1081736, 558777, 23364, 1633839, 11506, 222963, 36260, 2108, 17447, 11936, 2964, 896, 114609, 40, 290430, 52552, 143716, 92608, 5838, 4, 81101, 1150422, 78003, 42569, 1406, 40, 46, 81237, 13365, 67992, 13639, 5326, 514, 24462, 458371, 138865, 2120, 426006, 258968, 92324, 2404, 883, 17623, 46611, 80491, 372056, 123024, 2800675, 309, 2220, 317, 970916, 112371, 1, 3165, 6974, 855, 726, 988, 3638, 1983, 2208451, 10, 796417, 19555, 95, 13215, 76067, 13213, 149082, 149373, 1572, 44845, 109115, 98, 12, 4225, 219144, 8830, 18357, 1434, 973265, 13524, 317600, 6566, 6863, 13666294, 110873, 755, 1130460, 600710, 31, 2, 31536, 150239, 6321, 6098, 41, 119446, 12942, 1361, 132158, 458206, 142827, 15, 355706, 58668, 3639, 42091, 183, 812, 1406967, 1, 1, 20781, 8, 1416]
            countries = []
            activeCase = []
            recoveredCase = []
            print("Total___ %s", len(generalResponse["data"]))
            for GR in generalResponse["data"]:
                if "latest_data" in GR and GR["latest_data"]:
                    print("_Country__ %s", GR["name"])
                    if "confirmed" in GR["latest_data"] and GR["latest_data"]["confirmed"] and "recovered" in GR["latest_data"] and GR["latest_data"]["recovered"]:
                        activeCase.append(GR["latest_data"]["confirmed"])
                        recoveredCase.append(GR["latest_data"]["recovered"])
                        if "name" in GR and GR["name"]:
                            countries.append(GR["name"])
            print("_________________________________++++++++++++++++++++++++++++++++++++++++++++")
            print(countries)
            print(len(countries))
            print(activeCase)
            print(len(activeCase))
            print(recoveredCase)
            print(len(recoveredCase))
            fig = go.Figure([
                go.Bar(name='Confirmed Cases', x=countries, y=activeCase),
                go.Bar(name="Recovered Cases", x=countries, y=recoveredCase)
            ])

            fig.update_layout(title_text='Covid19 API Data')
            fig.show()
            return Response({"success": True, "message": "Exported"})

        except Exception as e:
            print(e)
            return Response({"success": False, "message": "Not Exported"})
