
import matplotlib.pyplot as plt

import pandas as pd
df = pd.read_excel('/Users/flywheel/Documents/recon-all-cinical-hyperfine-analysis.xlsx')

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
for person in df['person'].unique():
    person_data = df[df['person'] == person]
    grouped_data = person_data.groupby('age')

    if person_data['age'].nunique() > :
        ax[0].plot(person_data['age'], person_data['total intracranial'], label=f'person {person}')
        ax[1].plot(person_data['age'], person_data['csf'], label=f'person {person}')

ax[0].set_title('total intracranial vs Age')
ax[0].set_xlabel('Age (months)')
ax[0].set_ylabel('Brain Volume')
ax[0].legend()

ax[1].set_title('csf vs Age')
ax[1].set_xlabel('Age (months)')
ax[1].set_ylabel('csf volume')
ax[1].legend()

plt.tight_layout()
plt.show()