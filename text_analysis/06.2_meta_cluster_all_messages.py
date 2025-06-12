import pandas as pd
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
import numpy as np

# Load the data
relabeled_cluster = pd.read_csv('text_analysis/results/relabeled_cluster_all_messages_final.csv')

relabeled_cluster_naomit = relabeled_cluster[~relabeled_cluster['repdoc'].isna()].reset_index(drop=True)
# use the relabled_topic
relabeled_cluster_naomit['relabeled_topic'][relabeled_cluster_naomit['relabeled_topic'].isna()] = \
    relabeled_cluster_naomit['repdoc'][relabeled_cluster_naomit['relabeled_topic'].isna()] 

# Some light cleaning: delete leading " or '
for m_id, m in enumerate(relabeled_cluster_naomit['relabeled_topic']):
    if m[0] == '"' or m[0] == "'":
        m = m[1:]
    if m[-1] == '"' or m[-1] == "'":
        m = m[:-1]
    relabeled_cluster_naomit['relabeled_topic'].iloc[m_id] = m

representation_model = KeyBERTInspired()

# Run model
topic_model = BERTopic(representation_model=representation_model,
                        min_topic_size=5,
                        nr_topics='auto'
                        )

topics, probs = topic_model.fit_transform(relabeled_cluster_naomit['relabeled_topic'])


# Get results
results = topic_model.get_document_info(relabeled_cluster_naomit['relabeled_topic'])

# # Get the first representative doc
results['most_rep_doc'] = results['Representative_Docs'].map(
     lambda x: x[0])



# Save model and results
topic_model.save("text_analysis/model_checkpoints/meta_cluster/full_model_all_messages", serialization="pickle")
topic_model.save("text_analysis/model_checkpoints/meta_cluster/light_model_all_messages", serialization="safetensors")


# Manually merge topics if their representative docs are the same
unique_rep_doc = set(results['most_rep_doc'])
results['manual_cluster'] = np.nan
results['manual_rep_doc'] = np.nan
for doc_id, unique_doc in enumerate(unique_rep_doc):
    
    doc_in_this_cluster = results['most_rep_doc'] == unique_doc
    results['manual_cluster'][doc_in_this_cluster] = doc_id
    results['manual_rep_doc'][doc_in_this_cluster] = unique_doc


# Plug back to original
assert relabeled_cluster_naomit.shape[0] == results.shape[0]

relabeled_cluster_naomit['meta_cluster'] = results['manual_cluster']
relabeled_cluster_naomit['meta_rep_doc'] = results['manual_rep_doc']

# Relabel pre-defined prompt in the vanilla arm to 'ask for help'
# this is due to classification error
for row_id in range(relabeled_cluster_naomit.shape[0]):
    if relabeled_cluster_naomit.loc[row_id, 'treatment'] == 'vanilla':
        if (relabeled_cluster_naomit.loc[row_id, 'meta_rep_doc'] == 'can you help me figure out how to solve this problem?') | \
            (relabeled_cluster_naomit.loc[row_id, 'meta_rep_doc'] == 'can you better help me understand the question'):
            relabeled_cluster_naomit.loc[row_id, 'meta_rep_doc'] = 'ask for help'
            
# meta cluster
relabeled_cluster_naomit = relabeled_cluster_naomit.sort_values('meta_cluster')
relabeled_cluster_naomit.to_csv('text_analysis/results/meta_cluster_all_messages_final.csv')


# ==============================
# Find most common questions
# ==============================
relabeled_cluster_naomit = pd.read_csv('text_analysis/results/meta_cluster_all_messages_final.csv')
print(relabeled_cluster_naomit.query('treatment == "vanilla"').groupby('meta_rep_doc')['count'].sum(
) / sum(relabeled_cluster_naomit.query('treatment == "vanilla"').groupby('meta_rep_doc')['count'].sum()))
# total meta clusters
len(relabeled_cluster_naomit['meta_rep_doc'].unique())

# most popular clusters
(relabeled_cluster_naomit.query('treatment == "vanilla"').groupby('meta_rep_doc')['count'].sum(
) / sum(relabeled_cluster_naomit.query('treatment == "vanilla"').groupby('meta_rep_doc')['count'].sum())).sort_values(ascending=False)