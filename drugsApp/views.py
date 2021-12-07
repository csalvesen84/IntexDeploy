from django.shortcuts import render
from django.http import HttpResponse
from drugsApp.models import Specialty
from drugsApp.models import Prescriber, Credential, State, Triple, Drugs
import requests, json, math

# Create your views here.
def indexPageView(request) :
    return render(request, 'drugsApp/index.html')

def searchPPageView(request) :
    stata = State.objects.all()
    credata = Credential.objects.all()
    spec = Specialty.objects.all()

    
    context = {
        "stateName" : stata,
        "credName" : credata,
        "specName" : spec
    }
    return render(request, 'drugsApp/searchP.html', context)

def searchPageView(request) :
    if request.method == 'GET':
        firstname = request.GET['searchFirstName']
        lastname = request.GET['searchLastName']
        gender = request.GET['searchGender']
        credentials = request.GET['searchCredentials']
        state = request.GET['searchState']
        specialty = request.GET['searchSpecialty']  
        isopioidpres = request.GET['searchIsOpioidPrescriber']

        sQuery = 'SELECT pd_prescriber."NPI", pd_prescriber."Fname", pd_prescriber."Lname", pd_prescriber."Gender", pd_prescriber."Credential", \
                pd_prescriber."StateAbbreviation", pd_prescriber."Specialty", pd_prescriber."IsOpioidPrescriber" \
                FROM pd_prescriber WHERE pd_prescriber."NPI" > 0 ' #bring in Primary key here!
        

        if firstname != "":
            sQuery += 'AND pd_prescriber."Fname" IN (\'' + firstname + '\') '
        if lastname != "":
            sQuery += 'AND pd_prescriber."Lname" IN (\'' + lastname + '\') '
        if gender != "":
            sQuery += 'AND pd_prescriber."Gender" IN (\'' + gender + '\') '
        if credentials != "":
            sQuery += 'AND pd_prescriber."Credential" = (\'' + credentials + '\') '
        if state != "":
            sQuery += 'AND pd_prescriber."StateAbbreviation" = (\'' + state + '\') '
        if specialty != "":
            sQuery += 'AND pd_prescriber."Specialty" = (\'' + specialty + '\') '
        if isopioidpres != "":
            sQuery += 'AND pd_prescriber."IsOpioidPrescriber" = (\'' + isopioidpres + '\') '

        record = Prescriber.objects.raw(sQuery)   
        stata = State.objects.all()
        credata = Credential.objects.all()
        spec = Specialty.objects.all()

        
        context = {
            "searchpres" : record,
            "specName" : spec,
            "stateName" : stata,
            "credName" : credata,
            "qfirstname" : firstname,
            "qlastname" : lastname,
            "qgender" : gender,
            "qcredentials" : credentials,
            "qstate" : state,
            "qspecialty" : specialty, 
            "qisopioidpres" : isopioidpres,
            "nothing" : "No results found. Please try your search again."
        }
        count = 0
        for rec in record:
            count += 1

        if count > 0 :
            return render(request, 'drugsApp/searchPres.html', context)
        else :
            return render(request, 'drugsApp/searchP.html', context)

def searchDPageView(request) :
    drugdata = Drugs.objects.all()

    context = {
        "drugsName" : drugdata,
    }
    return render(request, 'drugsApp/searchD.html', context)

def searchDrugsPageView(request) :
    if request.method == 'GET':
        drugsname = request.GET['searchDrugName']
        isopioiddrug = request.GET['searchDrugOpioid']

        sQuery = 'SELECT pd_drugs.drugid, pd_drugs.drugname, pd_drugs.isopioid, pd_drugs.average \
                FROM pd_drugs WHERE pd_drugs.drugid > 0 ' #bring in Primary key here!

        if drugsname != "":
            sQuery += 'AND pd_drugs.drugname IN (\'' + drugsname + '\') '
        if isopioiddrug != "":
            sQuery += 'AND pd_drugs.isopioid IN (\'' + isopioiddrug + '\') '
        print(sQuery)
        record = Drugs.objects.raw(sQuery)
        drugdata = Drugs.objects.all()
   
        
        context = {
            "searchdrug" : record,
            "drugsName" : drugdata,
            "qdrugsname" : drugsname,
            "qisopioiddrug" : isopioiddrug,
            "nothing" : "No results found. Please try your search again."
        }
        count = 0
        for rec in record:
            count += 1

        if count > 0 :
            return render(request, 'drugsApp/searchDrugs.html', context)
        else :
            return render(request, 'drugsApp/searchD.html', context)

