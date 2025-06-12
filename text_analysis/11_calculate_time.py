import pandas as pd
from datetime import datetime

data = pd.read_csv('text_analysis/data/all_user_messages_raw_s1_4_final_w_time_stamp.csv')

# Convert to dt object
time_stamp = pd.to_datetime(data['time_stamp'], format="mixed")
data['time_stamp'] = time_stamp

# For each username-grade-session_id-treatment, 
# get the first time stamp and the last time stamp
def calculate_time_info(group):
    min_time = min(group['time_stamp'])
    max_time = max(group['time_stamp'])
    diff = (max_time - min_time).total_seconds() / 60
    return pd.DataFrame({'first_msg_time': min_time, 
                         'last_msg_time': max_time, 
                         'total_time_in_minutes': diff}, index=[0])
group_time = data.groupby(['username', 'grade', 'session_id', 'treatment']).apply(calculate_time_info)
group_data_reformat = group_time.reset_index()

# Drop unused columns
time_stamp_data_reformat = group_data_reformat.drop(['level_4'],axis=1)

# save
time_stamp_data_reformat.to_csv('text_analysis/data/student_time_stamp_info.csv')