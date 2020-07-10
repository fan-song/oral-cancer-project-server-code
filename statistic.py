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

qualityImageLine = 3
impressionLine = 6
afLine = 9

path = "/var/www/html/project_oral_x/flaskapp/static/patientInfo"
sort_path = "/var/www/html/project_oral_x/flaskapp/sorted_images"
#path ="./static/patientInfo"
dirs = os.listdir( path )
dirs.sort()

number_good_imQuality_hm = 0
number_fair_imQuality_hm = 0
number_poor_imQuality_hm = 0
number_ND_imQuality_hm = 0
number_OSCC_impression_hm = 0
number_precancer_impression_hm =0
number_benign_impression_hm = 0
number_normal_impression_hm = 0
number_ND_impression_hm = 0
number_other_impression_hm = 0
number_loss_and_caner_hm = 0
number_loss_af_hm = 0
number_gain_af_hm = 0
number_normal_af_hm = 0
number_ND_af_hm = 0
number_total_hm = 0 

number_good_imQuality_p = 0
number_fair_imQuality_p = 0
number_poor_imQuality_p = 0
number_ND_imQuality_p = 0
number_OSCC_impression_p = 0
number_precancer_impression_p =0
number_benign_impression_p = 0
number_normal_impression_p = 0
number_ND_impression_p = 0
number_other_impression_p = 0
number_loss_and_caner_p = 0
number_gain_and_caner_p = 0
number_normal_and_caner_p = 0
number_ND_and_caner_p = 0
number_loss_af_p = 0
number_gain_af_p = 0
number_normal_af_p = 0
number_ND_af_p = 0
number_total_p = 0 