def displayPageView(request) :
    if request.method == 'POST':
        data = Prescriber.objects.all()

        context = {
            "prescribers" : data
        }
        return render(request, 'drugsApp/display.html', context)
    else:
        data = Prescriber.objects.all()[:50]

        context = {
            "prescribers" : data
        }
        return render(request, 'drugsApp/display.html', context)


def analyticsPageView(request) :
    if request.method == 'POST':
        if 'recommend' in request.POST:
            url = "http://9c24615e-0611-450f-88f3-17e5df241cfb.eastus2.azurecontainer.io/score"

            payload = json.dumps({
            "Inputs": {
                "WebServiceInput0": [
                {
                    "PrescriberName": "Lauren Khan",
                    "Gender": "F",
                    "StateAbbreviation": "OH",
                    "Specialty": "Nurse Practitioner",
                    "IsOpioidPrescriber": "False",
                    "TotalPrescriptions": 370,
                    "LnPlus1(TotalPrescriptions)": 5.916202062607435
                },
                {
                    "PrescriberName": "Eden Pace",
                    "Gender": "F",
                    "StateAbbreviation": "AZ",
                    "Specialty": "Nurse Practitioner",
                    "IsOpioidPrescriber": "True",
                    "TotalPrescriptions": 300,
                    "LnPlus1(TotalPrescriptions)": 5.707110264748875
                },
                {
                    "PrescriberName": "Norah Owen",
                    "Gender": "F",
                    "StateAbbreviation": "TN",
                    "Specialty": "Nurse Practitioner",
                    "IsOpioidPrescriber": "True",
                    "TotalPrescriptions": 3178,
                    "LnPlus1(TotalPrescriptions)": 8.064321960910803
                }
                ],
                "WebServiceInput3": [
                {
                    "PrescriberName": request.POST['fullName'],
                    "drugname": request.POST['drugName'],
                    "qty": request.POST['quantity']
                }
                ],
                "WebServiceInput4": [
                {
                    "drugid": 2,
                    "drugname": "ABILIFY",
                    "isopioid": "False"
                },
                {
                    "drugid": 3,
                    "drugname": "ACETAMINOPHEN.CODEINE",
                    "isopioid": "True"
                },
                {
                    "drugid": 4,
                    "drugname": "ACYCLOVIR",
                    "isopioid": "False"
                }
                ]
            },
            "GlobalParameters": {}
            })
            headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer EC9vlVEHBOSSKWpauhadiFk44jamV3sm'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            json_data = json.loads(response.text)

            begin = "Recommended Item "
            recommendations = []

            for i in range(1,6):
                parseStatement = begin + str(i)
            try:
                recommendations.append(json_data["Results"]["WebServiceOutput0"][0][parseStatement])
            except:
                pass

            isOpioid = ["ACETAMINOPHEN.CODEINE", "FENTANYL", "HYDROCODONE.ACETAMINOPHEN", "OXYCODONE.ACETAMINOPHEN", "OXYCONTIN"]

            for dope in isOpioid:
                for rec in recommendations:
                    if dope == rec:
                        recommendations.remove(rec)

            output = ""
            recNum = 1

            for rec in recommendations:
                output += "Recommendation "
                output += str(recNum)
                recNum += 1
                output += ": "
                output += rec
                output += "\n"
                data = Drugs.objects.all()
                stata = State.objects.all()
                spec = Specialty.objects.all()

            context = {
                "out" : output,
                "drugs" : data,
                "states" : stata,
                "specName" : spec
            }
            return render(request, 'drugsApp/analytics.html', context)
        
        elif 'predict' in request.POST:
            url = "http://83e02ed0-e4fc-4c45-9aeb-056be5d01386.eastus2.azurecontainer.io/score"

            payload = json.dumps({
            "Inputs": {
                "WebServiceInput0": [
                {
                    "gender": request.POST['gender'],
                    "state": request.POST['state'],
                    "specialty": request.POST['specialty'],
                    "isopioidprescriber": request.POST['opioidPrescriber'],
                    "LnPlus1(totalprescriptions)": 4.941642422609304
                },
                ]
            },
            "GlobalParameters": {}
            })
            headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer Y7s7arIAW0AMhtNH4W8lYZQG6AVm0rn0'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            json_data = json.loads(response.text)
            data = json_data["Results"]["WebServiceOutput0"][0]["predicted_prescriptions"]
            data = math.exp(data) - 1
            data = math.floor(data)
            drugs = Drugs.objects.all()
            stata = State.objects.all()
            spec = Specialty.objects.all()

            context = {
                "outie" : str(data),
                "drugs" : drugs,
                "states" : stata,
                "specName" : spec
            }
            return render(request, 'drugsApp/analytics.html', context)


    else:
        data = Drugs.objects.all()
        stata = State.objects.all()
        spec = Specialty.objects.all()

        context = {
            "drugs" : data,
            "states" : stata,
            "specName" : spec
        }
        return render(request, 'drugsApp/analytics.html', context)

