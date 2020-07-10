
from flask import Flask, request, render_template
from time import gmtime, strftime, localtime
from datetime import datetime
from pytz import timezone
import os, sys
import os.path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape
from reportlab.platypus import Image
import smtplib
import shutil
from glob import glob
import subprocess
import matlab.engine

app = Flask(__name__)

patientId = ''
lat_line = 20
lng_line = 22

def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ("successfully sent the mail")
    except:
        print ("failed to send mail")

def import_data(path,patientId):
    path_patient = path +"/"+ patientId
    d = path_patient
    dirs = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    generate_pdf(dirs,path_patient,patientId)
    flagd = 1;
    for time in dirs:
        DoneFilePath = time +"/" +"d.txt"
        #print (DoneFilePath)
        if not os.path.exists(DoneFilePath):
            flagd = 0;
    print (flagd)
    if flagd == 1:
        send_email('biomedical.uaosc@gmail.com','biomedical','biomedical.uaosc@gmail.com',patientId,' Docter checked. \n PDF report generated OR updated. \n Use our mobile app or website to check. ')
    
    
def generate_pdf(dirs,path_patient,patientId):
    pdf_name = "/report.pdf"
    save_name = path_patient + pdf_name
    c = canvas.Canvas(save_name,pagesize=A4)
    
    fistline = "Overall Report of Patient ID:  "
    
    '''draw header'''
    c.setFont('Helvetica',30,leading=None)
    c.drawCentredString(300,760,fistline)
    c.drawCentredString(300,730,patientId)
    
    rob_path = "/var/www/html/project_oral_x/flaskapp/rob.jpg"
    c.drawImage(rob_path,500,120,width=90,height=128)

    '''page 1'''
    
    # Patient Info
    height = 660
    c.setFont('Helvetica',16,leading=None)
    c.drawString(100,height,"Patient Basic Information:")
    height = height -20
    c.setFont('Helvetica',10,leading=None)
    txtPathInfo = path_patient + "/1.txt"
    with open(txtPathInfo, "r") as f:
        for line in f:
            line = line.strip()
            c.drawString(100,height,line)
            height = height - 15
    height = height -50
    txtPathInfo = path_patient + "/upload_time.txt"
    with open(txtPathInfo, "r") as f:
        for line in f:
            line = line.strip()
            c.drawString(100,height,line)
            height = height - 15
    height = height -50
    
    # jpg list
    height = 660
    c.setFont('Helvetica',16,leading=None)
    c.drawString(360,height,"File List:")
    height = height -20
    c.setFont('Helvetica',8,leading=None)
    for subfolder in dirs:
        folderName = subfolder.replace(path_patient,'')
        c.drawString(360,height,folderName)
        height = height - 15
        for file in os.listdir(subfolder):
            if file.endswith(".jpg"):
                c.drawString(380,height,file)
                height = height - 15


    
    c.showPage()
    
    # main body
    
    for subfolder in dirs:
        jpgPath = [None] * 5
        i = 0
        txtPathresult = subfolder + "/result.txt"
        with open(txtPathresult, "r") as f:
            contentresult = f.read()
        txtPathcomment = subfolder + "/comment.txt"
        with open(txtPathcomment, "r") as f:
            contentcomment = f.read()
            for file in os.listdir(subfolder):
                #if file.endswith(".jpg"):
                #    jpgPath[i] = subfolder + "/" + file
                #    i = i + 1
                     #if file.endswith(".jpg"):
                     #   jpgPath[i] = imgfilePath_time + "/" + file
                     #   jpg_name[i] = file.replace(".jpg",'')
                     #   i = i + 1
                if "FL" in file:
                    jpgPath[0] = subfolder + "/" + file
                    #jpg_name[0] = file.replace(".jpg",'')
                    i = i + 1
                if "fl" in file:
                    jpgPath[1] = subfolder + "/" + file
                    #jpg_name[1] = file.replace(".jpg",'')
                    i = i + 1
                if "WL" in file:
                    jpgPath[2] = subfolder + "/" + file
                    #jpg_name[2] = file.replace(".jpg",'')
                    i = i + 1
                if "wl" in file:
                    jpgPath[3] = subfolder + "/" + file
                    #jpg_name[3] = file.replace(".jpg",'')
                    i = i + 1
            if jpgPath[0] == None:
                jpgPath[0] = jpgPath[2]
                #jpg_name[0] = jpg_name[2]
                jpgPath[1] = jpgPath[3]
                #jpg_name[1] = jpg_name[3]
                    
                    
        if i == 4:
            generate_page_pair(jpgPath,subfolder,c)
        if i == 2:
            generate_page_single(jpgPath,subfolder,c)
            
    c.save()

            
