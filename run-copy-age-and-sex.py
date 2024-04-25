import pandas as pd

df = pd.read_csv('/Users/flywheel/Documents/fw-recon-all-clinical-data-analysis/combined_processed_output_with_sex3.csv')
#TODO: copy age & sex for same patient id + label


# Print original DataFrame
print("Original DataFrame:")
print(df)
# Function to extract the last part of the patient_info
def extract_last_part(info):
    return info.split('_')[-1]

# Apply the function to create a new column
df['info_last_part'] = df['patient_info'].apply(extract_last_part)

# Group by the extracted part and fill NA within each group based on available ages
df['age_filled'] = df.groupby('info_last_part')['age'].transform(lambda x: x.fillna(method='ffill').fillna(method='bfill'))

print("\nDataFrame with Filled Ages:")
print(df[['patient_info', 'age', 'age_filled']])
# Display the updated DataFrame
print("\nDataFrame with Extracted Info Part:")
print(df)

# Export to Excel
df.to_csv('/Users/flywheel/Documents/fw-recon-all-clinical-data-analysis/combined_processed_output_with_age_and_sex3.csv')
