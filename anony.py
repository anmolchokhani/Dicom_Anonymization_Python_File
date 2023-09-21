import os
import pydicom as dicom
from pydicom.uid import generate_uid
from faker import Faker
import datetime
import random
import sys
import glob


def keep_as_itis(input_path, save_path):
    fake = Faker()
    genders = ['M', 'F']
    patient_metadata = {
        'name': fake.name(),
        'gender': random.choice(genders),
        'id': fake.pystr_format(),
        'dob': fake.date_between(start_date='-70y', end_date='today'),
        'institution': fake.company(),
        'accession': fake.pystr_format(),
        "Modality": "CR"
    }
    series_metadata = {
        'series_instance_uid': generate_uid(),
        'study_instance_uid': generate_uid(),
    } 
    series_identifier = series_metadata['series_instance_uid']
    study_identifier = series_metadata['study_instance_uid']

    instance_number = 0

    dcm_obj = dicom.read_file(input_path)

    updatedSOPInstanceUID = "{}.{}".format(series_identifier, str(instance_number))
    dcm_obj.SOPInstanceUID = updatedSOPInstanceUID

#     dcm_obj.SeriesInstanceUID = series_identifier
#     dcm_obj.StudyInstanceUID = study_identifier
#     setattr(dcm_obj, "InstanceNumber", instance_number)

    dcm_obj.PatientName = f"testbp_{dcm_obj.get('PatientName', dcm_obj.get('SeriesInstanceUID',''))}"
    dcm_obj.PatientBirthDate = patient_metadata.get('dob', datetime.date.today())
    dcm_obj.PatientSex = patient_metadata.get('gender', 'M')
    dcm_obj.PatientID = patient_metadata.get('id')
    
    dcm_obj.SeriesInstanceUID = series_identifier
    dcm_obj.StudyInstanceUID = study_identifier
    setattr(dcm_obj, "InstanceNumber", instance_number)
    
    dcm_obj.AccessionNumber = patient_metadata.get('accession')
    dcm_obj.InstitutionName = patient_metadata.get('institution')
    dcm_obj.Modality = patient_metadata.get('Modality', "CR")

    if save_path:
        # out_path = os.path.join(save_path, os.path.basename(input_path)+".dcm")
        # os.makedirs(save_path, exist_ok=True)
        dicom.write_file(save_path, dcm_obj)
    else:
        dicom.write_file(input_path, dcm_obj)

        

import os
dir='/Users/anmolchokhani/Desktop/anony/DICOMS'
all_files=os.listdir(dir)
save_paths='/Users/anmolchokhani/Desktop/anony/dicomfinal'
from tqdm import tqdm
count=0
for files in tqdm(all_files):
    to_anonymize= os.path.join(dir,files)
    anonymized=os.path.join(save_paths,files)
    keep_as_itis(to_anonymize,anonymized)
    print(count+1)
