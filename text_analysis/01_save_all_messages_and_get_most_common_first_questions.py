import pandas as pd

# Load data
conv_data = pd.read_csv('text_analysis/data/raw/valid_student_data.csv')
# =======================
# Save all conversation
# =======================
user_message = conv_data.query('role == "user"')
# All should be user messages
assert all(user_message['role'] == 'user')

# Save all message
user_message.to_csv('text_analysis/data/all_user_messages_raw_s1_4_final.csv')

# =====================================================================
# Save the message count by username, problem, session, grade, and treatment
# =====================================================================
num_messages = user_message.groupby(['username', 
                      'problem_id', 
                      'session_id',
                      'grade',
                      'treatment'
                      ])['message'].count().reset_index().rename(columns={'message':'num_messages'})
num_messages.to_csv('text_analysis/results/num_student_prompts.csv')

# =======================
# Save the first message
# =======================
# Drop all prompt rows
conv_data_without_prompts = conv_data.query('role != "system"')

# Group by username - session_id - problem_id, then take the first row
first_message_set = conv_data_without_prompts.groupby(
    ['username',
     'session_id',
     'grade',
     'problem_id']).head(1)

# All should be user messages
assert all(first_message_set['role'] == 'user')

# Check if unique at username conversation_id level
assert any(
    first_message_set[['username', 'conversation_id']].duplicated()) == False

# Save
first_message_set.to_csv('text_analysis/data/first_message_raw_s1_4_final.csv')

# ===============================
# Save a the time stamp version
# ===============================

# Load Data
conv_data = pd.read_csv('text_analysis/data/raw/valid_student_data_w_time_stamp.csv')

# Save all conversation
user_message = conv_data.query('role == "user"')
# All should be user messages
assert all(user_message['role'] == 'user')

# Save all message
user_message.to_csv('text_analysis/data/all_user_messages_raw_s1_4_final_w_time_stamp.csv')



