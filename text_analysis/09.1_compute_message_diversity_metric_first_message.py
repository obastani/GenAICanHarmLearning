import pickle
import pandas as pd
import numpy as np

# Save to Dict
with open('text_analysis/results/first_message_embeddings_final.pkl', 'rb') as file:
    data = pickle.load(file)

df = pd.DataFrame(data)

# Session-Treatment-grade mean
session_treatment_grade_mean = df.groupby(['session_id',
                                           'treatment',
                                           'grade',
                                           'problem_id'])['embedding'].mean().to_frame().reset_index()


# Calculate cosine similarity and MSE
matched_data = df.merge(session_treatment_grade_mean,
                        how='left',
                        on=['session_id',
                            'treatment',
                            'grade',
                            'problem_id'],
                        suffixes=[
                            '_problem', '_grand_mean']
                        )

assert matched_data.shape[0] == df.shape[0]


def cosine_similarity(row):
    vector_a = row['embedding_problem']
    vector_b = row['embedding_grand_mean']
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)

    similarity = dot_product / (norm_a * norm_b)
    return similarity


def mse(row):
    vector_a = row['embedding_problem']
    vector_b = row['embedding_grand_mean']

    return np.sqrt(np.sum(np.square(vector_a - vector_b)))


matched_data.loc[:, 'cosine_similarity'] = matched_data.apply(
    cosine_similarity, axis=1)
matched_data.loc[:, 'euclidean_distance'] = matched_data.apply(mse, axis=1)

# final data
final_data = matched_data[['username',
                           'session_id',
                           'treatment',
                           'problem_id',
                           'grade',
                           'cosine_similarity',
                           'euclidean_distance']].sort_values(['treatment',
                                                               'session_id',
                                                               'problem_id'
                                                               ])
                           
problem_id_col = ['username',
                'session_id',
                'treatment',
                'problem_id',
                'grade'
                ]
final_data['message_id'] = final_data.groupby(problem_id_col).cumcount() + 1
final_data.to_csv('text_analysis/results/diversity_metrics_first_messages_final.csv')

# ========================================
# Merge with diversity metrics for convenience
data_concat = pd.read_csv(
    'text_analysis/results/superficial_and_template_label_first_messages_final.csv')
diversity_metric = pd.read_csv(
    'text_analysis/results/diversity_metrics_first_messages_final.csv')

col_merge_on = ['username',
                'session_id',
                'treatment',
                'problem_id',
                'grade'
                ]
for colname in col_merge_on:
    assert all(data_concat[colname].isin(diversity_metric[colname]))


diversity_w_superficial = diversity_metric.merge(data_concat,
                                                 how='left',
                                                 on=['username',
                                                     'session_id',
                                                     'treatment',
                                                     'problem_id',
                                                     'grade',
                                                     'message_id'
                                                     ])


# Delete exact template column
merged_data = diversity_w_superficial.drop(['exact_template',
                                            'template',
                                            'meta_cluster',
                                            'Unnamed: 0_y'
                                            ], axis=1)


merged_data.to_csv('text_analysis/results/diversity_w_superficial_first_messages_final.csv')
