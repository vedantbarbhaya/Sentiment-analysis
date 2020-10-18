#NATURAL LANGUAGE PROCESSING

#IMPORTING LIBRARIES
import numpy as np
import matplotlib as plt
import pandas as pd

#IMPORTING THE DATASET
data = pd.read_csv("/Users/vishalkundar/review.csv")


data.columns = ['starPart','CommentsPart']
# renaming rows

''' The format of stars in the review file is for example 3.0 stars of 5.0 . We need to extract
 3.0 from this. The below method does that. We divide by 5 to apply scaling so that the values
 are always between 0 and 1 '''
 
'''Now if it below 0.5 we assign it 0 as negative and above 0.5 as 1 positive 0.5 is neutral '''
for index, row in data.iterrows():
    value = row['starPart'].rsplit(" ")
    if value[0] != "stars":
        scaledValue = float(value[0]) / 5.0
        if scaledValue < 0.5 :
            scaledValue = 0
        else:
            scaledValue = 1
        row['starPart'] = scaledValue
    else:
        # This is where the star part was not extracted properly for some reason so we put it 0
        # As it is pretty rare occurence
        row['starPart'] = "0"
        
# CLEANING THE TEXT
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer # For stemming

''' NLTK - The Natural Language ToolKit is one of the best-known and most-used 
NLP libraries in the Python ecosystem, useful for all sorts of tasks from tokenization, 
to stemming, to part of speech tagging, and beyond '''

reviewsList = []# Holds all reviews that will be preprocessed

# Looping for all reviews
for index, row in data.iterrows():
    review = re.sub('[^a-zA-Z]',' ',row['CommentsPart']) # Used to remove special characters associated with
    #it for example         
    review = review.lower()
    review = review.split() # Converts it to a list 

    '''The below line is commented because it is modified further in stemming
    and so there is no use of it now except for understanding its purpose ''' 
    # review = [word for word in review if not word in set(stopwords.words('english'))]
    # Here set is used because the algorithms are faster for a set when we have huge dataset

    #Stemming - keeps the root word i.e loved,loves,loving = love
    # To reduce sparsity in sparse matrix

    ps = PorterStemmer()# PorterStemmer class object
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]

    # Converting list of words back to string
    review = ' '.join(review)
    reviewsList.append(review)
    
# CREATING SPARSE MATRIX 
''' Taking all the unique words from reviews list and creating a column for
 each of them basically to make a sparse matrix '''
 
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(max_features = 2350) # Check Documentation - it is used to create the matrix
X = cv.fit_transform(reviewsList).toarray() # Here X is matrix of features and to convert it to matrix
# we do .toarray
# max features paramter uses only the words with a good frequency for sparse matrix 
# 2350 of most frequent words will be used
# This improves quality of sparse matrix 

y = data.iloc[:, 0].values # Creating dependant variable vector which is the scalled stars part
y = y.astype('int') # because it was taking it as an nd object array
# CREATING THE MODEL - NAIVE BAYES


# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
''' Tells us how many correct predictions we got
00 - correct predictions for negative reviews
10 - incorrect predictions for negative review
01 - incorrect predictions for positive reviews
11 - correct predictions for positive reviews '''
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
# Accuracy = 172/203 = 84%
print(cm)

# Visualaizations
import seaborn as sn
from matplotlib.figure import Figure
df_cm = pd.DataFrame(cm, index = [0,1],columns = [0,1])
f = Figure(figsize = (10,7))
sn.heatmap(df_cm, annot=True)
