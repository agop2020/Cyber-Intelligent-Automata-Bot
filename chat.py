import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
print("test2") #disregard this, was printing to test something
import numpy
import tflearn
import tensorflow
import random
import json
import pickle

#if changing index.JSON, model needs to be retrained - put an x after the try line(line 17)

with open("index.JSON") as file:
    data = json.load(file)
try:
    #opens up a pickle file with these 4 variables
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = [] #each stripped down word in patterns
    labels = [] #tags(goodbye, greetings)
    docs_x = [] #questions/statements to respond to(patterns) - not stripped down
    docs_y = [] #what tag/intent each docs_x element is a part of
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern) #gets all words in a pattern to ultimately strip
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])

    #strips word down (what's -> what), removes duplicate words(makes all lowercase first), sorts alphabetically
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    #bag of words(0s and 1s if a word exists or doesn't exist in a sentence)

    training = []
    output = []

    #0s, representing all tags
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        #wrds is stripped down words in patterns(doc_x)
        wrds = [stemmer.stem(w.lower()) for w in doc]

        #words is main wordlist of patterns - sorted and stripped, no duplicates
        #wrds is only stripped patterns
        #ensures there isn't more than one 0 or 1 for the same word
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]

        #looks through labels, find where tag is of that particular pattern word, sets that value to 1 in output row
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag) #actual words in patterns represented by 0s and 1s
        output.append(output_row) #tags represented by 0s and 1s

    training = numpy.array(training)
    output = numpy.array(output)

    #saves those variables in a pickle file
    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)


#model
tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])]) #input layer - one neuron is one word in patterns
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax") #softmax allows for probabilities of each output, has six neurons(6 possible classes of tags)
net = tflearn.regression(net)

model = tflearn.DNN(net)
try:
    model.load("model.tflearn")
except:
    #epoch is num of times the model will see the same data
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

#bag of words from user input
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    #same logic as earlier bag of words, ensures there aren't multiple 1s or 0s for one word
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)

def chat(inp):
    # if inp.lower() == "quit":
    #     return None

    #gives probabilities for each tag/class
    results = model.predict([bag_of_words(inp, words)])
    #gets the most likely class
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']

    return random.choice(responses)

