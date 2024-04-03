import flywheel
import json
import pandas as pd
from datetime import datetime
import re

#  Module to identify the correct template use for the subject VBM analysis based on age at scan
#  Need to get subject identifiers from inside running container in order to find the correct template from the SDK

def get_demo():

    data = []
    age = []
    sex = []
    # Read config.json file
    p = open('/flywheel/v0/config.json')
    config = json.loads(p.read())

    # Read API key in config file
    api_key = (config['inputs']['api-key']['key'])
    fw = flywheel.Client(api_key=api_key)
    gear = 'synthseg'
    
    # Get the input file id
    input_file_id = (config['inputs']['input']['hierarchy']['id'])
    print("input_file_id is : ", input_file_id)
    input_container = fw.get(input_file_id)

    # Get the session id from the input file id
    # & extract the session container
    session_id = input_container.parents['session']
    session_container = fw.get(session_id)
    session = session_container.reload()
    print("subject label: ", session.subject.label)
    print("session label: ", session.label)
    session_label = session.label
    subject_label = session.subject.label

    # -------------------  Get the subject age & matching template  -------------------  #

    # get the T2w axi dicom acquisition from the session
    # Should contain the DOB in the dicom header
    # Some projects may have DOB removed, but may have age at scan in the subject container

    for acq in session_container.acquisitions.iter():
        # print(acq.label)
        acq = acq.reload()
        if 'T2' in acq.label and 'AXI' in acq.label and 'Segmentation' not in acq.label: 
            for file_obj in acq.files: # get the files in the acquisition
                # Screen file object information & download the desired file
                if file_obj['type'] == 'dicom':
                    
                    dicom_header = fw._fw.get_acquisition_file_info(acq.id, file_obj.name)
                    try:
                        PatientSex = dicom_header.info["PatientSex"]
                    except:
                        PatientSex = "NA"
                        continue
                    print("PatientSex: ", PatientSex)

                    if 'PatientBirthDate' in dicom_header.info:
                        # Get dates from dicom header
                        dob = dicom_header.info['PatientBirthDate']
                        seriesDate = dicom_header.info['SeriesDate']
                        # Calculate age at scan
                        age = (datetime.strptime(seriesDate, '%Y%m%d')) - (datetime.strptime(dob, '%Y%m%d'))
                        age = age.days
                    elif session.age != None: 
                        # 
                        print("Checking session infomation label...")
                        # print("session.age: ", session.age) 
                        age = int(session.age / 365 / 24 / 60 / 60) # This is in seconds
                    elif 'PatientAge' in dicom_header.info:
                        print("No DOB in dicom header or age in session info! Trying PatientAge from dicom...")
                        age = dicom_header.info['PatientAge']
                        # Need to drop the 'D' from the age and convert to int
                        age = re.sub('\D', '', age)
                        age = int(age)
                    else:
                        print("No age at scan in session info label! Ask PI...")
                        age = 0

                    if age == 0:
                        print("No age at scan - skipping")
                        exit(1)
                    # Make sure age is positive
                    elif age < 0:
                        age = age * -1
                    print("age: ", age)
    
    # assign values to lists. 
    data = [{'subject': subject_label, 'session': session_label, 'age': age, 'sex': PatientSex }]  
    # Creates DataFrame.  
    demo = pd.DataFrame(data)

    # filePath = '/flywheel/v0/output/vol.csv'
    # with open(filePath) as csv_file:
    #     vols = pd.read_csv(csv_file, index_col=None, header=0) 
    #     vols = vols.drop('subject', axis=1)

    # frames = [demo, vols]
    # df = pd.concat(frames, axis=1)

    # outdir = ('/flywheel/v0/output/hyperfine_synthseg_volume.csv')
    # df.to_csv(outdir)

    print("Demographics: ", subject_label, session_label, age, PatientSex)
    return subject_label, session_label, age, PatientSex




