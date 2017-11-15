import json
import time
from pprint import pprint

initialData = json.load(open('D:/FeatureHashing/merged.json'))
cleanData = []

def removeArticlesWithoutTopic():
    global initialData, cleanData
    i = 0
    for obj in initialData:
        if "topics" in obj:
            cleanData.append(obj)


if __name__ == '__main__':
    start_time = time.time()
    removeArticlesWithoutTopic()
    pprint(cleanData[1])
    print("Execution time: %s seconds." % (time.time() - start_time))

