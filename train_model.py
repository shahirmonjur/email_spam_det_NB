import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

df = pd.read_csv("emails.csv")
df.drop_duplicates(inplace=True)

X = df['text']
y = df['spam']

cv = CountVectorizer()
X_vec = cv.fit_transform(X)

model = MultinomialNB()
model.fit(X_vec, y)

joblib.dump(model, 'model.pkl')
joblib.dump(cv, 'vectorizer.pkl')