def generate_page_pair(jpgPath,subfolder,c):
    height = 760
    c.setFont('Helvetica',16,leading=None)
    c.drawString(100,height,"For Reference:")
    height = height -30
    c.setFont('Helvetica',6,leading=None)
    txtPathresult = subfolder + "/result.txt"
    with open(txtPathresult, "r") as f:
        for line in f:
            line = line.strip()
            c.drawString(100,height,line)
            height = height -13
    height = height - 0
    c.setFont('Helvetica',16,leading=None)
    c.drawString(100,height,"Doctor Comments:")
    c.setFont('Helvetica',6,leading=None)
    height = height -0
    txtPathcomment = subfolder + "/comment.txt"
    with open(txtPathcomment, "r") as f:
        for line in f:
            line = line.strip()
            c.drawString(100,height,line)
            height = height -13
            
    image_fl = jpgPath[0]
    image_name = image_fl.replace(subfolder + "/",'')
    image_name = image_name.replace(".jpg",'')
    c.drawImage(image_fl,350,690,width=130,height=130)
    c.drawString(350,660,"Figure 1, " + image_name +".")
    image_wl = jpgPath[1]
    image_name = image_wl.replace(subfolder + "/",'')
    image_name = image_name.replace(".jpg",'')
    c.drawImage(image_wl,350,510,width=130,height=130)
    c.drawString(350,480,"Figure 2, " + image_name +".")
    image_fl_analyze = jpgPath[2]
    image_name = image_fl_analyze.replace(subfolder + "/",'')
    image_name = image_name.replace(".jpg",'')
    c.drawImage(image_fl_analyze,350,330,width=130,height=130)
    c.drawString(350,300,"Figure 3, " + image_name +".")
    image_wl_analyze = jpgPath[3]
    image_name = image_wl_analyze.replace(subfolder + "/",'')
    image_name = image_name.replace(".jpg",'')
    c.drawImage(image_wl_analyze,350,150,width=130,height=130)
    c.drawString(350,120,"Figure 4, " + image_name +".")

    c.showPage()

def generate_page_single(jpgPath,subfolder,c):
    height = 760
    c.setFont('Helvetica',16,leading=None)
    c.drawString(100,height,"For Reference:")
    height = height -30
    c.setFont('Helvetica',6,leading=None)
    txtPathresult = subfolder + "/result.txt"
    with open(txtPathresult, "r") as f:
        for line in f:
            line = line.strip()
            c.drawString(100,height,line)
            height = height -13
    height = height - 30
    c.setFont('Helvetica',16,leading=None)
    c.drawString(100,height,"Doctor Comments:")
    c.setFont('Helvetica',6,leading=None)
    height = height -13
    txtPathcomment = subfolder + "/comment.txt"
    with open(txtPathcomment, "r") as f:
        for line in f:
            line = line.strip()
            c.drawString(100,height,line)
            height = height -13

    image_fl = jpgPath[0]
    c.drawImage(image_fl,350,560,width=160,height=160)
    c.drawString(350,530,"Figure 1, Original Img")
    image_wl = jpgPath[1]
    #c.drawImage(image_wl,350,290,width=160,height=160)
    #c.drawString(350,260,"Figure 2, Suspicous area Img.")    
    
    c.showPage()

@app.route('/check_statistics', methods=['GET', 'POST'])
def check_statistics():
    txtPathStatistics = "/var/www/html/project_oral_x/flaskapp/static/statistics.txt"
    with open(txtPathStatistics, "r") as f:
        content = f.read()
    return render_template('check_statistics.html',content=content)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/ViewMap', methods=['GET','POST'])
def view_map():
    path = "/var/www/html/project_oral_x/flaskapp/static/patientInfo"
    #path = "./static/patientInfo"
    dirs = os.listdir( path )
    patient_num = len(dirs)
    lat_coordi=[None] * patient_num
    lng_coordi=[None] * patient_num
    i = 0;
    for patient in dirs:
        txtPathInfo = path + "/" + patient + "/1.txt"
        f1 = open(txtPathInfo)
        lines = f1.readlines()
        if len(lines) > 18:
            lat_coordi[i] = lines[lat_line].strip()
            lng_coordi[i] = lines[lng_line].strip()

        else :
            lat_coordi[i] = ""
            lng_coordi[i] = ""

        #lat_coordi[i] = lines[lat_line].strip()
        #lng_coordi[i] = lines[lng_line].strip()
        i = i + 1
    return render_template('ViewMap.html',latCoordi = lat_coordi,lngCoordi=lng_coordi)

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/contact1', methods=['GET'])
def contact1():
    return render_template('contact1.html')

@app.route('/signin1', methods=['GET'])# signin2signinin1 sign-in
def signin_form():
    return render_template('form.html')

