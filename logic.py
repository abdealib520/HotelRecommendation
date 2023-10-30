import numpy as np
import pandas as pd
import ast
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('omw-1.4.1')
stop_words = set(stopwords.words('english'))
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

def preprocessing(data):    
    data['Special'] = data['Special'].apply(ast.literal_eval).apply(lambda x: ' '.join(x))
    data['Price'] = data['Price'].str.replace('₹','').str.replace(',','').astype('int32')
    data['Discount'] = data['Discount'].str.replace('%','').astype('float32').div(100)
    data = data.dropna(subset=['Location','Price','Title','City'])
    data = data.drop(['Review','From_Date','To_Date'],axis=1)
    return data


def text_preprocess(text):
    tokens = word_tokenize(text)
    tokens_lemmatized = [wordnet_lemmatizer.lemmatize(w) for w in tokens if not w.lower() in stop_words]
    return set(tokens_lemmatized)

def intersection_length(text,se):
    text_tokens = text_preprocess(text)
    length = len(text_tokens.intersection(se))
    return length

def offer_convert(value):
    if value == 'Yes':
        return True
    else:
        return False

def hotel_recommender(city,location,requirements,min_no_of_ratings=10, \
                                       min_price=0,max_price=99999,offer=False):
    data = pd.read_csv('Hotel_data.csv')
    data = preprocessing(data)
    city = city.lower()
    data['City'] = data['City'].str.lower()
    if offer:
        data = data.dropna(subset='Offer')
        data['Discounted_Price'] = np.round(data['Price'] - data['Price']*data['Discount'],0)
    data = data.loc[(data['City'] == city) & (data['No_of_ratings'] >= min_no_of_ratings)\
                    & (data['Price'] >= min_price) & (data['Price'] <= max_price)]
    location_tokens = text_preprocess(location)
    data['Recommendation_Location'] = data['Location'].apply(intersection_length,args=(location_tokens,))
    requirements_tokens = text_preprocess(requirements)
    
    data['Recommendation_Requirements'] = data['Special'].apply(intersection_length,args=(requirements_tokens,))
    return data.sort_values(by=['Recommendation_Location', 'Recommendation_Requirements'],ascending=False).head().\
            drop(['Recommendation_Location','Recommendation_Requirements','City'],axis=1)
