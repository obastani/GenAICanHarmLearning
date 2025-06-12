import pandas as pd
from plotnine import (ggplot, aes, geom_bar,
                      theme, element_text, theme_bw,
                      xlab, ylab)
from itertools import product

data = pd.read_csv('text_analysis/results/meta_cluster_first_messages_final.csv')


data['boring'] = (data['meta_rep_doc'] == 'what is the answer') | (
    data['meta_rep_doc'] == 'repeat the question')
data['template'] = (data['meta_rep_doc'] == 'can you help me figure out how to solve this problem?') | \
    (data['meta_rep_doc'] == 'can you help me better understand the question?')

# =============================================================================
# Find top messages per session-grade-treatment group
# =============================================================================
top_3_clusters_for_each_session = data.groupby(
    ['session_id', 'treatment', 'meta_rep_doc','meta_cluster']).agg({'count': 'sum'}).reset_index()
session_total = top_3_clusters_for_each_session. groupby(
    ['session_id', 'treatment'])['count'].transform('sum')
top_3_clusters_for_each_session['session_total'] = session_total
top_3_clusters_for_each_session.loc[:, 'prop'] = top_3_clusters_for_each_session['count'] / \
    top_3_clusters_for_each_session['session_total']
    
top_3_clusters_per_each_session_sorted = top_3_clusters_for_each_session.sort_values(
    ['session_id', 'treatment', 'count'], ascending=[True, True, False]).groupby(['session_id', 'treatment']).head(3)
 
all_unique_clusters = top_3_clusters_per_each_session_sorted['meta_rep_doc'].drop_duplicates().to_list()

top_3_clusters_for_each_session.query(f"treatment == 'aug'").sort_values(
    ['session_id', 'treatment', 'count'], ascending=[True, True, False])

# Generate all combinations of elements from A, B, and C
all_session_id = ['s1', 's2', 's3', 's4']
all_treatment = ['aug', 'vanilla']
all_clusters = all_unique_clusters
all_clusters_combinations = list(product(all_session_id, all_treatment, all_clusters))
all_clusters_df = pd.DataFrame(all_clusters_combinations, columns=['session_id', 'treatment', 'meta_rep_doc'])

all_clusters_w_prob = all_clusters_df.merge(top_3_clusters_for_each_session,
                      how = 'left',
                      on = ['session_id', 'treatment', 'meta_rep_doc'])

# convert NAN to 0
all_clusters_w_prob = all_clusters_w_prob.fillna(0)
all_clusters_w_prob['meta_rep_doc'].unique()

# relabel
# NOTE: the relabeling might change in different runs, due to randomness in the BERTopic model.
# If the cluster changes, the relabel_mapping needs to be updated for the script to run.
relabel_mapping = {
    'is the answer 4': "Attempted Answers",
    'repeat the question': "Repeat Question Text",
    'the answer is refik and sami': "Attempted Answers",
    'what is the answer': "Ask for Answers",
    'solve this question': "Ask for Help",
    'can you help me with the start of the question': 'Ask for Help',
    'can you help me figure out how to solve this problem?': "Ask for Help (template)"
}

def relabel(x):
    return relabel_mapping[x]

all_clusters_w_prob['meta_rep_doc'] = all_clusters_w_prob['meta_rep_doc'].apply(lambda x: relabel(x))

# Aggregate docs with the same label
all_clusters_w_prob = all_clusters_w_prob.groupby(['session_id',
                             'treatment',
                             'meta_rep_doc']).agg({'prop':'sum'}).reset_index()

all_clusters_w_prob = all_clusters_w_prob.sort_values(
    ['session_id', 'treatment', 'prop'], ascending=[True, True, False])


# Ready to visualize
aug_plot_data = all_clusters_w_prob.query('treatment == "aug"').reset_index(drop=True)
van_plot_data = all_clusters_w_prob.query('treatment == "vanilla"').reset_index(drop=True)


aug_plot_data.to_csv('text_analysis/results/augmented_top3_clusters_final.csv')
van_plot_data.to_csv('text_analysis/results/vanilla_top3_clusters_final.csv')
