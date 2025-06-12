import pandas as pd
from tqdm import tqdm
import numpy as np
import torch
from transformers import BertTokenizer, BertModel
import pickle


df = pd.read_csv('text_analysis/data/translated_all_messages_s1_4_final.csv')

assert all(df[['username',
                        'grade',
                        'session_id',
                        'problem_id',
                        'treatment']].duplicated()) == False

# convert messages to BERT embeddings
# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
model = BertModel.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

# Set device (use GPU if available, otherwise use CPU)
device = torch.device("mps" if torch.cuda.is_available() else "cpu")
model.to(device)

user_df = df.query('role == "user"').reset_index()
batch_size = 150

# Label Template Messages
template_message = (user_df['translated_message'] == 'can you help me figure out how to solve this problem?') | \
    (user_df['translated_message'] == 'can you help me better understand the question?')


results = {
    'session_id': [],
    'grade': [],
    'username': [],
    'treatment': [],
    'problem_id': [],
    'embedding': [],
    'template': template_message
}

for idx in tqdm(range(0, user_df.shape[0], batch_size)):
    #print(range(idx,(idx + batch_size - 1)))
    batch_texts = user_df.loc[idx:(idx + batch_size - 1), 'message'].to_list()
    batch_session = user_df.loc[idx:(idx + batch_size - 1), 'session_id']
    batch_grade = user_df.loc[idx:(idx + batch_size - 1), 'grade']
    batch_username = user_df.loc[idx:(idx + batch_size - 1), 'username']
    batch_treatment = user_df.loc[idx:(idx + batch_size - 1), 'treatment']
    batch_problem_id = user_df.loc[idx:(idx + batch_size - 1), 'problem_id']
    
    results['session_id'].extend(batch_session)
    results['grade'].extend(batch_grade)
    results['username'].extend(batch_username)
    results['treatment'].extend(batch_treatment)
    results['problem_id'].extend(batch_problem_id)
    
    # Tokenize input text and convert to tensor
    input_ids = tokenizer(batch_texts, 
                          padding=True,
                          truncation=True,
                          return_tensors='pt')
    input_ids = input_ids.to(device)

    # Perform inference
    with torch.no_grad():
        outputs = model(**input_ids)
    
    # pooler embeddings
    cls_embeddings = outputs.pooler_output.numpy()
    
    cls_embedding_list = [cls_embeddings[i] for i in range(cls_embeddings.shape[0])]
    
    results['embedding'].extend(cls_embedding_list)
    
    assert len(results['session_id']) == len(results['embedding'])
    

    
with open('text_analysis/results/all_message_embeddings_final.pkl', 'wb') as file:
    pickle.dump(results, file)