for patient in dirs:
    #pdfPath = path + "/" + patient + "/report.pdf"
    patient_path = path + "/" + patient
    InfoFilePath = patient_path + "/1.txt"
    f10 = open(InfoFilePath)
    lines = f10.readlines()
    if len(lines)<18 :
        #print(patient)
        print('')
    else:
        lat_coordi = lines[20].strip()
        #print(lat_coordi)
        if lat_coordi == "0.0":
            #print(patient)
            print('')
        
    dirs_time = [d for d in os.listdir(patient_path) if os.path.isdir(os.path.join(patient_path,d))]
    for time in dirs_time:
        if "wholeMouth" in time:
            time_path = patient_path + "/" + time
            dirs_files = os.listdir( time_path )
            #print (patient)
            #print (time)
            commentFilePath = patient_path + "/" + time + "/comment.txt"
            f1 = open(commentFilePath)
            lines = f1.readlines()
            #print(lines)
            #print(len(lines))
            if len(lines)>10:
                imageQuality = lines[qualityImageLine].strip()
                impression = lines[impressionLine].strip()
                af = lines[afLine].strip()
                #print(af)
            
                number_total_hm = number_total_hm +1
                if imageQuality == "good":
                    number_good_imQuality_hm = number_good_imQuality_hm + 1
                if imageQuality == "fair":
                    number_fair_imQuality_hm = number_fair_imQuality_hm + 1
                if imageQuality == "poor":
                    number_poor_imQuality_hm = number_poor_imQuality_hm + 1
                if imageQuality == "Not appreciate/Not Diagnostic":
                    number_ND_imQuality_hm = number_ND_imQuality_hm +1
                if impression == "OSCC":
                    number_OSCC_impression_hm = number_OSCC_impression_hm + 1
                    for file in dirs_files:
                        if "FL" in file:
                            src = time_path + "/" + file
                            dst = sort_path + "/cancer/wholeMouth/af/" + file
                            shutil.copy(src,dst)
                        if "WL" in file:
                            src = time_path + "/" + file
                            dst = sort_path + "/cancer/wholeMouth/whiteLight/" + file
                            shutil.copy(src,dst)
                if impression == "Benign":
                    number_benign_impression_hm = number_benign_impression_hm + 1
                    for file in dirs_files:
                        if "FL" in file:
                            src = time_path + "/" + file
                            dst = sort_path + "/benign/wholeMouth/af/" + file
                            shutil.copy(src,dst)
                        if "WL" in file:
                            src = time_path + "/" + file
                            dst = sort_path + "/benign/wholeMouth/whiteLight/" + file
                            shutil.copy(src,dst)
                if impression == "Normal/Variation":
                    number_normal_impression_hm = number_normal_impression_hm + 1
                    for file in dirs_files:
                        if "FL" in file:
                            src = time_path + "/" + file
                            dst = sort_path + "/normal/wholeMouth/af/" + file
                            shutil.copy(src,dst)
                        if "WL" in file:
                            src = time_path + "/" + file
                            dst = sort_path + "/normal/wholeMouth/whiteLight/" + file
                            shutil.copy(src,dst)
                if impression == "Not appreciate/Not Diagnostic":
                    number_ND_impression_hm = number_ND_impression_hm + 1
                    for file in dirs_files:
                        if "FL" in file:
                            src = time_path + "/" + file
                            dst = sort_path + "/ND/wholeMouth/af/" + file
                            shutil.copy(src,dst)
                        if "WL" in file:
                            src = time_path + "/" + file
                            dst = sort_path + "/ND/wholeMouth/whiteLight/" + file
                            shutil.copy(src,dst)
                if impression == "Others":
                    number_other_impression_hm = number_other_impression_hm + 1
                    for file in dirs_files:
                        if "FL" in file:
                            src = time_path + "/" + file
                            dst = sort_path + "/other/wholeMouth/af/" + file
                            shutil.copy(src,dst)
                        if "WL" in file:
                            src = time_path + "/" + file
                            dst = sort_path + "/other/wholeMouth/whiteLight/" + file
                            shutil.copy(src,dst)
                if (impression == "Lichen Planus" or impression == "Homogenous Leukoplakia" or impression == "Speckled Leukoplakia"  or impression == "Tobacco Pouch Keratosis" or impression == "Veruccous Leukoplakia" or impression == "OSMF"):
                    number_precancer_impression_hm = number_precancer_impression_hm + 1
                    for file in dirs_files:
                        if "FL" in file:
                            src = time_path + "/" + file
                            dst = sort_path + "/precancer/wholeMouth/af/" + file
                            shutil.copy(src,dst)
                        if "WL" in file:
                            src = time_path + "/" + file
                            dst = sort_path + "/precancer/wholeMouth/whiteLight/" + file
                            shutil.copy(src,dst)
                if af == "loss" and not (impression == "Others" or impression =="Normal/Variation" or impression =="Not appreciate/Not Diagnostic" or impression =="Benign"):
                    number_loss_and_caner_hm = number_loss_and_caner_hm + 1
                if af =="loss":
                    number_loss_af_hm = number_loss_af_hm + 1
                if af =="gain":
                    number_gain_af_hm = number_gain_af_hm + 1
                if af =="normal":
                    number_normal_af_hm = number_normal_af_hm + 1
                if af =="Not appreciate/Not Diagnostic":
                    number_ND_af_hm = number_ND_af_hm + 1
                    
        if "wholeMouth" not in time:
            time_path = patient_path + "/" + time
            dirs_files = os.listdir( time_path )
            #print (patient)
            #print (time)
            commentFilePath = patient_path + "/" + time + "/comment.txt"
            f1 = open(commentFilePath)
            lines = f1.readlines()
            #print(lines)
            #print(len(lines))
            if len(lines)>10:
                imageQuality = lines[qualityImageLine].strip()
                impression = lines[impressionLine].strip()
                af = lines[afLine].strip()
                #print(af)
            
                number_total_p = number_total_p +1
                if imageQuality == "good":
                    number_good_imQuality_p = number_good_imQuality_p + 1
                if imageQuality == "fair":
                    number_fair_imQuality_p = number_fair_imQuality_p + 1
                if imageQuality == "poor":
                    number_poor_imQuality_p = number_poor_imQuality_p + 1
                if imageQuality == "Not appreciate/Not Diagnostic":
                    number_ND_imQuality_p = number_ND_imQuality_p +1
                if impression == "OSCC":
                    #print("OSCC")
                    #print(patient)
                    number_OSCC_impression_p = number_OSCC_impression_p + 1
                    if len(dirs_files) == 7:
                        for file in dirs_files:
                            if "FL" in file:
                                src = time_path + "/" + file
                                dst = sort_path + "/cancer/probe/af/" + file
                                shutil.copy(src,dst)
                            if "WL" in file:
                                src = time_path + "/" + file
                                dst = sort_path + "/cancer/probe/whiteLight/" + file
                                shutil.copy(src,dst)
                if impression == "Benign":
                    #print("Benign")
                    #print(patient)
                    number_benign_impression_p = number_benign_impression_p + 1
                    if len(dirs_files) == 7: 
                        for file in dirs_files:
                            if "FL" in file:
                                src = time_path + "/" + file
                                dst = sort_path + "/benign/probe/af/" + file
                                shutil.copy(src,dst)
                            if "WL" in file:
                                src = time_path + "/" + file
                                dst = sort_path + "/benign/probe/whiteLight/" + file
                                shutil.copy(src,dst)
                if impression == "Normal/Variation":
                    #print("Normal")
                    #print(patient)					
                    number_normal_impression_p = number_normal_impression_p + 1
                    if len(dirs_files) == 7:
                        for file in dirs_files:
                            if "FL" in file:
                                src = time_path + "/" + file
                                dst = sort_path + "/normal/probe/af/" + file
                                shutil.copy(src,dst)
                            if "WL" in file:
                                src = time_path + "/" + file
                                dst = sort_path + "/normal/probe/whiteLight/" + file
                                shutil.copy(src,dst)
                if impression == "Not appreciate/Not Diagnostic":
                    print(patient)
                    number_ND_impression_p = number_ND_impression_p + 1
                    if len(dirs_files) == 7:
                        for file in dirs_files:
                            if "FL" in file:
                                src = time_path + "/" + file
                                dst = sort_path + "/ND/probe/af/" + file
                                shutil.copy(src,dst)
                            if "WL" in file:
                                src = time_path + "/" + file
                                dst = sort_path + "/ND/probe/whiteLight/" + file
                                shutil.copy(src,dst)
                if impression == "Others":
                    #print("Other")
                    #print(patient)
                    number_other_impression_p = number_other_impression_p + 1
                    if len(dirs_files) == 7 :
                        for file in dirs_files:
                            if "FL" in file:
                                src = time_path + "/" + file
                                dst = sort_path + "/other/probe/af/" + file
                                shutil.copy(src,dst)
                            if "WL" in file:
                                src = time_path + "/" + file
                                dst = sort_path + "/other/probe/whiteLight/" + file
                                shutil.copy(src,dst)
                if impression == "Lichen Planus" or impression == "Homogenous Leukoplakia" or impression == "Speckled Leukoplakia"  or impression == "Tobacco Pouch Keratosis" or impression == "Veruccous Leukoplakia" or impression == "OSMF":
                    #print("Pre")
                    #print(patient)
                    number_precancer_impression_p = number_precancer_impression_p + 1
                    if len(dirs_files) == 7:
                        for file in dirs_files:
                            if "FL" in file:
                                src = time_path + "/" + file
                                dst = sort_path + "/precancer/probe/af/" + file
                                shutil.copy(src,dst)
                            if "WL" in file:
                                src = time_path + "/" + file
                                dst = sort_path + "/precancer/probe/whiteLight/" + file
                                shutil.copy(src,dst)
                if af == "loss" and not (impression == "Others" or impression =="Normal/Variation" or impression =="Not appreciate/Not Diagnostic" or impression =="Benign"):
                    number_loss_and_caner_p = number_loss_and_caner_p + 1
                if af == "gain" and not (impression == "Others" or impression =="Normal/Variation" or impression =="Not appreciate/Not Diagnostic" or impression =="Benign"):
                    number_gain_and_caner_p = number_gain_and_caner_p + 1
                if af == "normal" and not (impression == "Others" or impression =="Normal/Variation" or impression =="Not appreciate/Not Diagnostic" or impression =="Benign"):
                    number_normal_and_caner_p = number_normal_and_caner_p + 1
                if af == "Not appreciate/Not Diagnostic" and not (impression == "Others" or impression =="Normal/Variation" or impression =="Not appreciate/Not Diagnostic" or impression =="Benign"):
                    number_ND_and_caner_p = number_ND_and_caner_p + 1
                if af =="loss":
                    number_loss_af_p = number_loss_af_p + 1
                    #print(patient)
                    #print(time)
                if af =="gain":
                    number_gain_af_p = number_gain_af_p + 1
                if af =="normal":
                    number_normal_af_p = number_normal_af_p + 1
                if af =="Not appreciate/Not Diagnostic":
                    number_ND_af_p = number_ND_af_p + 1

