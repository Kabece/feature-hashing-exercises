import json
import time
from pprint import pprint

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer

earnOrNot = []
justBodies = []
np.random.seed(0)

def removeArticlesWithoutTopic():
    global earnOrNot, justBodies
    for obj in json.load(open('D:/FeatureHashing/merged.json')):
        if "topics" in obj and "body" in obj:
            justBodies.append(obj["body"])
            if "earn" in obj["topics"]:
                earnOrNot.append(1)
            else:
                earnOrNot.append(0)

def bagTheWords():
    global justBodies
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(justBodies)
    return X, vectorizer.get_feature_names()

def hashTheWords():
    global justBodies
    numberOfBuckets = 1000
    X = []
    feature_names = set()
    for body in justBodies:
        words = body.split()
        hashes = [0] * numberOfBuckets
        for word in words:
            hashedValue = hash(word) % numberOfBuckets
            hashes[hashedValue] += 1
            feature_names.add(hashedValue)
        X.append(hashes)
    return X, list(feature_names)


def prepareSets(X, feature_names, isBagOfWords):
    global justBodies, earnOrNot
    if isBagOfWords:
        df = pd.DataFrame(X.toarray(), columns=feature_names)
    else:
        df = pd.DataFrame(X, columns=feature_names)
    df['ztopic'] = earnOrNot
    df['zis_train'] = np.random.uniform(0, 1, len(df)) <= .8
    train, test = df[df['zis_train']==True], df[df['zis_train']==False]
    trainSetEarnOrNot = train['ztopic']
    return train, test, trainSetEarnOrNot

def classify(train, test, trainSetEarnOrNot, feature_names):
    global justBodies
    clf = RandomForestClassifier(n_jobs=-1, n_estimators=50)
    clf = clf.fit(train[feature_names], trainSetEarnOrNot)
    predicted = clf.predict(test[feature_names])
    pprint(pd.crosstab(test['ztopic'], predicted, rownames=['Actual'], colnames=['Predicted']))

if __name__ == '__main__':
    start_time = time.time()
    removeArticlesWithoutTopic()
    initial_preparing_time = time.time() - start_time
    print("Bag of Words method: ")
    X, feature_names = bagTheWords()
    train, test, trainSetEarnOrNot = prepareSets(X, feature_names, True)
    classify(train, test, trainSetEarnOrNot, feature_names)
    bag_of_words_method_time = time.time() - initial_preparing_time
    print()
    print("Feature Hashing method: ")
    X2, feature_names2 = hashTheWords()
    train2, test2, trainSetEarnOrNot2 = prepareSets(X2, feature_names2, False)
    classify(train2, test2, trainSetEarnOrNot2, feature_names2)
    feature_hashing_method_time = time.time() - bag_of_words_method_time
    print("Execution time: %s seconds." % (time.time() - start_time))
    print("Bag of words method execution time: %s seconds." % (bag_of_words_method_time))
    print("Feature hashing method execution time: %s seconds." % (feature_hashing_method_time))


