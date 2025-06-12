import pandas as pd
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired


# ================
# Preparedata
# ================
raw_data = pd.read_csv('text_analysis/data/translated_first_prompt_s1_4_final.csv', dtype=str)

# Generate session_id - problem_id column
raw_data['treatment_session_problem'] = raw_data['treatment'] + '_' + \
    's' + raw_data['session_id'] + '_' + \
    'g' + raw_data['grade'].map(lambda x: x.zfill(2)) + '_' + \
    'q' + raw_data['problem_id']

# Clean the text
# NOTE: ORDER MATTERS!
unreadable_patterns_list = ['nuffdn',
                            'uffdn',
                            'nufffdn',
                            'ufffdn',
                            'ufffd'
                            '&quot;',
                            'u2005',
                            'u200a',
                            'u200b',
                            'nn',
                            "\\’,"]
substitution_list = [{'pattern': 'u0131', 'replacement': 'i'},
                     {'pattern': 'u2227', 'replacement': '∧'},
                     {'pattern': 'u2032', 'replacement': "'"},
                     {'pattern': 'u22bb', 'replacement': "⊻"},
                     {'pattern': 'u2212', 'replacement': "-"},
                     {'pattern': 'u2228', 'replacement': "∨"},
                     {'pattern': 'u27f9n', 'replacement': "=>"},
                     {'pattern': 'u21d2n', 'replacement': "=>"},
                     {'pattern': r'n(\d+)n\d+', 'replacement': r'\1'},
                     {'pattern': 'u2229', 'replacement': '∩'},
                     {'pattern': 'u00e7', 'replacement': 'c'},
                     {'pattern': 'u00f6', 'replacement': 'o'},
                     {'pattern': 'u011f', 'replacement': 'g'},
                     {'pattern': r'n\([^)]*\)n', 'replacement': ''},
                     {'pattern': r"n'n", 'replacement': "'"},
                     {'pattern': 'u27f9', 'replacement': "=>"},
                     {'pattern': 'u21d2', 'replacement': "=>"},
                     {'pattern': r'=n\{[^)]*\}n', 'replacement': ''},
                     {'pattern': r'n\{[^)]*\}n', 'replacement': ''},
                     {'pattern': 'u00fc', 'replacement': 'u'},
                     {'pattern': 'u2019', 'replacement': "'"}
                     ]


def clean_unreadable_patterns(input_string_series,
                              unreadable_pattern_list,
                              substitution_list
                              ):

    if not isinstance(input_string_series, pd.Series):
        raise TypeError('input_string_series needs to be pd.Series')

    for pattern in unreadable_pattern_list:
        input_string_series = input_string_series.str.replace(
            pattern, '', regex=False)

    for substitution_pattern in substitution_list:
        pattern = substitution_pattern['pattern']
        replacement = substitution_pattern['replacement']
        input_string_series = input_string_series.str.replace(
            pattern, replacement, regex=True)

    return input_string_series


# Clean
raw_data['translated_message'] = clean_unreadable_patterns(
    input_string_series=raw_data['translated_message'],
    unreadable_pattern_list=unreadable_patterns_list,
    substitution_list=substitution_list)

# =========================
# BERTtopic Model
# =========================
# Initialize BERT topic models
representation_model = KeyBERTInspired()

# Run one topic model for each treatment-session-problem
group_id_list = raw_data['treatment_session_problem'].drop_duplicates()

# Loop through group
translation_failure = 0
for group in group_id_list:

    # Extract messages
    group_message = raw_data[raw_data['treatment_session_problem'] == group]
    assert all(group_message['treatment_session_problem'].drop_duplicates()
               == group)
    messages_total = group_message['translated_message']

    # Some message is NA due to translation failure, use the original messages
    if any(messages_total.isna()):
        messages_total[messages_total.isna(
        )] = group_message['message'][messages_total.isna()]

        translation_failure += 1

    messages = messages_total.reset_index(drop=True)

    # Run model
    topic_model = BERTopic(representation_model=representation_model,
                           min_topic_size=2)
    topics, probs = topic_model.fit_transform(messages)

    if any([x == -1 for x in topics]) == True:
        # Eliminate -1
        topic_outlier_reduced = topic_model.reduce_outliers(
            messages,
            topics,
            strategy="c-TF-IDF")
    else:
        topic_outlier_reduced = topics

    # Get results
    results = topic_model.get_document_info(messages)
    results['Topic_mod'] = topic_outlier_reduced

    # Match the -1 topic with the correct representative docs
    # Replace representative doc
    topic_repdoc = results[~results['Topic'].duplicated()][[
        'Topic', 'Representative_Docs']]
    topic_repdoc.columns = ['Topic', 'repdoc']

    # Merge
    results_corrected = results.merge(topic_repdoc, how='left', on='Topic')

    # Get the first representative doc
    results_corrected['most_rep_doc'] = results_corrected['repdoc'].map(
        lambda x: x[0])

    # Save model and results
    topic_model.save(f"text_analysis/model_checkpoints/s1_4/checkpoint_{group}_full",
                     serialization="pickle")
    topic_model.save(f"text_analysis/model_checkpoints/s1_4/checkpoint_{group}_light",
                     serialization="safetensors")
    results_corrected.to_csv(
        f'text_analysis/data/first_message_cluster_by_arm_grade/first_prompt_cluster_result_{group}_s1_4_final.csv')

