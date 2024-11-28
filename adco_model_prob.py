from time import time
import numpy as np

def sigmoid(x):
    return 1 / ( 1 + np.exp(-x))

def prob_model(senti : float, subj : float, sim : float) -> float:
    """
    Parameter : senti -> 본문의 전체적인 감정, subj -> 본문의 전체적인 주관성, sim -> 본문과 기준 단어와의 유사성
    Return : prob -> 본문이 광고일 확률, 범위: (0, 1)
    """
    with open('datas\\prob_model_wb.txt','r') as file:
        content = file.read()
    w1, w2, w3, b = map(float, content.split(','))
    prob = sigmoid(w1 * senti + w2 * subj + w3 * sim + b)
    prob = float(prob)
    return prob


def train():
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense
    from tensorflow.keras import optimizers

    param_list = []
    result_list = []

    with open('datas\\adco_data_ad.csv', 'r') as file:
        contents = file.read().split('\n')[1:7]
    for content in contents:
        temp = content.split(',',maxsplit= 1)
        result_list.append(1 if temp[0] == 'y' else 0)
        row = []
        for f in temp[1].split(','):
            row.append(float(f))
        param_list.append(row)

    params = np.array(param_list)
    results = np.array(result_list)

    print(params)
    print(results)

    model = Sequential()
    model.add(Dense(1, input_dim=3, activation='sigmoid'))

    sgd = optimizers.SGD(learning_rate=0.01)
    model.compile(optimizer=sgd, loss='binary_crossentropy', metrics=['binary_accuracy'])

    model.fit(params, results, epochs=200)

    w1 = float(model.layers[0].get_weights()[0][0])
    w2 = float(model.layers[0].get_weights()[0][1])
    w3 = float(model.layers[0].get_weights()[0][2])
    b = float(model.layers[0].get_weights()[1][0])

    with open('datas\\prob_model_wb.txt', 'w') as file:
        file.write(f"{w1},{w2},{w3},{b}")

if (__name__ == "__main__"):
    # train()
    print(prob_model(0.356597866419295,0.7702251914751915,0.0378642936596218))