txtPathStatistics = "/var/www/html/project_oral_x/flaskapp/static/statistics.txt"
with open(txtPathStatistics,"w", encoding="utf8") as fo:
    fo.writelines("\n\nTotal number of whole mouth images\n")
    fo.writelines(str(number_total_hm))
    fo.writelines("\n\nTotal number of good Image Quality whole mouth images\n")
    fo.writelines(str(number_good_imQuality_hm))  
    #fo.writelines("\n")   
    fo.writelines("\n\nTotal number of fair Image Quality whole mouth images\n")
    fo.writelines(str(number_fair_imQuality_hm))
    fo.writelines("\n\nTotal number of poor Image Quality whole mouth images\n")
    fo.writelines(str(number_poor_imQuality_hm))
    fo.writelines("\n\nTotal number of ND Image Quality whole mouth images\n")
    fo.writelines(str(number_ND_imQuality_hm))
    fo.writelines("\n\nTotal number of OSCC Impression whole mouth images\n")
    fo.writelines(str(number_OSCC_impression_hm))
    fo.writelines("\n\nTotal number of precancer Impression whole mouth images\n")
    fo.writelines(str(number_precancer_impression_hm))
    fo.writelines("\n\nTotal number of Benige Impression whole mouth images\n")
    fo.writelines(str(number_benign_impression_hm))
    fo.writelines("\n\nTotal number of Normal Impression whole mouth images\n")
    fo.writelines(str(number_normal_impression_hm))
    fo.writelines("\n\nTotal number of ND Impression whole mouth images\n")
    fo.writelines(str(number_ND_impression_hm))
    fo.writelines("\n\nTotal number of Other Impression whole mouth images\n")
    fo.writelines(str(number_other_impression_hm))
    fo.writelines("\n\nTotal number of af loss and pre/OSCC whole mouth images\n")
    fo.writelines(str(number_loss_and_caner_hm))
    fo.writelines("\n\nTotal number of loss af whole mouth images\n")
    fo.writelines(str(number_loss_af_hm))
    fo.writelines("\n\nTotal number of gain af whole mouth images\n")
    fo.writelines(str(number_gain_af_hm))
    fo.writelines("\n\nTotal number of normal af whole mouth images\n")
    fo.writelines(str(number_normal_af_hm))
    fo.writelines("\n\nTotal number of ND af whole mouth images\n")
    fo.writelines(str(number_ND_af_hm))
  
    fo.writelines("\n\n\n")        

    fo.writelines("\n\nTotal number of probe images\n")
    fo.writelines(str(number_total_p))
    fo.writelines("\n\nTotal number of good Image Quality probe images\n")
    fo.writelines(str(number_good_imQuality_p))
    fo.writelines("\n\nTotal number of fair Image Quality probe images\n")
    fo.writelines(str(number_fair_imQuality_p))
    fo.writelines("\n\nTotal number of poor Image Quality probe images\n")
    fo.writelines(str(number_poor_imQuality_p))
    fo.writelines("\n\nTotal number of ND Image Quality probe images\n")
    fo.writelines(str(number_ND_imQuality_p))
    fo.writelines("\n\nTotal number of OSCC Impression probe images\n")
    fo.writelines(str(number_OSCC_impression_p))
    fo.writelines("\n\nTotal number of precancer Impression probe images\n")
    fo.writelines(str(number_precancer_impression_p))
    fo.writelines("\n\nTotal number of Benige Impression probe images\n")
    fo.writelines(str(number_benign_impression_p))
    fo.writelines("\n\nTotal number of Normal Impression probe images\n")
    fo.writelines(str(number_normal_impression_p))
    fo.writelines("\n\nTotal number of ND Impression probe images\n")
    fo.writelines(str(number_ND_impression_p))
    fo.writelines("\n\nTotal number of Other Impression probe images\n")
    fo.writelines(str(number_other_impression_p))
    fo.writelines("\n\nTotal number of af loss and pre/OSCC probe images\n")
    fo.writelines(str(number_loss_and_caner_p))
    fo.writelines("\n\nTotal number of af gain and pre/OSCC probe images\n")
    fo.writelines(str(number_gain_and_caner_p))
    fo.writelines("\n\nTotal number of af normal and pre/OSCC probe images\n")
    fo.writelines(str(number_normal_and_caner_p))
    fo.writelines("\n\nTotal number of af ND and pre/OSCC probe images\n")
    fo.writelines(str(number_ND_and_caner_p))
    fo.writelines("\n\nTotal number of loss af probe images\n")
    fo.writelines(str(number_loss_af_p))
    fo.writelines("\n\nTotal number of gain af probe images\n")
    fo.writelines(str(number_gain_af_p))
    fo.writelines("\n\nTotal number of normal af probe images\n")
    fo.writelines(str(number_normal_af_p))
    fo.writelines("\n\nTotal number of ND af probe images\n")
    fo.writelines(str(number_ND_af_p))

               
            