@app.route('/signin', methods=['GET']) #post2get sign-in
def signin():
    #username = request.form['username'] # sign-in
    #password = request.form['password'] # sign-in
    #if username=='admin' and password=='p':  #sign-in
        path = "/var/www/html/project_oral_x/flaskapp/static/patientInfo"
        #path ="./static/patientInfo"
        dirs = os.listdir( path )
        
        dirs_file = [None] *len(dirs)
        dirs.sort()
        i = 0;
        for patient in dirs:
            #pdfPath = path + "/" + patient + "/report.pdf"
            patient_path = path + "/" + patient
            dirs_time = [d for d in os.listdir(patient_path) if os.path.isdir(os.path.join(patient_path,d))]
            flagd = 1;
            for time in dirs_time:
                DoneFilePath = patient_path + "/" + time +"/" +"d.txt"
                #print (DoneFilePath)
                if not os.path.exists(DoneFilePath):
                    flagd = 0;
            if flagd == 1:
                dirs_file[i] = "report"
            else: 
                dirs_file[i] = "wait"
            i = i+1
        #seperate wait and reported cases
        number_wait = 0
        number_report = 0
        for check in dirs_file:
            if check == "report":
                number_report = number_report + 1
            else :
                number_wait = number_wait +1    
        dirs_wait = [None]*number_wait
        dirs_report = [None]*number_report
        print(number_wait)
        print(number_report)
        print(len(dirs_file))
        print(len(dirs))

        number_report_dimapur = 0;
        number_report_kle = 0;
        number_report_mscc = 0;
        number_report_uci = 0;
        number_report_other = 0;
        k = 0
        for location in dirs:
            if dirs_file[k] == "report":
                if "dm" in location:
                    number_report_dimapur = number_report_dimapur + 1
                elif "kl" in location:
                    number_report_kle = number_report_kle + 1
                elif "nh" in location:
                    number_report_mscc = number_report_mscc + 1
                elif "uci" in location:
                    number_report_uci = number_report_uci + 1
                else :
                    number_report_other = number_report_other + 1
            k=k+1
        print(number_report_dimapur)
        print(number_report_kle)
        print(number_report_mscc)
        print(number_report_uci)
        print(number_report_other)
        dirs_report_dimapur = [None]*number_report_dimapur
        dirs_report_kle = [None]*number_report_kle
        dirs_report_mscc = [None]*number_report_mscc
        dirs_report_uci = [None]*number_report_uci
        dirs_report_other = [None]*number_report_other
        i1 = 0
        i2 = 0
        i3 = 0
        i4 = 0
        i5 = 0
        j = 0
        k = 0                               
        for check in dirs_file:
            if k == 379 :
                break
            #print(k)
            #print(check)
            #print(dirs[k])
            if check == "report":
                if "dm" in dirs[k]: 
                    print(dirs[k])                                  
                    dirs_report_dimapur[i1] = dirs[k]
                    i1=i1+1
                    k=k+1
                elif "kl" in dirs[k]:
                    dirs_report_kle[i2] = dirs[k]
                    i2=i2+1
                    k=k+1
                elif "nh" in dirs[k]:
                    dirs_report_mscc[i3] = dirs[k]
                    i3=i3+1
                    k=k+1
                elif "uci" in dirs[k]:
                    dirs_report_uci[i4] = dirs[k]
                    i4=i4+1
                    k=k+1
                else: 
                    dirs_report_other[i5] = dirs[k]
                    i5=i5+1
                    k=k+1                           
            if check == "wait" :
                 dirs_wait[j] = dirs[k]   
                 j=j+1
                 k=k+1  
        #print(dirs_report)                               
        return render_template('list_patient.html',dirs=dirs_wait,dirs_dimapur=dirs_report_dimapur,dirs_kle=dirs_report_kle,dirs_mscc=dirs_report_mscc,dirs_uci=dirs_report_uci,dirs_other=dirs_report_other,number_report=number_report)
        
    #return render_template('form.html', message='username and password not matched', username=username)  #sign-in
    #return render_template('form.html', message='under maintanence', username=username)

@app.route('/list_patient_back', methods=['GET','POST'])
def list_patient_back():

    path = "/var/www/html/project_oral_x/flaskapp/static/patientInfo"
    #path ="./static/patientInfo"
    dirs = os.listdir( path )
    
    dirs_file = [None] *len(dirs)
    dirs.sort()
    i = 0;
    for patient in dirs:
        #pdfPath = path + "/" + patient + "/report.pdf"
        patient_path = path + "/" + patient
        dirs_time = [d for d in os.listdir(patient_path) if os.path.isdir(os.path.join(patient_path,d))]
        
        flagd = 1;
        for time in dirs_time:
            DoneFilePath = patient_path + "/" + time +"/" +"d.txt"
            #print (DoneFilePath)
            if not os.path.exists(DoneFilePath):
                flagd = 0;
        if flagd == 1:
            dirs_file[i] = "report"
        else: 
            dirs_file[i] = "wait"
        i = i+1
    #seperate wait and reported cases
    number_wait = 0
    number_report = 0
    for check in dirs_file:
        if check == "report":
            number_report = number_report + 1
        else :
            number_wait = number_wait +1    
    dirs_wait = [None]*number_wait
    dirs_report = [None]*number_report
    number_report_dimapur = 0;
    number_report_kle = 0;
    number_report_mscc = 0;
    number_report_uci = 0;
    number_report_other = 0;
    k = 0
    for location in dirs:
        if dirs_file[k] == "report":
            if "dm" in location:
                number_report_dimapur = number_report_dimapur + 1
            elif "kl" in location:
                number_report_kle = number_report_kle + 1
            elif "nh" in location:
                number_report_mscc = number_report_mscc + 1
            elif "uci" in location:
                number_report_uci = number_report_uci + 1
            else :
                number_report_other = number_report_other + 1
        k=k+1
    print(number_report_dimapur)
    print(number_report_kle)
    print(number_report_mscc)
    print(number_report_uci)
    print(number_report_other)
    dirs_report_dimapur = [None]*number_report_dimapur
    dirs_report_kle = [None]*number_report_kle
    dirs_report_mscc = [None]*number_report_mscc
    dirs_report_uci = [None]*number_report_uci
    dirs_report_other = [None]*number_report_other
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    i5 = 0
    j = 0
    k = 0                               
    for check in dirs_file:
        if k == 379 :
            break
        #print(k)
        #print(check)
        #print(dirs[k])
        if check == "report":
            if "dm" in dirs[k]: 
                print(dirs[k])                                  
                dirs_report_dimapur[i1] = dirs[k]
                i1=i1+1
                k=k+1
            elif "kl" in dirs[k]:
                dirs_report_kle[i2] = dirs[k]
                i2=i2+1
                k=k+1
            elif "nh" in dirs[k]:
                dirs_report_mscc[i3] = dirs[k]
                i3=i3+1
                k=k+1
            elif "uci" in dirs[k]:
                dirs_report_uci[i4] = dirs[k]
                i4=i4+1
                k=k+1
            else: 
                dirs_report_other[i5] = dirs[k]
                i5=i5+1
                k=k+1                           
        if check == "wait" :
            dirs_wait[j] = dirs[k]   
            j=j+1
            k=k+1
    #print(dirs_report)     
    return render_template('list_patient.html',dirs=dirs_wait,dirs_dimapur=dirs_report_dimapur,dirs_kle=dirs_report_kle,dirs_mscc=dirs_report_mscc,dirs_uci=dirs_report_uci,dirs_other=dirs_report_other,number_report=number_report)

