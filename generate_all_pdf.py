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


def import_data(path,patientId):
    path_patient = path +"/"+ patientId
    d = path_patient
    dirs = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    generate_pdfa(dirs,path_patient,patientId)
    flagd = 1;
    for time in dirs:
        DoneFilePath = time +"/" +"d.txt"
        #print (DoneFilePath)
        if not os.path.exists(DoneFilePath):
            flagd = 0;
    print (flagd)
    if flagd == 1:
        print(1)
        #send_email('biomedical.uaosc@gmail.com','biomedical','biomedical.uaosc@gmail.com',patientId,' Docter checked. \n PDF report generated OR updated. \n Use our mobile app or website to check. ')  

def generate_pdfa( dirs,path_patient,patientId ):
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
    c.drawImage(image_wl,350,290,width=160,height=160)
    c.drawString(350,260,"Figure 2, Adjusted Img.")    
    
    c.showPage()


path = "/var/www/html/project_oral_x/flaskapp/static/patientInfo"
dirs = os.listdir( path )
for patient in dirs:
    import_data(path,patient)
