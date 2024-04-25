
import pandas as pd

df_masterFile = pd.read_csv('/Users/flywheel/Documents/fw-recon-all-clinical-data-analysis/masterfile_labelled.csv')
df_demographics = pd.read_csv('/Users/flywheel/Documents/fw-recon-all-clinical-data-analysis/demographics.csv')
#write code that gets session from fly wheel and reads sex filling in empty values 


# # Setup connection to flywheel client
# api_key = os.environ.get('FW_CLI_API_KEY') # This is the API key for the flywheel instance, saved as an environment variable
# fw = flywheel.Client(api_key=api_key)

# # Define the project we're working in
# group_name = "global_map"
# project_names = ["UCT-Khula-Hyperfine"]

# for project_name in project_names:
#     project = fw.lookup(f"{group_name}/{project_name}")

#     # Because these are anatomicals PER subject, we'll collect T1's or T2's over subjects:
#     for subject in project.subjects.iter():


# # Export to Excel

# Merging the two DataFrames on the common column 'person_id'
merged_df = pd.merge(df_masterFile, df_demographics[['person', 'child_sex']], on='person', how='left')

# Mapping the 'sex' column values where 1 = 'Male' and anything else = 'Female'
merged_df['child_sex'] = merged_df['child_sex'].map({1: 'M', 2: 'F'})

# Now merged_df contains the updated 'sex' values, and you can replace the masterFile DataFrame if needed
df_masterFile['child_sex'] = merged_df['child_sex']
df_masterFile.to_excel('/Users/flywheel/Documents/fw-recon-all-clinical-data-analysis/master_file_2.xlsx')
