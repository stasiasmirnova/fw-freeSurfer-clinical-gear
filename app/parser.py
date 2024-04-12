"""Parser module to parse output."""

from typing import Tuple
from flywheel_gear_toolkit import GearToolkitContext
import os
import pandas as pd

def parseOutput():

    os.rename('/flywheel/v0/output/samseg.stats', '/flywheel/v0/output/samseg_stats.csv')
    samseg = pd.read_csv('/flywheel/v0/output/samseg_stats.csv', header=None, index_col=None)
    os.rename('/flywheel/v0/output/sbtiv.stats', '/flywheel/v0/output/sbtiv_stats.csv')
    sbtiv = pd.read_csv('/flywheel/v0/output/sbtiv_stats.csv', header=None, index_col=None)
    df = samseg.append(sbtiv)
    print(df)

    selected_columns = df.iloc[:, [0, 1]]
    # print(selected_columns.head())
    # Remove '# Measure ' from the entire DataFrame
    selected_columns = selected_columns.replace('# Measure ', '', regex=True)
    # Transpose the DataFrame
    transposed_df = selected_columns.T
    # Save the transposed DataFrame to a new CSV file
    transposed_df.to_csv('/flywheel/v0/output/vols.csv', index=False, header=False)