@app.route("/list_patient_delete/<hashcode>",methods=['GET',"POST"])
@app.route("/list_patient_delete/",methods=['GET',"POST"])
def list_patient_delete(hashcode=None):
    if not hashcode == None:
        print (hashcode)
        print (hashcode)
        global patientId
        patientId = hashcode
        path = "/var/www/html/project_oral_x/flaskapp/static/patientInfo"
        #path ="./static/patientInfo"
        showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ip = request.environ.get('HTTP_X_REALIP',request.remote_addr)
        trash_path ="/var/www/html/trash/" + patientId + "-_-" + showtime + "-_-" + ip

        file_path = path + "/" + patientId
        shutil.copytree(file_path,trash_path)
        shutil.rmtree(file_path)
        dirs = os.listdir( path )
        dirs_file = [None] *len(dirs)
        dirs.sort()
        i = 0;
        for patient in dirs:
            #pdfPath = path + "/" + patient + "/report.pdf"
            patient_path = path + "/" + patient
            dirs_time = [d for d in os.listdir(patient_path) if os.path.isdir(os.path.join(patient_path,d))]
        
            flagd = 1;
            for time in dirs_time:
                DoneFilePath = patient_path + "/" + time +"/" +"d.txt"
                #print (DoneFilePath)
                if not os.path.exists(DoneFilePath):
                    flagd = 0;
            if flagd == 1:
                dirs_file[i] = "report"
            else: 
                dirs_file[i] = "wait"
            i = i+1
        return render_template('list_patient.html',dirs=dirs,dirs_file=dirs_file)

    else:
        print ("Not Received")
        return render_template('home.html')

@app.route("/list_patient1_fix/<hashcode>",methods=['GET',"POST"])
@app.route("/list_patient1_fix/",methods=['GET',"POST"])
def list_patient1_fix(hashcode=None):
    if not hashcode == None:
        #print (hashcode)
        #print (hashcode)
        global patientId
        patientId = hashcode
    
        path = "/var/www/html/project_oral_x/flaskapp/static/patientInfo"
        matlabpatientpath = path+"/"+patientId+"/"
        #line0 = "cd /var/www/html/project_oral_x/"
        #line1 = "sudo chmod -R 777 /var/www/html/project_oral_x/flaskapp/static/patientInfo/"
        #line2 = 'matlab -nodisplay -r \"folder_test(\''+commandpatientpath+'\');exit;"'
        
        #eng=matlab.engine.start_matlab()
        #eng.cd(r'/var/www/html/project_oral_x')
        #eng.folder_test(matlabpatientpath,nargout=0)


@app.route("/list_patient1/<hashcode>",methods=['GET',"POST"])
@app.route("/list_patient1/",methods=['GET',"POST"])
def list_patient1(hashcode=None):
    if not hashcode == None:
        #print (hashcode)
        #print (hashcode)
        global patientId
        patientId = hashcode
    
        path = "/var/www/html/project_oral_x/flaskapp/static/patientInfo"
        matlabpatientpath = path+"/"+patientId+"/"
        
        #line0 = "cd /var/www/html/project_oral_x/"
        #line1 = "sudo chmod -R 777 /var/www/html/project_oral_x/flaskapp/static/patientInfo/"
        #line2 = 'matlab -nodisplay -r \"folder_test(\''+commandpatientpath+'\');exit;"'
        
        #eng=matlab.engine.start_matlab()
        #eng.cd(r'/var/www/html/project_oral_x')
        #eng.folder_test(matlabpatientpath,nargout=0)
        
        #path = "./static/patientInfo"
        dirs = os.listdir( path )
        dirs_file = [None] *len(dirs)
        dirs.sort()
        i = 0;
        for patient in dirs:
            #pdfPath = path + "/" + patient + "/report.pdf"
            patient_path = path + "/" + patient
            dirs_time = [d for d in os.listdir(patient_path) if os.path.isdir(os.path.join(patient_path,d))]
        
            flagd = 1;
            for time in dirs_time:
                DoneFilePath = patient_path + "/" + time +"/" +"d.txt"
                #print (DoneFilePath)
                if not os.path.exists(DoneFilePath):
                    flagd = 0;
            if flagd == 1:
                dirs_file[i] = "report"
            else: 
                dirs_file[i] = "wait"
            i = i+1

        for patient in dirs:
            if patientId == patient:
                path_patient = path + "/" + patientId
                #path_patient = "/var/www/html/project_oral_x/flaskapp/static/patientInfo" + patientId
                #dirs = os.walk( path_patient )
                #list_subfolders = path_patient + "/*/"
                #dirs = glob(list_subfolders)
                d = path_patient
                dirs = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
                subfolderLength = len(dirs)
                for x in range(0, subfolderLength):
                    dirs[x] = dirs[x].replace(path_patient+"/",'')
                #print(dirs)
                # check if commented for list time
                dirs_file_time = [None] *len(dirs)
                i=0
                for time in dirs:
                    DoneFilePath = path_patient + "/" + time +"/" +"d.txt"
                    #print (DoneFilePath)
                    if os.path.exists(DoneFilePath):
                        dirs_file_time[i]="checked"
                    else :
                        dirs_file_time[i]=""
                    i=i+1
                #print(dirs_file_time)
                return render_template('list_time.html',dirs=dirs,patientId=hashcode,dirs_file_time=dirs_file_time)
    
        return render_template('list_patient.html',message='Please Input a Correct Patient ID',dirs=dirs,dirs_file=dirs_file)           

    else:
        print ("Not Received")
        return render_template('home.html')