def detailPageView(request, detailNPI) :  
    data = Prescriber.objects.get(NPI = detailNPI)
    presTriple = Triple.objects.filter(prescriberid = data.NPI)
    context = {
        "pres" : data,
        "triple" : presTriple
    }
    return render(request, 'drugsApp/detail.html', context)

def detailDrugPageView(request, detaildrugname) :
    data = Drugs.objects.get(drugname = detaildrugname)
    sQuery = 'SELECT * FROM pd_triple WHERE pd_triple."drugname" = \'' + detaildrugname + '\' ORDER BY pd_triple."qty" DESC LIMIT 10'
    querydata = Triple.objects.raw(sQuery)
    context = {
        "drug" : data,
        "prescriber" : querydata
    }
    return render(request, 'drugsApp/detailDrug.html', context)

def editPageView(request, editNPI) :
    data = Prescriber.objects.get(NPI = editNPI)
    presState = State.objects.get(stateabbrev=data.StateAbbreviation)
    stata = State.objects.all()
    credata = Credential.objects.all()
    specs = Specialty.objects.all()

    context = {
        "pres" : data,
        "presState" : presState,
        "stateName" : stata,
        "credName" : credata,
        "specName" : specs
    }
    
    return render(request, 'drugsApp/edit.html', context)

def updatePageView(request):
    if request.method == 'POST':
        editNPI = request.POST['editNPI']

        prescriber = Prescriber.objects.get(NPI=editNPI)

        #THIS CODE WAS AN ATTEMPT TO MAKE THE True and False not true and false
        value = str(request.POST['opioidPrescriber'])
        value = value.capitalize()
        prescriber.IsOpioidPrescriber = value


        state = request.POST['state']
        prescriber.Fname = request.POST['firstName']
        prescriber.Lname = request.POST['lastName']
        prescriber.Gender = request.POST['gender']
        prescriber.Credential = request.POST['credentials']
        prescriber.StateAbbreviation = State.objects.get(stateabbrev=state)
        prescriber.Specialty = request.POST['specialty']
        prescriber.TotalPrescriptions = request.POST['totalPrescriptions']


        prescriber.save()
    return displayPageView(request)

def deletePageView(request, deleteNPI):
    data = Prescriber.objects.get(NPI = deleteNPI)

    data.delete()

    return displayPageView(request)

def addPageView(request) :
    if request.method == 'POST': 
        prescriber = Prescriber()

        state = request.POST['state']
        prescriber.StateAbbreviation = State.objects.get(stateabbrev=state)
        prescriber.NPI = request.POST['npi']
        prescriber.Fname = request.POST['firstName']
        prescriber.Lname = request.POST['lastName']
        prescriber.Gender = request.POST['gender']
        prescriber.Credential = request.POST['credentials']
        prescriber.Specialty = request.POST['specialty']
        prescriber.TotalPrescriptions = request.POST['totalPrescriptions']
        prescriber.IsOpioidPrescriber = request.POST['opioidPrescriber']

        prescriber.save()

        return displayPageView(request)
    else : 
        data = State.objects.all()
        creds = Credential.objects.all()
        specs = Specialty.objects.all()

        context = {
            "stateName" : data,
            'credentialName' : creds,
            'specialtyName' : specs
        }

        return render(request, 'drugsApp/add.html', context)