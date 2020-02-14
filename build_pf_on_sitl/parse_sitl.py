import glob

import pandas as pd

from aidapy.tools.sitl_parsing import convert_sitl,\
    read_and_transform, generate_output_path


input_path = "SITL_reports_*/*.txt"
files = glob.glob(input_path)

for file_ in files:
    convert_sitl(file_)

converted_path = generate_output_path(input_path)
converted_files = glob.glob(converted_path)

df_list = []
for file_ in converted_files:
    df = read_and_transform(file_)
    df_list.append(df)
final_df = pd.concat(df_list)
value_counts = final_df['LOCATION'].value_counts()
print(value_counts)

final_df.to_pickle("df_sitl.pkl")