#deprecated
@app.route('/list_patient',methods=['POST'])
def list_patient():
    global patientId
    patientId = request.form['patientId']
    path = "/var/www/html/project_oral_x/flaskapp/static/patientInfo"
    #path = "./static/patientInfo"
    dirs = os.listdir( path )
    for patient in dirs:
        if patientId == patient:
            path_patient = path + "/" + patientId
            #path_patient = "/var/www/html/project_oral_x/flaskapp/static/patientInfo" + patientId
            #dirs = os.walk( path_patient )
            #list_subfolders = path_patient + "/*/"
            #dirs = glob(list_subfolders)
            d = path_patient
            dirs = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
            subfolderLength = len(dirs)
            for x in range(0, subfolderLength):
                dirs[x] = dirs[x].replace(path_patient+"/",'')
            # check if commented for list time
            dirs_file_time = [None] *len(dirs)
            i=0
            for time in dirs:
                DoneFilePath = path_patient + "/" + time +"/" +"d.txt"
                #print (DoneFilePath)
                if os.path.exists(DoneFilePath):
                    dirs_file_time[i]="checked"
                else :
                    dirs_file_time[i]=""
                i=i+1
            #print(dirs_file_time)
            return render_template('list_time.html',dirs=dirs,patientId=hashcode,dirs_file_time=dirs_file_time)
    
    return render_template('list_patient.html',message='Please Input a Correct Patient ID',dirs=dirs)   


@app.route("/list_time_delete/<hashcode>",methods=['GET',"POST"])
@app.route("/list_time_delete/",methods=['GET',"POST"])
def list_time_delete(hashcode=None):
    if not hashcode == None:
        print (hashcode)
        print (hashcode)
        global patientId
        time_string = hashcode
    
        path = "/var/www/html/project_oral_x/flaskapp/static/patientInfo"
        #path = "./static/patientInfo"
        
        file_path = path + "/" + patientId + "/" + time_string
        
        showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ip = request.environ.get('HTTP_X_REALIP',request.remote_addr)
        trash_path ="/var/www/html/trash/" + patientId +"-_-"+ time_string+ "-_-" + showtime + "-_-" + ip
        shutil.copytree(file_path,trash_path)
        shutil.rmtree(file_path)

        dirs = os.listdir( path )
        for patient in dirs:
            if patientId == patient:
                path_patient = path + "/" + patientId
                #path_patient = "/var/www/html/project_oral_x/flaskapp/static/patientInfo" + patientId
                #dirs = os.walk( path_patient )
                #list_subfolders = path_patient + "/*/"
                #dirs = glob(list_subfolders)
                d = path_patient
                dirs = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
                subfolderLength = len(dirs)
                for x in range(0, subfolderLength):
                    dirs[x] = dirs[x].replace(path_patient+"/",'')
                # check if commented for list time
                dirs_file_time = [None] *len(dirs)
                i=0
                for time in dirs:
                    DoneFilePath = path_patient + "/" + time +"/" +"d.txt"
                    #print (DoneFilePath)
                    if os.path.exists(DoneFilePath):
                        dirs_file_time[i]="checked"
                    else :
                        dirs_file_time[i]=""
                    i=i+1
                #print(dirs_file_time)
                return render_template('list_time.html',dirs=dirs,patientId=hashcode,dirs_file_time=dirs_file_time)
    
        return render_template('list_patient.html',message='Please Input a Correct Patient ID',dirs=dirs)           

    else:
        print ("Not Received")
        return render_template('home.html')

        

