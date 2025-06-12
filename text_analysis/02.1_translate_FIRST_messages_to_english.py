from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import pandas as pd
from tqdm import tqdm
import pickle
import os

# Set up Google Translate API
# Path to the service account key JSON file
# NOTE: include the path to the google cloud service account key
service_account_file = 'gpt-analyses-e74b015f86ac.json'

# Create a translation client using the service account key
credentials = service_account.Credentials.from_service_account_file(
    service_account_file)
client = translate.Client(credentials=credentials)

# Goal: Translate Turkish to English
# Step 1: Detect language
# Step 2: If language != en, translate to en

# Load data
user_messages = pd.read_csv('text_analysis/data/first_message_raw_s1_4_final.csv')

# Assume this is not the first run
# detect if the file exists
if os.path.exists('text_analysis/data/translated_prompts.pickle'):
    with open('text_analysis/data/translated_prompts.pickle', 'rb') as handle:
        reviewed_message = pickle.load(handle)
else:
    reviewed_message = {}

translation_results = []
for row_id in tqdm(range(user_messages.shape[0])):

    row = user_messages.iloc[row_id]
    message = row['message']

    # convert message to lower case + strip white space
    message_lc = message.strip().lower()

    # step 0: if message_lc has already been checked
    # use the previous results
    if reviewed_message.get(message_lc, None) != None:
        translated_message = reviewed_message[message_lc]['translated_message']
        translated = reviewed_message[message_lc]['translated']

        # Plug back
        translation_results.append({'translated_message': translated_message,
                                    'translated': translated})
        # print('This message has been translated')
        continue

    # step 1: check if the message is english
    language_check = client.detect_language(message_lc)

    # step 2:
    if language_check['language'] != 'en':
        # Translate text
        translated_language = client.translate(message_lc,
                                               target_language='en')

        translated_message = translated_language['translatedText']
        translated = True

    else:
        translated_message = message_lc
        translated = False

    # Plug back
    translation_results.append({'translated_message': translated_message,
                                'translated': translated})

    # Add to reviewed_text
    reviewed_message[message_lc] = {'translated_message': translated_message,
                                    'translated': translated}
    
    assert len(translation_results) == row_id + 1
# ============End of Loop ============

# Merge
translation_df = pd.DataFrame(translation_results)
assert translation_df.shape[0] == user_messages.shape[0]
final_result = pd.concat([user_messages, translation_df], axis=1)

# check if untranslated texts are the same
eng = final_result.query('translated == False')
assert all(eng['message'].map(lambda x: x.strip().lower())
           == eng['translated_message'])

# save
final_result.to_csv('text_analysis/data/translated_first_prompt_s1_4_final.csv')
with open('text_analysis/data/translated_prompts.pickle', 'wb') as handle:
    pickle.dump(reviewed_message, handle, protocol=pickle.HIGHEST_PROTOCOL)

