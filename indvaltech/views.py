from multiprocessing import Event
from re import L, template
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.core.mail import send_mail

# Create your views here.


def login_user(request):
    if request.method == "POST":
        username = request.POST['user']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            email = User.objects.get(username=username).email
            des = HRD_table.objects.get(Company_email=email).Designation
            name = HRD_table.objects.get(Company_email=email).Name
            if(des == "CEO" or des == "HR"):

                leaveData=Leave.objects.all()
                data=leaveData
                return render(request,'HRD.html',{'data':data})

            elif('manager' in des or 'Manager' in des):
                return redirect(icons, name=name)
            else:
                return redirect(designer, name=name)
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, 'login.html')


def family(request, name):
    query = HRD_table.objects.filter(Q(Name=name))
    r = query[0]
    data = Family.objects.filter(Q(EID=r))
    if request.method == "POST":
        query = HRD_table.objects.filter(Q(Name=name))
        r = query[0]
        fname = request.POST['fmember_name']
        age = request.POST['age']
        relation = request.POST['relatives']
        occupation = request.POST['occupation']
        contact = request.POST['contact']
        remarks = request.POST['remarks']
        if len(contact) == 10:
               form1 = Family(EID=r, name=fname, age=age, relation=relation,
                               occupation=occupation, contact=contact, remarks=remarks)
               form1.save()
               data = Family.objects.filter(Q(EID=r))
               return render(request, 'Family.html', {'name': name, 'datas': data})
        else:
               messages.error(request, 'Invalid Phone Number')
    return render(request, 'Family.html', {'name': name, 'datas': data})


def family_delete(request, name, relation):
    if request.method == 'POST':
        query = HRD_table.objects.filter(Q(Name=name))
        r = query[0]
        obj = Family.objects.get(EID=r, relation=relation)
        obj.delete()
        return redirect(family, name=name)


def register(request, name):
        if request.method == 'POST':
            query=HRD_table.objects.filter(Q(Name=name))
            r=query[0]
            aadhar=request.POST['aadhar']
            Gender=request.POST['gender']
            Email=request.POST['email']
            aadharDoc=request.FILES['aDoc']
            Pan=request.POST['Pan']
            panDoc=request.FILES['panDoc']
            passport=request.POST['passport']
            passportDoc=request.FILES['passportDoc']
            esicNum=request.POST['esicNum']
            esicDoc=request.FILES['esicDoc']
            Address=request.POST['sala']
            PermanentAddress=request.POST['paddress']
            Ph=request.POST['ph']
            DOB=request.POST['dob']
            Blood=request.POST['blood']
            EmergencyPh=request.POST['eph']
            Photo=request.FILES['img']

            print(Photo.size)

         #VALIDATION

            if len(Ph) == 10 and len(EmergencyPh)==10  and len(aadhar)==10 and len(esicNum)==11 and Photo.size<1000000 and esicDoc.size<1000000 and passportDoc.size<1000000 and panDoc.size<1000000  and aadharDoc.size<1000000 :
              employeeRegistrationForm = Employee(esicNum=esicNum,esicDoc=esicDoc,passportDoc=passportDoc,passport=passport,panDoc=panDoc,Pan=Pan,aadhar=aadhar,aadharDoc=aadharDoc,Name=r,Address=Address,PermanentAddress=PermanentAddress,Ph=Ph,Gender=Gender,DOB=DOB,Email=Email,Blood=Blood,EmergencyPh=EmergencyPh,Photo=Photo)
              employeeRegistrationForm.save()
              return render(request, 'Education.html', {'name': name})

            else:
              messages.error(request, 'Invalid Phone Number of emergency phone number')
              return render(request,'employee.html',{'name':name})
        return render(request,'employee.html',{'name':name})


def hr(request):
        return render(request,'hrDashboard.html')