print("total number of good ImQua hm images")
print(number_good_imQuality_hm)
print("total number of fair ImQua hm images")
print(number_fair_imQuality_hm)
print("total number of poor ImQua hm images")
print(number_poor_imQuality_hm)
print("total number of ND ImQua hm images")
print(number_ND_imQuality_hm)
print("total number of OSCC Impre hm images")
print(number_OSCC_impression_hm)
print("total number of precancer Impre hm images")
print(number_precancer_impression_hm)
print("total number of Benige Impre hm images")
print(number_benign_impression_hm)
print("total number of Noraml Impre hm images")
print(number_normal_impression_hm)
print("total number of ND Impre hm images")
print(number_ND_impression_hm)
print("total number of Other Impre hm images")
print(number_other_impression_hm)
print("total number of af loss and pre/OSCC hm images")
print(number_loss_and_caner_hm)
print("total number of af loss af hm images")
print(number_loss_af_hm)
print("total number of af gain af hm images")
print(number_gain_af_hm)
print("total number of af normal af hm images")
print(number_normal_af_hm)
print("total number of af ND af hm images")
print(number_ND_af_hm)
print("total number hm")
print(number_total_hm)  
  
print("")        

print("total number of good p images")
print(number_good_imQuality_p)
print("total number of fair p images")
print(number_fair_imQuality_p)
print("total number of poor p images")
print(number_poor_imQuality_p)
print("total number of ND p images")
print(number_ND_imQuality_p)
print("total number of OSCC Impre p images")
print(number_OSCC_impression_p)
print("total number of precancer Impre p images")
print(number_precancer_impression_p)
print("total number of Benige Impre p images")
print(number_benign_impression_p)
print("total number of Noraml Impre p images")
print(number_normal_impression_p)
print("total number of ND Impre p images")
print(number_ND_impression_p)
print("total number of Other Impre p images")
print(number_other_impression_p)
print("total number of af loss and pre/OSCC p images")
print(number_loss_and_caner_p)
print("total number of af gain and pre/OSCC p images")
print(number_gain_and_caner_p)
print("total number of af normal and pre/OSCC p images")
print(number_normal_and_caner_p)
print("total number of af ND and pre/OSCC p images")
print(number_ND_and_caner_p)
print("total number of af loss af p images")
print(number_loss_af_p)
print("total number of af gain af p images")
print(number_gain_af_p)
print("total number of af normal af p images")
print(number_normal_af_p)
print("total number of af ND af p images")
print(number_ND_af_p)
print("total number p")
print(number_total_p)         
