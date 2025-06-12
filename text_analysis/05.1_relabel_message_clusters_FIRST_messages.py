import pandas as pd
import numpy as np

# load cluster
clusters = pd.read_csv('text_analysis/results/top_messages_by_arm_question_s1_4_first_messages_final.csv')
# the index is in the correct order
assert (all(clusters.index == range(clusters.shape[0])))

# Total number of unique clusters
len(set(clusters['repdoc']))

# load question list
question_list = pd.read_csv('text_analysis/data/raw/question_list.csv', encoding='latin1')


clusters['relabeled_topic'] = ""
for row_id in range(clusters.shape[0]):
    
    row = clusters.iloc[row_id]
    
    # Skip rows that are separators (i.e., all NAs)
    if isinstance(row['treatment'], str) is False:
        continue
    
    # Step 1: relabel cluster name to 'repeat the question' if they are similar enough
    grade = int(row['grade'][1:])
    session = row['session_id']
    question_id = int(row['question_id'][1:])
    
    chars = pd.Series(row['repdoc'].split(' '))
    question = question_list.query(f"grade == {grade} & session == '{session}' & problem_id == {question_id}")
    question_char = question['question'].iloc[0].split(' ')
    
    # Calculate overlap rate
    overlap_rate = np.mean(pd.Series(question_char).isin(chars))
    
    # If the overlap is above 50%, label the cluster as "repeat the question"
    if overlap_rate >= 0.5:
        clusters.loc[row_id, 'relabeled_topic'] = 'repeat the question'
    
    
# save the the results
clusters.to_csv('text_analysis/results/relabeled_cluster_first_messages_final.csv')

    
    