def bank(request, name):
    if request.method == "POST":
        query = HRD_table.objects.filter(Q(Name=name))
        r = query[0]
        acNo = request.POST['acNo']
        ifsc = request.POST['ifsc']
        scode = request.POST['sCode']
        iban = request.POST['iban']
        bankname = request.POST['bankname']
        branchname = request.POST['branchname']

        if len(ifsc) ==11:
            bankform = Bank(EID=r, name=name, account=acNo, ifsc=ifsc,
                            swift=scode, iban=iban, bank_name=bankname, branch=branchname)
            bankform.save()
            messages.success(request, ("Details updated"))
            return render(request, 'history.html', {'name': name})
        else:
            messages.error(request, 'Invalid IFSC Code')
    return render(request, 'bank.html', {'name': name})


class AddProject(View):
    def get(self, request, *args, **kwargs):
        all_emp = HRD_table.objects.all()
        return render(request, 'AddProject.html', {'all_emp': all_emp})

    def post(self, request, *args, **kwargs):
        pid = request.POST['pid']
        eid = request.POST['employees']
        query = HRD_table.objects.filter(Q(EID=eid))
        r = query[0]
        pname = request.POST['pname']
        department = request.POST['subject']
        sdate = request.POST['sop']
        edate = request.POST['eop']
        location = request.POST['subject2']
        pdesc = request.POST['remarks']

        projectform = Project(PID=pid, EID=r, Pname=pname, Department=department,
                              StartDate=sdate, EndDate=edate, location=location, ProjectDesc=pdesc )
        projectform.save()
        messages.success(request, ("Details updated"))
        return render(request, 'AddProject.html')


def AttendForm(request):
    return render(request, 'AttendanceForm.html')


def DesignDashboard(request):
    return render(request, 'Design Dashboard.html')


def education(request, name):
    query = HRD_table.objects.filter(Q(Name=name))
    r = query[0]
    data = Education.objects.filter(Q(EID=r))

    if request.method == "POST":
        query = HRD_table.objects.filter(Q(Name=name))
        r = query[0]
        q = request.POST['qual']
        b = request.POST['board']
        p = request.POST['percentage']
        y = request.POST['yop']

        educationform = Education(
            EID=r, qualification=q, board=b, percentage=p, passing=y)
        educationform.save()
        data = Education.objects.filter(Q(EID=r))
        return render(request, 'Education.html', {'name': name, 'datas':data})

    return render(request, 'Education.html', {'name': name, 'datas': data})


def education_delete(request, name, qual):
    if request.method == 'POST':
        query = HRD_table.objects.filter(Q(Name=name))
        r = query[0]
        obj = Education.objects.get(EID=r, qualification=qual)
        obj.delete()
        return redirect(education, name=name)


class AddActivity(View):
    def get(self, request, *args, **kwargs):
        all_project = Project.objects.all()
        return render(request, 'AddActivity.html', {'all_project': all_project})

    def post(self, request, *args, **kwargs):
        pname = request.POST['subject']
        query2 = Project.objects.filter(Q(Pname=pname))
        r = query2[0]
        task = request.POST['subject2']
        allocatedtime = request.POST['allocatedtime']
        actualtime = request.POST['actualtime']
        date = request.POST['date']

        addactivityform = Team(
            PID=r, TaskName=task, Allocated=allocatedtime, ActualTime=actualtime, dates=date)
        addactivityform.save()
        return render(request, 'AddActivity.html')


def history(request, name):
    query = HRD_table.objects.filter(Q(Name=name))
    r = query[0]
    data = History.objects.filter(Q(EID=r))
    if request.method == "POST":
        query = HRD_table.objects.filter(Q(Name=name))
        r = query[0]
        org = request.POST['org']
        work = request.POST['nature']
        designation = request.POST['designation']
        tools = request.POST['software']
        last_salary = request.POST['lsalary']
        reason_of_leaving = request.POST['reason']
        recepient = HRD_table.objects.get(Name=name).Company_email

        employeeHistoryForm = History(EID=r, organization=org, last_salary=last_salary, tools=tools,
                                      designation=designation, work=work, reason_of_leaving=reason_of_leaving)
        employeeHistoryForm.save()
        data = History.objects.filter(Q(EID=r))
        send_mail(
            subject="Form Submission",
            message='All the forms have been submitted',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recepient])
        return render(request, 'history.html', {'name': name, 'datas': data})
    return render(request, 'history.html', {'name': name, 'datas': data})


