import nltk
import pandas as pd
import re
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
porter = PorterStemmer()


def preprocess_text(text):
    
    if isinstance(text, str):
        tokens = word_tokenize(text.lower())

        tokens = [token + ' ' for token in tokens if token.isalnum() ]

    # Stemming
        ##stokens = [porter.stem(token) for token in tokens]

        return tokens


csvfile=csv.writer(open('ipc_dataset_nlp.csv','w'),lineterminator='\n')
csvfields=['Section','Description','Punishment','Bailable/Non-Bailable']
csvfile.writerow(csvfields)

data= pd.read_csv("ipc_dataset.csv")
rows=[]

for i in range(len(data)):
    each_row_tuple= data.loc[i,"Section"], data.loc[i,"Description"], data.loc[i,"Punishment"], data.loc[i,"Bailable/Non-Bailable"]
    each_row = list(each_row_tuple)
    ##processed_section = preprocess_text(each_row[0])
    processed_description = preprocess_text(each_row[1])
    processed_punishment = preprocess_text(each_row[2])
    ##processed_bailable = preprocess_text(each_row[3])
    rows.append((each_row[0],''.join(processed_description),''.join(processed_punishment), each_row[3]))

csvfile.writerows(rows)





