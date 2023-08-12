import pydicom
from pydicom.uid import generate_uid
import names
from datetime import datetime
from random import randint, randrange, choice
import os


def create_new_dicom(original_file,new_file):
    ds = pydicom.read_file(original_file,force=True)

    ds.SOPInstanceUID = str(generate_uid())
    ds.SeriesInstanceUID = str(generate_uid())
    ds.PatientName = names.get_full_name()
    ds.PatientSex= choice(['M','F'])
    ds.AccessionNumber=str(datetime.now())
    ds.PatientBirthDate=str(datetime.now().strftime("%d-%m-%Y"))
    ds.SeriesNumber= str(randint(1,99))
    ds.PatientID = f'{str(randint(10023430, 99999923423))}'
    ds.StudyDate = f'{datetime.now().strftime("%Y-%m-%d")}'
    ds.StudyID=str(randint(100000,999999))


    ds.StudyTime = f'{str(    datetime.now().strftime("%H%M%S.%f")[:-3])}'
    print(ds.PatientID)
#Change the directory Name To anonymize
    os.chdir('/Users/anmolchokhani/Desktop/Dicoms/dicom4/')
    new_file=str(new_file)+'.dcm'
    ds.save_as(new_file)
    
if __name__=="__main__":  
    
    original_directory_name="/Users/anmolchokhani/Desktop/Dicoms/dicomfinal2/"
    # final_directory_name=""

    for count,file in enumerate(os.listdir(original_directory_name)):
        print(count)
        file=os.path.join(original_directory_name,file)
        if os.path.isfile(os.path.join(original_directory_name,file)):
            print(file)
            create_new_dicom(file,count)


