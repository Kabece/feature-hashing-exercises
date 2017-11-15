import json
import time
from pprint import pprint

initialData = json.load(open('D:/FeatureHashing/merged.json'))
cleanData = []

def removeArticlesWithoutTopic():
    global initialData, cleanData
    i = 0
    for obj in initialData:
        if "topics" in obj and "body" in obj:
            cleanData.append(lowercaseBody(obj))

def lowercaseBody(object):
    object["body"] = object["body"].lower()
    return object

if __name__ == '__main__':
    start_time = time.time()
    removeArticlesWithoutTopic()
    pprint(len(cleanData))
    pprint(cleanData[0])
    print("Execution time: %s seconds." % (time.time() - start_time))

