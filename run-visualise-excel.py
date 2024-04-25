
import matplotlib.pyplot as plt

import pandas as pd
highfieldDf = pd.read_csv('/Users/flywheel/Documents/fw-recon-all-clinical-data-analysis/recon-all-cinical-highfield.csv')
highfieldDf['software'] = 'Recon-All-Clinical'  # Or use a condition-based approach if applicable
highfieldDf['magnetic_field'] = 'HighField'  # Or use a condition-based approach if applicable

lowfieldDf = pd.read_csv('/Users/flywheel/Documents/fw-recon-all-clinical-data-analysis/recon-all-cinical-hyperfine.csv')
lowfieldDf['software'] = 'Recon-All-Clinical'  # Or use a condition-based approach if applicable
lowfieldDf['magnetic_field'] = 'LowField'  # Or use a condition-based approach if applicable

highfieldSynthSegDf = pd.read_csv('/Users/flywheel/Documents/fw-recon-all-clinical-data-analysis/UCT-Khula-Highfield-synthseg-0.1.3-volumes.csv')
highfieldSynthSegDf['software'] = 'SynthSeg'  # Or use a condition-based approach if applicable
highfieldSynthSegDf['magnetic_field'] = 'HighField'  # Or use a condition-based approach if applicable

lowfieldSynthSegDf = pd.read_csv('/Users/flywheel/Documents/fw-recon-all-clinical-data-analysis/UCT-Khula-Hyperfine-synthseg-0.1.3-volumes.csv')
lowfieldSynthSegDf['software'] = 'SynthSeg'  # Or use a condition-based approach if applicable
lowfieldSynthSegDf['magnetic_field'] = 'LowField'  # Or use a condition-based approach if applicable


combined_df = pd.concat([highfieldDf, lowfieldDf,highfieldSynthSegDf, lowfieldSynthSegDf], ignore_index=True)
combined_df.to_csv('/Users/flywheel/Documents/fw-recon-all-clinical-data-analysis/combined_data.csv', index=False)