def history_delete(request, name, org):
    if request.method == 'POST':
        query = HRD_table.objects.filter(Q(Name=name))
        r = query[0]
        obj = History.objects.get(EID=r, organization=org)
        obj.delete()
        return redirect(history, name=name)

def timesheet(request):
    return render(request, 'Timesheets.html')


def leave(request,name):
     if request.method == 'POST':
       query = HRD_table.objects.filter(Q(Name=name))
       r=query[0]
       FromDate=request.POST['FromDate']
       ToDate=request.POST['ToDate']
       Reason=request.POST['Reason']

       leaveForm=Leave(EID=r,FromDate=FromDate,ToDate=ToDate,Reason=Reason)
       leaveForm.save()
       messages.success(request, ("Details updated"))
       return render(request, 'index.html', {'name': name})
     return render(request,'applyLeave.html', {'name': name})

def payslip(request, name):
    return render(request, 'payslip.html', {'name': name})


def hrd(request):
    if request.method=='POST':
        id_list=request.POST.getlist('boxes')
        leaveData=Leave.objects.all()
        data=leaveData


        for x in id_list:
         Leave.objects.filter(id=int(x)).update(approvel=True)
        return render(request, 'HRD.html',{'data':data})
    return render(request, 'HRD.html')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'forgotpasswrd.html'
    email_template_name = 'reset_email_content.html'
    success_url = reverse_lazy('login')
    #success_message = "We've emailed you instructions for setting your password, " \
    #                   "if an account exists with the email you entered. You should receive them shortly." \
    #                   " If you don't receive an email, " \
    #                   "please make sure you've entered the address you registered with, and check your spam folder."


class setpPasswordView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'onlinetemp.html'
    success_message = "Password reset complete"\
    " please login again"
    success_url = reverse_lazy('login')


def search(request, name):
    if request.method == 'POST':
        if request.POST.get('ename'):
            enames = request.POST['ename']
            query = HRD_table.objects.filter(Q(Name=enames))
            r = query[0]

            HRDDetails = HRD_table.objects.filter(Q(EID=r))
            personaldetails = Employee.objects.filter(Q(Name=enames))
            educationdetails = Education.objects.filter(Q(EID=r))
            certificates = Certification.objects.filter(Q(EID=r))
            bankdetials = Bank.objects.filter(Q(EID=r))
            familydetails = Family.objects.filter(Q(EID=r))
            workingprojects = Project.objects.filter(Q(EID=r))
            Employeehistory = History.objects.filter(Q(EID=r))

            return render(request, 'EmployeeDetails.html', {'data1': personaldetails, 'data2': educationdetails, 'data3': certificates, 'data4': bankdetials, 'data5': familydetails, 'data6':workingprojects, 'data7': Employeehistory, 'data8': HRDDetails })
            #return render(request, 'index.html', {'name': r})

        if request.POST.get('emp_id'):
            eid = request.POST['emp_id']
            query = HRD_table.objects.filter(Q(EID=eid))
            r = query[0]
            HRDDetails = HRD_table.objects.filter(Q(EID=eid))
            personaldetails = Employee.objects.filter(Q(Name=r))
            educationdetails = Education.objects.filter(Q(EID=eid))
            certificates = Certification.objects.filter(Q(EID=eid))
            bankdetials = Bank.objects.filter(Q(EID=eid))
            familydetails = Family.objects.filter(Q(EID=eid))
            workingprojects = Project.objects.filter(Q(EID=eid))
            Employeehistory = History.objects.filter(Q(EID=eid))

            return render(request, 'EmployeeDetails.html', {'data1': personaldetails, 'data2': educationdetails, 'data3': certificates, 'data4': bankdetials, 'data5': familydetails, 'data6':workingprojects, 'data7': Employeehistory, 'data8': HRDDetails })
    return render(request, 'search.html', {'name': name})


