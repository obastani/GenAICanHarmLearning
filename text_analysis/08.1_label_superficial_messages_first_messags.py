import pandas as pd
from bertopic import BERTopic
from tqdm import tqdm

# load meta cluster results
meta_cluster_results = pd.read_csv(
    'text_analysis/results/meta_cluster_first_messages_final.csv')

# Label superficial
meta_cluster_results['superficial'] = (meta_cluster_results['meta_rep_doc'] == \
    'what is the answer') | (meta_cluster_results['meta_rep_doc'] == 'repeat the question')
# Label template
meta_cluster_results['template'] = meta_cluster_results['meta_rep_doc'] == \
    'can you help me figure out how to solve this problem?'

# Generate session_id - problem_id column
meta_cluster_results['treatment_session_problem'] = meta_cluster_results['treatment'] + '_' + \
    meta_cluster_results['session_id'] + '_' + \
    meta_cluster_results['grade'].map(lambda x: x.zfill(2)) + '_' + \
    meta_cluster_results['question_id']

# =========================================================================
# load message cluster results
raw_data = pd.read_csv('text_analysis/data/translated_first_prompt_s1_4_final.csv', dtype=str)


# Generate session_id - problem_id column
raw_data['treatment_session_problem'] = raw_data['treatment'] + '_' + \
    's' + raw_data['session_id'] + '_' + \
    'g' + raw_data['grade'].map(lambda x: x.zfill(2)) + '_' + \
    'q' + raw_data['problem_id']
group_id_list = raw_data['treatment_session_problem'].drop_duplicates()

# =========================================================================
all_users_data = []
for group in tqdm(group_id_list):

    loaded_model = BERTopic.load(
        f"text_analysis/model_checkpoints/s1_4/checkpoint_{group}_full")
    group_message = raw_data[raw_data['treatment_session_problem'] == group]
    assert all(group_message['treatment_session_problem'].drop_duplicates()
               == group)
    messages_total = group_message['translated_message']

    # Get the topic assignment of each topic
    doc_topic_info = loaded_model.get_document_info(messages_total)

    # Add topic by 1 to match meta_cluster results
    doc_topic_info['Topic'] = doc_topic_info['Topic'] + 1

    # Merge with meta cluster results
    relevant_meta_clusters = meta_cluster_results.query(
        f"treatment_session_problem == '{group}'")
    merged_doc = doc_topic_info.merge(relevant_meta_clusters,
                                      how='left',
                                      left_on='Topic',
                                      right_on='topic')

    # Prepare Final data
    assert group_message.shape[0] == merged_doc.shape[0]
    # Ignore index
    group_message['template'] = merged_doc['template'].to_list()
    group_message['superficial'] = merged_doc['superficial'].to_list()
    group_message['exact_template'] = (
        merged_doc['meta_rep_doc'] == 'can you help me figure out how to solve this problem?').to_list()
    group_message['meta_cluster'] = merged_doc['meta_cluster'].to_list()

    # Final data
    final_data = group_message[['username',
                                'grade',
                                'session_id',
                                'problem_id',
                                'meta_cluster',
                                'treatment',
                                'template',
                                'superficial',
                                'exact_template'
                                ]].reset_index(drop=True)
    # If NA, then labeled as false.
    # NA is caused by the message belong to outlier clusters
    final_data[['template', 'superficial']] = final_data[[
        'template', 'superficial']].fillna(False)
    assert all(final_data[['template', 'superficial']].isna().sum() == 0)

    # Append
    all_users_data.append(final_data)

# Concat Data
data_concat = pd.concat(all_users_data, axis=0).reset_index(drop=True)
sum(data_concat['exact_template'])

# Add a message_id column
problem_id_col = ['username',
                'session_id',
                'treatment',
                'problem_id',
                'grade']

data_concat['message_id'] = data_concat.groupby(problem_id_col).cumcount() + 1
assert any(data_concat.duplicated()) == False

# save
data_concat.to_csv(
    'text_analysis/results/superficial_and_template_label_first_messages_final.csv')
