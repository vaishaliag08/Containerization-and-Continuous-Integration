import string
import re
from typing import Tuple
import numpy as np
import nltk
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = pickle.load(open("tfidfvectorizer.pkl", "rb"))

def score(text:str,
          model,
          threshold:float) -> Tuple[bool, float]:
    
    ## preprocess raw input text
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = text.replace("subject ", "")
    text = text.replace("re ", "")
    text = re.sub(r"\d+", "", text)
    stopwords = nltk.corpus.stopwords.words("english")
    tokenizer = WhitespaceTokenizer()
    text = tokenizer.tokenize(text)
    text = [word for word in text if word not in stopwords]
    lemmatizer = WordNetLemmatizer()
    text = [lemmatizer.lemmatize(word) for word in text]
    text = [word for word in text if len(word) > 1]
    text = [" ".join(text)]
    text = np.array(text)

    ## vectorize the text
    text_vect = vectorizer.transform(text)

    propensity = model.predict_proba(text_vect)
    if propensity[0][1] >= threshold: 
        prediction = 1
        propen = propensity[0][1]
    else: 
        prediction = 0
        propen = propensity[0][0]
    return prediction, propen

# text = "Subject: make big money with foreclosed real estate in your area  trinity consulting 1730 redhill ave . , ste . 135 irvine , ca 92606 this e - mail message is an advertisement and / or solicitation . "
# text = "Subject: re : rotational opportunities within your group  kate ,  my assistant , shirley crenshaw , will schedule a meeting .  vince  kate lucas  10 / 17 / 2000 11 : 57 am  to : vince j kaminski / hou / ect @ ect  cc :  subject : rotational opportunities within your group  dear vince ,  i am a rotating associate and would like to learn more about opportunities  within your group . i have worked in rac and am currently in financial  trading . i believe the associate / analyst program may forward you my cv , but i  thought it good to get in touch personally .  please let me know if there is someone with whom i could speak about the  group and its needs for associates .  with best regards ,  kate"
# svc_model = pickle.load(open("support_vector.pkl", "rb"))
# threshold = 1
# print(score(text, svc_model, threshold))