@app.route("/list_time1/<hashcode>",methods=['GET',"POST"])
@app.route("/list_time1/",methods=['GET',"POST"])
def list_time1(hashcode=None):
    if not hashcode == None:
        print (hashcode)
        print (hashcode)
        global patientId
        global time_string
        id_time_string = hashcode
        patientId = id_time_string.split(':')[0]
        time_string = id_time_string.split(':')[1]
        root_path = "/var/www/html/project_oral_x/flaskapp/static/patientInfo"
        #root_path = "./static/patientInfo"
        path_patient = root_path + "/" + patientId
        #imgfilepath = "./static/patientInfo"
        imgfilepath = "/var/www/html/project_oral_x/flaskapp/static/patientInfo"
        
        d = path_patient
        dirs = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
        subfolderLength = len(dirs)
        for x in range(0, subfolderLength):
            dirs[x] = dirs[x].replace(path_patient+"/",'')
        # check if commented for list time
        dirs_file_time = [None] *len(dirs)
        i=0
        for time in dirs:
            DoneFilePath = path_patient + "/" + time +"/" +"d.txt"
            #print (DoneFilePath)
            if os.path.exists(DoneFilePath):
                dirs_file_time[i]="checked"
            else :
                dirs_file_time[i]=""
            i=i+1
        #print(dirs_file_time)
    
        jpgPath = [None] * 5
        i = 0
        jpg_name = [None] * 5
    
        for time in dirs: 
            if time_string == time:
                path_time = path_patient + "/" + time_string
                imgfilePath_time = imgfilepath + "/" + patientId + "/" + time_string
                txtPathInfo = path_patient + "/1.txt"
                with open(txtPathInfo, "r") as f:
                    contentInfo = f.read()
                f1 = open(txtPathInfo)
                lines = f1.readlines()
                print(len(lines))
                if len(lines) > 18:
                    lat_coordi = lines[lat_line].strip()
                    lng_coordi = lines[lng_line].strip()
                    gpsLocation1 = lines[18].strip()
                    patientLocation1 = lines[16].strip()
                else :
                    lat_coordi = ""
                    lng_coordi = ""
                    gpsLocation1 = ""
                    patientLocation1 = ""

                patientName1 = lines[4].strip()
                patientHeight1 = lines[6].strip()
                patientWeight1 = lines[8].strip()
                patientGender1 = lines[10].strip()
                patientAge1 = lines[12].strip()
                patientPhone1 = lines[14].strip()
                
                
                #print (lat_coordi)
                #print (lng_coordi)
            
                txtPathresult = path_time + "/result.txt"
                with open(txtPathresult, "r") as f:
                    contentresult = f.read()
                txtPathcomment = path_time + "/comment.txt"
                with open(txtPathcomment, "r") as f:
                    contentcomment = f.read()
                    for file in os.listdir(imgfilePath_time):
                        #if file.endswith(".jpg"):
                        #    jpgPath[i] = imgfilePath_time + "/" + file
                        #    print (jpgPath[i])
                        #    print (jpgPath[i])
                        #    jpgPath[i] = jpgPath[i].replace("/var/www/html/project_oral_x/flaskapp",'')
                        #    jpg_name[i] = file.replace(".jpg",'')
                        #    i = i + 1
                            
                         #if file.endswith(".jpg"):
                         #   jpgPath[i] = imgfilePath_time + "/" + file
                         #   jpg_name[i] = file.replace(".jpg",'')
                         #   i = i + 1
                        if "FL" in file:
                            jpgPath[0] = imgfilePath_time + "/" + file
                            jpgPath[0] = jpgPath[0].replace("/var/www/html/project_oral_x/flaskapp",'')
                            jpg_name[0] = file.replace(".jpg",'')
                            jpg_name[0] = file.replace(" ",' ')
                            i = i + 1
                        if "fl" in file:
                            jpgPath[1] = imgfilePath_time + "/" + file
                            jpgPath[1] = jpgPath[1].replace("/var/www/html/project_oral_x/flaskapp",'')
                            jpg_name[1] = file.replace(".jpg",'')
                            jpg_name[1] = file.replace(" ",' ')
                            i = i + 1
                        if "WL" in file:
                            jpgPath[2] = imgfilePath_time + "/" + file
                            jpgPath[2] = jpgPath[2].replace("/var/www/html/project_oral_x/flaskapp",'')
                            jpg_name[2] = file.replace(".jpg",'')
                            jpg_name[2] = file.replace(" ",' ')
                            i = i + 1
                        if "wl" in file:
                            jpgPath[3] = imgfilePath_time + "/" + file
                            jpgPath[3] = jpgPath[3].replace("/var/www/html/project_oral_x/flaskapp",'')
                            jpg_name[3] = file.replace(".jpg",'')
                            jpg_name[3] = file.replace(" ",' ')
                            i = i + 1
                    if jpgPath[0] == None:
                        jpgPath[0] = jpgPath[2]
                        jpg_name[0] = jpg_name[2]
                        jpgPath[1] = jpgPath[3]
                        jpg_name[1] = jpg_name[3]
                            
                            
                    if i == 4:
                        return render_template('patientView.html',patientId=patientId,time_string=time_string,contentresult=contentresult,contentInfo=contentInfo,contentcomment=contentcomment,jpgPath=jpgPath,jpgName=jpg_name,latCoordi=lat_coordi,lngCoordi=lng_coordi,patientName=patientName1,patientHeight=patientHeight1,patientWeight=patientWeight1,patientGender=patientGender1,patientAge=patientAge1,patientPhone=patientPhone1,patientLocation=patientLocation1,gpsLocation=gpsLocation1)
                    if i == 2:
                        return render_template('patientView_single.html',patientId=patientId,time_string=time_string,contentresult=contentresult,contentInfo=contentInfo,contentcomment=contentcomment,jpgPath=jpgPath,jpgName=jpg_name,latCoordi=lat_coordi,lngCoordi=lng_coordi,patientName=patientName1,patientHeight=patientHeight1,patientWeight=patientWeight1,patientGender=patientGender1,patientAge=patientAge1,patientPhone=patientPhone1,patientLocation=patientLocation1,gpsLocation=gpsLocation1)
        return render_template('list_time.html',message='Please Input a Correct Time String',dirs=dirs,patientId=patientId,dirs_file_time=dirs_file_time)   
    
    else:
        print ("Not Received")
        return render_template('home.html')
            
