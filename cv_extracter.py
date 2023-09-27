import os
import PyPDF2
from PyPDF2 import PdfReader
import re

def get_category(text):
    line = text.splitlines()
    ft = line[0]
    return ft

def get_skills(text):
    s = []

    skill_keywords = ["accounts payables","accounts receivables","Excellent classroom management", "Data-driven curriculum",
 "Effectively works with parents","Differentiates instruction"," Collaborates with Colleagues",
"administrative functions", "trial balance", "banking", "budget", "bi",
"Computer Applications", "Credit", "clients", "Customer Service",
"data entry", "insurance", "inventory","Outlook", "Excel", "Word", "PowerPoint", "QuickBooks","OneNote"
"Excel", "Outlook", "PowerPoint", "Word", "mortgage loan", "Enterprise",
"policies", "QuickBooks", "Sales", "sales reports", "telecommunications",
"discharge planning", "lesson plans", "evaluate patients", "supervision","workflow",
"Highly Effective Teacher","Motivator"," Innovator", "Successful Leader","Classroom Discipline Classroom Management" ,"Creative Lesson Planning" ,"Public Speaking" ,"Active Learning"]


    for skill in skill_keywords:
        # Use a case-insensitive search to capture variations in capitalization
        if re.search(skill, text, re.IGNORECASE):
            s.append(skill)

    # return ",".join(s)
    return ",".join(s)

def get_education(text):
    e = []

    education_keywords = ["Bachelor of Business Administration","Computer Applications Specialist Certificate Program",
         "Business Training Center","Bachelor of Science : Accounting ","Bachelor of Science : Business Administration Finance",
         "Bachelor of Science","BS : Accounting Business Administration","BBA","MBA",
         "Trained as Accountant"
         ]

    for education in education_keywords:
        if re.search(education,text,re.IGNORECASE):
            e.append(education)

    # return ",".join(e)
    return ",".join(e)


def get_CV_text(path):
    reader = PdfReader(path)
    content = ""
    for pages in range(len(reader.pages)):
        page = reader.pages[pages]
        content += page.extract_text((0, 90))
        # print(page.extract_text((0, 90)))
        # print("*********************************************************")
        return content

print("Resume Matching with Job Descriptions Using PDF CVs")
print("******************************************************")
print("Select the Category:")
print("ACCOUNTANT\n",
      "ADVOCATE\n",
      "AGRICULTURE\n",
      "APPAREL\n",
      "ARTS\n",
      "AUTOMOBILE\n",
      "AVIATION\n",
      "BANKING\n",
      "BPO\n",
      "BUSINESS DEVELOPMENT\n",
      "CHEF\n",
      "CONSTRUCTION\n",
      "CONSULTANT\n",
      "DESIGNER\n",
      "DIGITAL MEDIA\n",
      "ENGINEERING\n",
      "FITNESS\n",
      "FINANCE\n",
      "HEALTHCARE\n",
      "HR\n",
      "INFORMATION TECHNOLOGY\n",
      "PUBLIC RELATIONS\n",
      "SALES\n",
      "TEACHER\n")

category_name = input()
category_name = category_name.upper()


pdf_files = "E:/CV_Extractor/Dataset/data/data/" + category_name
print(pdf_files)
cv_data = {}

for filename in os.listdir(pdf_files):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_files,filename)
        text = get_CV_text(pdf_path)
        cv_info = []
        fn = os.path.splitext(os.path.basename(pdf_path))[0]
        ct = get_category(text)
        cv_info.append(ct)
        sk = get_skills(text)
        cv_info.append(sk)
        ed = get_education(text)
        cv_info.append(ed)
        # print("ID:" + fn)
        # print("Category: " +get_category(text))
        # print("Skills: " +get_skills(text))
        # print("Education:" +get_education(text))
        cv_data[fn] = cv_info
        # print("******************************************")

print(cv_data)