def icons(request, name):
    return render(request, 'icons.html', {'name': name})

def result(request):
    if request.method == 'POST':
        value=request.POST['searchBy']
        if value == "1":
            eid = request.POST['emp']
            query = HRD_table.objects.filter(Q(EID=eid))
            r = query[0]
            HRDDetails = HRD_table.objects.filter(Q(EID=eid))
            personaldetails = Employee.objects.filter(Q(Name=r))
            educationdetails = Education.objects.filter(Q(EID=eid))
            certificates = Certification.objects.filter(Q(EID=eid))
            bankdetials = Bank.objects.filter(Q(EID=eid))
            familydetails = Family.objects.filter(Q(EID=eid))
            workingprojects = Project.objects.filter(Q(EID=eid))
            Employeehistory = History.objects.filter(Q(EID=eid))
            return render(request, 'EmployeeDetails.html', {'data1': personaldetails, 'data2': educationdetails, 'data4': bankdetials, 'data5': familydetails, 'data6':workingprojects, 'data7': Employeehistory, 'data8': HRDDetails })

        if value == "2":
            enames = request.POST['emp']
            query = HRD_table.objects.filter(Q(Name=enames))
            r = query[0]
            personaldetails = Employee.objects.filter(Q(Name=r))
            educationdetails = Education.objects.filter(Q(EID=r))
            certificates = Certification.objects.filter(Q(EID=r))
            bankdetials = Bank.objects.filter(Q(EID=r))
            familydetails = Family.objects.filter(Q(EID=r))
            workingprojects = Project.objects.filter(Q(EID=r))
            HRDDetails = HRD_table.objects.filter(Q(Name=enames))
            Employeehistory = History.objects.filter(Q(EID=r))

            return render(request, 'EmployeeDetails.html', {'data1': personaldetails, 'data2': educationdetails, 'data3': certificates, 'data4': bankdetials, 'data5': familydetails, 'data6':workingprojects, 'data7': Employeehistory, 'data8': HRDDetails })

        if value == "3":
            pname = request.POST['emp']
            emplist = Project.objects.filter(Q(Pname=pname))
            return render(request, 'searchbyproj.html', {'data': emplist})
    return render(request, 'EmployeeDetails.html')
# def approvel(request,name):
#       if request.method == "POST":
#          query = HRD_table.objects.filter(Q(Name=name))
#          r = query[0]
#          leave=Leave.objects.filter(Q(EID=r))
#          leaveData=leave[0]
#          leaveData.approvel=True
#          leave.save()
#          return render(request, 'index.html', {'name': name})

def hrDashboard(request):
    return render(request, 'hrDashboard.html')


def bankedit(request, name):
    return render(request, 'editbank.html', {'name': name})


def personaledit(request, name):
    return render(request, 'editpersonaldetails.html', {'name': name})

def get_chart(request):
    labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
    items = [10, 20, 8, 28, 40, 4]
    data = {
        "labels": labels,
        "defaultData": items
    }
    return JsonResponse(data)

def designer(request, name):
    return render(request, 'DesignerDashboard.html', {'name': name})

def searchbyproj(request):
    return render(request, 'searchbyproj.html')

def Emplist(request):
    elist = HRD_table.objects.all()
    return render(request, 'employeedetailsview.html', {'data': elist})

def elists(request, name):
    query = HRD_table.objects.filter(Q(Name=name))
    r = query[0]
    personaldetails = Employee.objects.filter(Q(Name=r))
    educationdetails = Education.objects.filter(Q(EID=r))
    Employeehistory = History.objects.filter(Q(EID=r))
    bankdetials = Bank.objects.filter(Q(EID=r))
    familydetails = Family.objects.filter(Q(EID=r))
    workingprojects = Project.objects.filter(Q(EID=r))
    return render(request, 'EmployeeDetails.html', {'data1': personaldetails, 'data2': educationdetails, 'data4': bankdetials, 'data5': familydetails, 'data6':workingprojects, 'data7': Employeehistory, 'data8': query })