# deprecated
@app.route('/list_time', methods=['POST'])
def list_time():
    global patientId
    global time_string
    time_string = request.form['time_string']
    root_path = "/var/www/html/project_oral_x/flaskapp/static/patientInfo"
    #root_path = "./static/patientInfo"
    path_patient = root_path + "/" + patientId
    #imgfilepath = "./static/patientInfo"
    imgfilepath = "/static/patientInfo"

    d = path_patient
    dirs = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    subfolderLength = len(dirs)
    for x in range(0, subfolderLength):
        dirs[x] = dirs[x].replace(path_patient+"/",'')
    
    jpgPath = [None] * 5
    i = 0
    jpg_name = [None] * 5
    
    for time in dirs: 
        if time_string == time:
            path_time = path_patient + "/" + time_string
            imgfilePath_time = imgfilepath + "/" + patientId + "/" + time_string
            txtPathInfo = path_patient + "/1.txt"
            with open(txtPathInfo, "r") as f:
                contentInfo = f.read()
            f1 = open(txtPathInfo)
            lines = f1.readlines()
            #contentInfo = lines #
            lat_coordi = contentInfo#lines[lat_line].strip()
            lng_coordi = contentInfo#lines[lng_line].strip()
            patientName1 = lines[5].strip()
            patientHeight1 = lines[7].strip()
            patientWeight1 = lines[9].strip()
            patientGender1 = lines[11].strip()
            patientAge1 = lines[13].strip()
            patientPhone1 = lines[15].strip()
            patientLocation1 = contentInfo#lines[17].strip()
            gpsLocation1 = contentInfo#line[19].strip()
            #print (lat_coordi)
            #print (lng_coordi)
            print(patientName)
            
            txtPathresult = path_time + "/result.txt"
            with open(txtPathresult, "r") as f:
                contentresult = f.read()
            txtPathcomment = path_time + "/comment.txt"
            with open(txtPathcomment, "r") as f:
                contentcomment = f.read()
                for file in os.listdir(path_time):
                    #if file.endswith(".jpg"):
                     #   jpgPath[i] = imgfilePath_time + "/" + file
                     #   jpg_name[i] = file.replace(".jpg",'')
                     #   i = i + 1
                    if "FL" in file:
                        jpgPath[0] = imgfilePath_time + "/" + file
                        jpgName[0] = file.replace(".jpg",'')
                        i = i + 1
                    if "fl" in file:
                        jpgPath[1] = imgfilePath_time + "/" + file
                        jpgName[1] = file.replace(".jpg",'')
                        i = i + 1
                    if "WL" in file:
                        jpgPath[2] = imgfilePath_time + "/" + file
                        jpgName[2] = file.replace(".jpg",'')
                        i = i + 1
                    if "wl" in file:
                        jpgPath[3] = imgfilePath_time + "/" + file
                        jpgName[3] = file.replace(".jpg",'')
                        i = i + 1
                if jpgPath[0] == None:
                    jpgPath[0] = jpgPath[2]
                    jpgName[0] = jpgName[2]
                    jpgPath[1] = jpgPath[3]
                    jpgName[1] = jpgName[3]
                    
                if i == 4:
                    return render_template('patientView.html',patientId=patientId,contentresult=contentresult,contentInfo=contentInfo,contentcomment=contentcomment,jpgPath=jpgPath,jpgName=jpg_name,latCoordi=lat_coordi,lngCoordi=lng_coordi,patientName=patientName1,patientHeight=patientHeight1,patientWeight=patientWeight1,patientGender=patientGender1,patientAge=patientAge1,patientPhone=patientPhone1,patientLocation=patientLocation1,gpsLocaction=gpsLocation1)
                if i == 2:
                    return render_template('patientView_single.html',patientId=patientId,contentresult=contentresult,contentInfo=contentInfo,contentcomment=contentcomment,jpgPath=jpgPath,jpgName=jpg_name,latCoordi=lat_coordi,lngCoordi=lng_coordi,patientName=patientName,patientHeight=patientHeight,patientWeight=patientWeight,patientGender=patientGender,patientAge=patientAge,patientPhone=patientPhone,patientLocation=patientLocation,gpsLocaction=gpsLocation)
    return render_template('list_time.html',message='Please Input a Correct Time String',dirs=dirs)         


