# Descriptions

This directory contains the full pipeline of scripts used in our analysis of student messages and GPT accuracy.

## Folders
- `data/` — Includes datasets for the analyses.
- `model_checkpoints/` - Includes saved BERTtopic models.
- `results/` - Includes intermediate and final results.

## Note
- Users need to provide a Google translation service account to run `02.1_translate_FIRST_messages_to_english.py` and `02.2_translate_ALL_messages_to_english.py`.
- Users need to provide a OpenAI API key to run `check_gpt_accuracy.py`.

## Scripts

All scripts are numerically ordered and should be run sequentially:

| Script Name | Description |
|-------------|-------------|
| `01_save_all_messages_and_get_most_common_first_questions.py` | Saves all messages and identifies the first message in each conversation. |
| `02.1_translate_FIRST_messages_to_english.py` | Translates first messages that are in Turkish to English. |
| `02.2_translate_ALL_messages_to_english.py` | Translates all Turkish messages to English. |
| `03.1_cluster_first_message_by_arm_grade_question.py` | Clusters first messages by treatment arm, grade, and question. |
| `03.2_cluster_all_message_by_arm_grade_question.py` | Clusters all messages by treatment arm, grade, and question. |
| `04.1_concatenate_FIRST_message_clusters.r` | Concatenates clusters of first messages. |
| `04.2_concatenate_ALL_message_clusters.R` | Concatenates clusters of all messages. |
| `05.1_relabel_message_clusters_FIRST_messages.py` | Manually relabels first-message clusters. |
| `05.2_relabel_message_clusters_ALL_messages.py` | Manually relabels all-message clusters. |
| `06.1_meta_cluster_first_messages.py` | Performs meta-clustering on relabeled first-message clusters. |
| `06.2_meta_cluster_all_messages.py` | Performs meta-clustering on relabeled all-message clusters. |
| `07.1_use_embeddings_to_measure_message_diversity_first_messages.py` | Converts first messages to embeddings and measures diversity. |
| `07.2_use_embeddings_to_measure_message_diversity_all_messages.py` | Converts all messages to embeddings and measures diversity. |
| `08.1_label_superficial_messages_first_messags.py` | Labels superficial content in first messages. |
| `08.2_label_superficial_messages_all_messags.py` | Labels superficial content in all messages. |
| `09.1_compute_message_diversity_metric_first_message.py` | Computes diversity metrics for first messages, merging with superficiality labels. |
| `09.2_compute_message_diversity_metric_all_messages.py` | Computes diversity metrics for all messages, merging with superficiality labels. |
| `10.1_create_visualization_data_first_message.py` | Generates visualization data for first-message meta-clusters. |
| `10.2_create_visualization_data_all_message.py` | Generates visualization data for all-message meta-clusters. |
| `11_calculate_time.py` | Calculates the time elapsed per student and class. |
| `check_gpt_accuracy.py` | Evaluates GPT-generated answers for correctness. |

