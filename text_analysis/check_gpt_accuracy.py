import openai
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os


# Gather all questions
question_list = pd.read_csv('text_analysis/data/raw/question_list.csv', encoding='latin1')

# Prepare OpenAI
# NOTE: Setup your API key in the .env file
load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

result_dict = {}
for row_id in range(question_list.shape[0]):
    
    row = question_list.iloc[row_id]
    
    question_id = row['session'] + '_' + str(row['grade']) + '_' + str(row['problem_id'])
    question = row['question']
    
    print(f"Question is {question}")
    counter = 0
    answers = []
    while counter <= 9:
        # Formulate the query
        gpt_query = [{'role': 'system', 
                    'content': f"You are ChatGPT, a large language model trained by OpenAI. \
                        Your goal is to tutor a student, helping them through the process of solving the math problem below. \
                            Please follow the student's instructions carefully. Write your answers in Github supported Markdown.\
                                Wrap inline math expressions with '$' and blcok math expressions with 'n$$n'.\
                                    When write numbered list, use 'First,' instead of use '1.'. Now you can help with this problem: \
                                        {question}."},
                    {'role': "user",
                    'content': "What is the answer"
                    }]
        
        # Send to GPT
        gpt_response = openai.ChatCompletion.create(stream=False, 
                                                    model='gpt-4',  
                                                    temperature=1,
                                                    max_tokens=1000,
                                                    messages = gpt_query)
        
        # GPT full answer
        gpt_answer = gpt_response['choices'][0]['message']['content']
        # gpt_answer
        answers.append(gpt_answer)
        
        # increase counter
        counter += 1
    
    # Plug back to the dict
    result_dict[question_id] = answers
    
    # Save every 5 steps
    if row_id % 5 == 0 and row_id != 0:
        pd.DataFrame.from_dict(result_dict, orient='index').to_csv('text_analysis/results/gpt_answers_checkpoint.csv')
        
# Save last time
pd.DataFrame.from_dict(result_dict, orient='index').to_csv('text_analysis/results/gpt_answers_full.csv')