@app.route('/doctor_comment_submitted', methods=['POST'])
def patientView():
    qualityImage = request.form['qualityImage']
    impression = request.form['impression']
    autofl = request.form['autofl']
    cancerORnot = request.form['cancerORnot']
    biopsyORnot = request.form['biopsyORnot']
    commenta = request.form['comment']
    patientId = request.form['patientId']
    time_string = request.form['time_string']
    #print(patientId)
    #print(time_string)
    
    if qualityImage == "Not appreciate/Not Diagnostic":
        impression = "Not appreciate/Not Diagnostic"
        autofl = "Not appreciate/Not Diagnostic"
        cancerORnot = "Not appreciate/Not Diagnostic"
        biopsyORnot = "Not appreciate/Not Diagnostic"
        commenta = "Not appreciate/Not Diagnostic"
    #print (commenta)
    
    #global patientId
    #global time_string
    time_string = time_string
    root_path = "/var/www/html/project_oral_x/flaskapp/static/patientInfo"
    #root_path = "./static/patientInfo"
    path_patient = root_path + "/" + patientId
    #imgfilepath = "./static/patientInfo"
    imgfilepath = "/static/patientInfo"

    path_time = path_patient + "/" + time_string
    #create d file
    txtPathDone = path_time + "/d.txt"
    f_d = open(txtPathDone,"w")
    f_d.close
    #create list for list time
    d = path_patient
    dirs = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    subfolderLength = len(dirs)
    for x in range(0, subfolderLength):
        dirs[x] = dirs[x].replace(path_patient+"/",'')
    # check if commented for list time
    dirs_file_time = [None] *len(dirs)
    i=0
    for time in dirs:
        DoneFilePath = path_patient + "/" + time +"/" +"d.txt"
        #print (DoneFilePath)
        if os.path.exists(DoneFilePath):
            dirs_file_time[i]="checked"
        else :
            dirs_file_time[i]=""
        i=i+1
        #print(dirs_file_time)
        
    
    jpgPath = [None] * 5
    i = 0
    jpg_name = [None] * 5
    
    for time in dirs: 
        if time_string == time:
            path_time = path_patient + "/" + time_string
            imgfilePath_time = imgfilepath + "/" + patientId + "/" + time_string
            txtPathInfo = path_patient + "/1.txt"
            with open(txtPathInfo, "r") as f:
                contentInfo = f.read()
            f1 = open(txtPathInfo)
            lines = f1.readlines()
            contentInfo = lines #
            
            if len(lines) > 18:
                lat_coordi = lines[lat_line].strip()
                lng_coordi = lines[lng_line].strip()
                gpsLocation1 = lines[18].strip()
                patientLocation1 = lines[16].strip()
            else :
                lat_coordi = ""
                lng_coordi = ""
                gpsLocation1 = ""
                patientLocation1 = ""
            
            patientName1 = lines[4].strip()
            patientHeight1 = lines[6].strip()
            patientWeight1 = lines[8].strip()
            patientGender1 = lines[10].strip()
            patientAge1 = lines[12].strip()
            patientPhone1 = lines[14].strip()
            
            
            #print (lat_coordi)
            #print (lng_coordi)
            
            txtPathresult = path_time + "/result.txt"
            with open(txtPathresult, "r") as f:
                contentresult = f.read()
            txtPathcomment = path_time + "/comment.txt"
            with open(txtPathcomment, "r") as f:
                contentcomment = f.read()
                for file in os.listdir(path_time):
                    #if file.endswith(".jpg"):
                     #   jpgPath[i] = imgfilePath_time + "/" + file
                     #   jpg_name[i] = file.replace(".jpg",'')
                     #   i = i + 1
                    if "FL" in file:
                        jpgPath[0] = imgfilePath_time + "/" + file
                        jpg_name[0] = file.replace(".jpg",'')
                        i = i + 1
                    if "fl" in file:
                        jpgPath[1] = imgfilePath_time + "/" + file
                        jpg_name[1] = file.replace(".jpg",'')
                        i = i + 1
                    if "WL" in file:
                        jpgPath[2] = imgfilePath_time + "/" + file
                        jpg_name[2] = file.replace(".jpg",'')
                        i = i + 1
                    if "wl" in file:
                        jpgPath[3] = imgfilePath_time + "/" + file
                        jpg_name[3] = file.replace(".jpg",'')
                        i = i + 1
                if jpgPath[0] == None:
                    jpgPath[0] = jpgPath[2]
                    jpg_name[0] = jpg_name[2]
                    jpgPath[1] = jpgPath[3]
                    jpg_name[1] = jpg_name[3]
                        
                with open(txtPathcomment,"w", encoding="utf8") as fo:
                    #fo.writelines(contentcomment)
                    #fo.writelines("\n\n\nDoctor Diagnositic:\n")
                    fo.writelines("\n\nQuality of Image: \n")
                    fo.writelines(qualityImage)  
                    fo.writelines("\n") 
                    fo.writelines("\nImpression: \n")
                    fo.writelines(impression)  
                    fo.writelines("\n") 
                    fo.writelines("\nAutofl: \n")
                    fo.writelines(autofl)  
                    fo.writelines("\n") 
                    fo.writelines("\nOSCC/PreCancer Lesions: \n")
                    fo.writelines(cancerORnot)  
                    fo.writelines("\n")     
                    fo.writelines("\nBiopsy advised: \n")
                    fo.writelines(biopsyORnot)  
                    fo.writelines("\n") 
                    fo.writelines("\nOther Comment: \n")
                    fo.writelines(commenta)  
                    fo.writelines("\n") 
                    #showtime = strftime("%Y-%m-%d %H:%M:%S %Z", localtime())
                    time_india = timezone('Asia/Kolkata')
                    india_time = datetime.now(time_india)
                    showtime = india_time.strftime('%Y-%m-%d_%H:%M:%S %Z')
                    fo.writelines(showtime)
                    ip = request.environ.get('HTTP_X_REALIP',request.remote_addr)
                    fo.writelines("   : ")
                    fo.writelines(ip)
                with open(txtPathcomment,"r") as f:
                     contentcomment = f.read()
   
                import_data(root_path,patientId)
                return render_template('list_time.html',dirs=dirs,patientId=patientId,dirs_file_time=dirs_file_time)
                #if i == 4:
                #    return render_template('patientView.html',patientId=patientId,contentresult=contentresult,contentInfo=contentInfo,contentcomment=contentcomment,jpgPath=jpgPath,jpgName=jpg_name,latCoordi=lat_coordi,lngCoordi=lng_coordi,patientName=patientName1,patientHeight=patientHeight1,patientWeight=patientWeight1,patientGender=patientGender1,patientAge=patientAge1,patientPhone=patientPhone1,patientLocation=patientLocation1,gpsLocation=gpsLocation1)
                #if i == 2:
                #    return render_template('patientView_single.html',patientId=patientId,contentresult=contentresult,contentInfo=contentInfo,contentcomment=contentcomment,jpgPath=jpgPath,jpgName=jpg_name,latCoordi=lat_coordi,lngCoordi=lng_coordi,patientName=patientName1,patientHeight=patientHeight1,patientWeight=patientWeight1,patientGender=patientGender1,patientAge=patientAge1,patientPhone=patientPhone1,patientLocation=patientLocation1,gpsLocation=gpsLocation1)

if __name__ =='__main__':
    app.run()
