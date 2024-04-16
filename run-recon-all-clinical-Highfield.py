import flywheel
import os
from datetime import datetime

"""
recon-all-clinical gear job submission script
anastasia.smirnova@kcl.ac.uk, April 2024

This script will submit a recon-all-clinical job for every T2w (or T1w) anatomical in the project
and is is run from local machine
Gear rules that have now been setup for this gear hopefully made this reduneant and will trigger automatically. 
However if there are new scans or ammendments it may be useful. 

Usage:
1. Setup Flywheel CLI and login locally
2. Install flywheel-sdk: pip install flywheel-sdk
3. Set the group_name and project_name variables below
4. Adjust the file_ojb.name if statement to match the anatomical you want to run SynthSeg on
5. Run the script: python run-SynthSeg.py

"""

# Setup connection to flywheel client
api_key = os.environ.get('FW_CLI_API_KEY') # This is the API key for the flywheel instance, saved as an environment variable
fw = flywheel.Client(api_key=api_key)

# Define the project we're working in
group_name = "global_map"
project_names = ["UCT-Khula-Highfield"]
#TODO: "UCT-Khula-Highfield" <- point to T2 - use synthse setter not in name
 # Initialize gear_job_list
job_list = list()
inputs = {}

# Define the gear we're running
recon_all_clinical_gear =  fw.lookup('gears/recon-all-clinical')
for project_name in project_names:
    project = fw.lookup(f"{group_name}/{project_name}")

    # Because these are anatomicals PER subject, we'll collect T1's or T2's over subjects:
    for subject in project.subjects.iter():

        # The only way to get to acquisitions is to go through the sessions
        for session in subject.sessions.iter():
            session = session.reload()
            print("parsing... ", subject.label, session.label)
            
                
            for acq in session.acquisitions.iter():
                # Now we have to look at every file in every acquisition, in every session.
                for file_obj in acq.files:
                    if 'ABCD_T2W_spc_vnav' in acq.label or 'ABCD_T2w_spc_vNav' in acq.label:
                        # Exclude this setter nonsense
                        if 'setter' in file_obj.name or 'vNav_e' in file_obj.name:
                            continue

                        # We only want anatomical Nifti's              
                        if file_obj.type == 'nifti' and file_obj.classification.get('Intent') == ['Structural']: # edit cause orig broke if Intent was empty
                            # print("file name is: ", file_obj.name, "file type is: ", file_obj.type, " & Intent is: ", file_obj.classification.get('Intent'))
                                        
                            # Check if this is a T2
                            if file_obj.classification.get('Measurement') == ['T2']:
                                input_label = 'input'
                                inputs[input_label] = file_obj
                                print("Found T2w: ", file_obj.name)


            try:
            # The destination for this anlysis will be on the session
                dest = session
                time_fmt = '%d-%m-%Y_%H-%M-%S'
                analysis_label = f'Recon_all_clinical_{datetime.now().strftime(time_fmt)}' #TODO: fix typo
                job_id = recon_all_clinical_gear.run(analysis_label=analysis_label, inputs=inputs, destination=dest, config={})
                job_list.append(job_id)
                print("Submitting Job: Check Jobs Log", dest.label)
            except:
               print("BOOP: Job cannot be sent.. No files for session??", dest.label)