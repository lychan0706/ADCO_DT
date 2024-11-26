def model(text : str) -> tuple[float]:
    # 작성자: 정윤수, 이유찬
    # 입력 : str, 추출한 본문 내용
    # 내부 동작 : 본문을 미리 학습시킨 모델에 입력해 칭찬 비율, 비판 비율, 가이드라인 유사도를 얻고, 이를 다른 모델에 넣어 광고 확률을 구한다.
    # 출력 : tuple, (광고 확률 : float, 칭찬 비율 : float, 비판 비율 : float, 가이드라인 유사도 : float)
    # 기타 : 모델 학습은 다른 함수에서 진행, 해당 함수는 학습 완료된 모델을 사용
    prob : float # 광고 확률
    comp : float # 칭찬 비율
    crit : float # 비판 비율
    sim : float # 가이드라인 유사도

#csv학습모델
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import SimpleRNN, Embedding, Dense
import numpy as np

def train_and_save_model(data):
    X_data = data['Sentence']
    y_data = data['Label']

    y_data_encoded = pd.get_dummies(y_data)

    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data_encoded, test_size=0.2, random_state=0)

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_train)
    X_train_encoded = tokenizer.texts_to_sequences(X_train)
    
    vocab_size = len(tokenizer.word_index) + 1
    max_len = max(len(seq) for seq in X_train_encoded)
    X_train_padded = pad_sequences(X_train_encoded, maxlen=max_len)

    model = Sequential()
    model.add(Embedding(vocab_size, 32))
    model.add(SimpleRNN(32)) 
    model.add(Dense(3, activation='softmax'))

    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train_padded, y_train, epochs=4, batch_size=64, validation_split=0.2)

    model.save('sentiment_model.h5')

    return tokenizer, max_len

if __name__ == "__main__":
    data = pd.read_csv("adco_data_compcrit.csv")
    tokenizer, max_len = train_and_save_model(data)

#칭찬/비찬 예측함수
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

def split_sentences(text):
    sentences = re.split(r'[.!?]', text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

def load_and_predict(crawled_texts, tokenizer, max_len):
    model = load_model('sentiment_model.h5')
    
    compliments = 0
    criticisms = 0
    neutrals = 0

    for sentence in crawled_texts:
        encoded_sentence = tokenizer.texts_to_sequences([sentence])
        padded_sentence = pad_sequences(encoded_sentence, maxlen=max_len)
        prediction = model.predict(padded_sentence)
        
        label = np.argmax(prediction[0])
        if label == 0:
            compliments += 1
        elif label == 1:
            criticisms += 1
        else:
            neutrals += 1

    total_sentences = len(crawled_texts)
    print(f"칭찬 횟수/전체 문장 수: {compliments}/{total_sentences}")
    print(f"비판 횟수/전체 문장 수: {criticisms}/{total_sentences}")
    
if __name__ == "__main__":
    tokenizer, max_len = train_and_save_model(data) 


    texts = crawler("user_url_here")
    load_and_predict(texts, tokenizer, max_len)
