import numpy as np
import pandas as pd
import re


answers = pd.read_csv('posts_answers.csv')
questions = pd.read_csv('posts_questions.csv')
questions.drop(columns=["parent_id"], inplace=True)
questions.rename(columns={"id" : "parent_id", "body" : "questions"}, inplace=True)
answers.rename(columns={"body" : "answers"}, inplace=True)
qa = questions.merge(answers, on=['parent_id'])
col = qa.columns
for i in col:
  if i != "answers" and i != "questions":
    qa.drop(columns=i, inplace=True)
col = qa.columns
for j in col:
  for i in range(len(qa[j])):
    killmentions = re.compile('^@[A-Za-z]+|.+ @[A-Za-z]+')
    clear_text_1 = killmentions.sub('', qa[j][i])
    killtags = re.compile('<.*?>')  
    clear_text_2 = killtags.sub('', clear_text_1)
    killslashn = re.compile('\n')
    qa[j][i] = killslashn.sub('', clear_text_2)
qa.to_csv('dataset.csv')