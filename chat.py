#Used in Tensorflow Model
import numpy
import tensorflow
import tflearn
import random
import json
import pickle


#Usde to for Contextualisation and Other NLP Tasks.
import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()



with open('intents.json') as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:

    words = []
    labels = []
    docs_x = []
    docs_y = []

    #tokenize words
    #tokenize means chopping off the words into different chunks
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)

    #its just going to append all the patterns we have
            docs_x.append(wrds)
            docs_y.append(intent["tag"])


    #taking all the tags in a list  
        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    #we are going to to covert every word and turn them into lower case
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]

    #sorted them by creating a list, set remove duplicate
    words = sorted(list(set(words)))

    labels = sorted(labels)


    # up until now we created a string but we need to convert into numbers to work on DNN
        
    #bagging onehotencoder
    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    #training
    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)


#chat method to take input and show output 
def chat(inp):
        print(inp)
        print(words)
        results = model.predict([bag_of_words(inp, words)])[0]
        results_index = numpy.argmax(results)
        tag = labels[results_index]


        if results[results_index] > 0.75:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
                    return (random.choice(responses))
       
        return 'Sorry, I didnt get that. what is your question again?'




if __name__ == "__main__":
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        resp = chat(inp)
        print(resp)
