#TODO: Clean up the gear a little bit 
#TODO: Add some info to the README.md etc
#TODO: add demographics capture
#TODO: gestational age 
# comparisons between high and low field
#Overall arche
#caudate, hippocampus, amygdala <- look at variability
#icc between high and low field <- lower icc fpor smaller regions
#narrative: tool development, scalability, validation testing: curves look like expected
#apply to clinical data <- can do stuff with clinical data
#Plots go in results
#wrapper for scalability 
#re run ? remove data that didn't work - 30 % of infants move during scan


import flywheel
import os
from pathlib import Path
import pathvalidate as pv
import pandas as pd 

api_key = os.environ.get('FW_CLI_API_KEY') # This is the API key for the flywheel instance, saved as an environment variable
fw = flywheel.Client(api_key=api_key)

# Define the project we're working in
group_name = "global_map"
project_names = ["UCT-Khula-Hyperfine"]
outputs = {}
# preallocate lists
df = []
sub = []
ses = []

# Create a work directory in our local "home" directory
work_dir = Path(Path.home()/'fw/analysis/', platform='auto')

# If it doesn't exist, create it
if not work_dir.exists():
    work_dir.mkdir(parents = True)

gear = 'recon-all-clinical'


# Define the gear we're running
recon_all_clinical_gear =  fw.lookup('gears/'+gear)
for project_name in project_names:
    project = fw.lookup(f"{group_name}/{project_name}")
    # Create a custom path for our project (we may run this on other projects in the future) and create if it doesn't exist
    project_path = pv.sanitize_filepath(work_dir/project.label/gear, platform='auto')
    if not project_path.exists():
        project_path.mkdir(parents = True)

    # Because these are anatomicals PER subject, we'll collect T1's or T2's over subjects:
    for subject in project.subjects.iter():
        sub_label = subject.label
        # The only way to get to acquisitions is to go through the sessions
        for session in subject.sessions.iter():
            ses_label = session.label
            session = session.reload()
            print("parsing... ", subject.label, session.label)
            
            for analysis in session.analyses:
                # print('Analysis found: '+str(analysis.label))
                if "Recon_all_clinical" in analysis.label and analysis.get("job").get("state") == "complete":
                    print('Analysis found is Recon_all_clinical & complete:'+str(analysis.label))
                    for analysis_file in analysis.files:
                        if "synthseg.qc.csv" in analysis_file.name or "synthseg.vol.csv" in analysis_file.name:
                            file = analysis_file
                            output_label = 'output'
                            outputs[output_label] = file
                            print("Found " + output_label)

                            analysis.download_tar(file.name)

                            print(sub_label, file.name)

                            # Sanitize our filename and parent path
                            download_dir = pv.sanitize_filepath(project_path/sub_label/ses_label,platform='auto')
                            
                            # Create the path
                            if not download_dir.exists():
                                download_dir.mkdir(parents=True)
                            download_path = download_dir/file.name
                            
                            # Download the file
                            print('downloading file', ses_label, file.name)
                            file.download(download_path)
            
                            sub.append(sub_label)
                            ses.append(ses_label)

                            with open(download_path) as csv_file:
                                results = pd.read_csv(csv_file, index_col=None, header=0) 
                                df.append(results)


# # # write DataFrame to an excel sheet 
# df = pd.concat(df, axis=0, ignore_index=True)
# outdir = os.path.join(project_path, 'highfield_synthseg_vol.csv')
# df.to_csv(outdir)

# # write demo to an excel sheet 
# dict = {'subject': sub, 'session': ses}  
# demo = pd.DataFrame(dict)
# demoOutdir = os.path.join(project_path, 'demo.csv')
# demo.to_csv(demoOutdir)