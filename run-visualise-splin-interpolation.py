import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np

# Read data from Excel
df = pd.read_excel('/Users/flywheel/Documents/recon-all-cinical-hyperfine-analysis.xlsx')

# Initialize plot
fig, ax = plt.subplots(1, 2, figsize=(12, 6))

for person in df['person'].unique():
    person_data = df[df['person'] == person]


    list(map(set,df.values))
    # Group by age and calculate average for duplicates
    grouped_data = person_data.groupby('age').mean().reset_index()
    print(df['age'])
    # Check if there are more than 3 unique ages after grouping
    if grouped_data['age'].nunique() > 3:
        # Spline interpolation
        spline_ticv = interp1d(grouped_data['age'], grouped_data['total intracranial'], kind='cubic', fill_value="extrapolate")
        spline_wmv = interp1d(grouped_data['age'], grouped_data['general white matter'], kind='cubic', fill_value="extrapolate")
        spline_gmv = interp1d(grouped_data['age'], grouped_data['general grey matter'], kind='cubic', fill_value="extrapolate")

        # Generate more age points for a smoother curve
        age_range = np.linspace(min(grouped_data['age']), max(grouped_data['age']), 100)

        # Plot the interpolated curves
        ax[0].plot(age_range, spline_ticv(age_range), label=f'person {person}')
        ax[1].plot(age_range, spline_wmv(age_range), label=f'person {person}')
        ax[2].plot(age_range, spline_gmv(age_range), label=f'person {person}')

# Set up the height plot
ax[0].set_title('TICV vs age')
ax[0].set_xlabel('age (months)')
ax[0].set_ylabel('TICV')
ax[0].legend()

# Set up the weight plot
ax[1].set_title('GWM vs age')
ax[1].set_xlabel('age (months)')
ax[1].set_ylabel('GWM')
ax[1].legend()

# Set up the weight plot
ax[1].set_title('GGM vs age')
ax[1].set_xlabel('age (months)')
ax[1].set_ylabel('GGM')
ax[1].legend()

# Display the plots
plt.tight_layout()
plt.show()