import os
import pandas as pd

def process_csv_files(root_dir):
    all_data = []
    # Traverse the directory structure
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('vol.csv'):
                full_path = os.path.join(root, file)

                # Read the CSV file
                df = pd.read_csv(full_path)
                
                # Extract metadata from the directory path
                parts = os.path.normpath(full_path).split(os.sep)

                # The index '191_28097536_12M' is found 2 levels up from the file name
                patient_info = parts[-3]  # '-3' because we count from the file going up the path
                session_name = parts[-2]

                # Add the patient_info as a new column in the DataFrame
                df['patient_info'] = patient_info
                df['session_name'] = session_name
 
                if patient_info.count('_') == 2:  # Ensure the directory name has exactly two underscores
                    patient_info = patient_info.replace('M', '')
                    print(patient_info)
                    number, person, age = patient_info.split('_')
                    df['person'] = person
                    df['age'] = age
                    
                # Append to the list
                all_data.append(df)
    
    # Combine all data into a single DataFrame
    master_df = pd.concat(all_data, ignore_index=True)
    
    # Set 'patient_info' as an index column
    master_df.set_index(['person', 'age','session_name'], inplace=True)

    # Export to Excel
    master_df.to_excel(root_directory+'/output.xlsx')

# Directory containing the folders and CSV files
root_directory = '/Users/flywheel/fw/analysis/UCT-Khula-Hyperfine/recon-all-clinical'  # Replace with your root directory
process_csv_files(root_directory)
