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

import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import SimpleRNN, Embedding, Dense
from tensorflow.keras.models import Sequential

data = adco_data_compcrit

X_data = data['neut']  
# 여기서는 'neut'가 faeture값임에도 중립적인 문장을 포함한 데이터처럼 사용, 칭찬/비판에 비해 중요도가 크지 않은 특성이기에 이렇게 입력 데이터 값으로 사용하여 모델 학습 진행합니당 
y_data = data[['comp', 'crit']]  # 이진 분류를 위한 두 레이블

X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=0)

tokenizer = Tokenizer() #문장의 토큰 인덱스 생성 
tokenizer.fit_on_texts(X_train)
X_train_encoded = tokenizer.texts_to_sequences(X_train) #문장을 정수 시퀀스로 변환

vocab_size = len(tokenizer.word_index) + 1
max_len = max(len(seq) for seq in X_train_encoded)
X_train_padded = pad_sequences(X_train_encoded, maxlen=max_len) #각 문장의 길이를 max_len으로 패딩 

embedding_dim = 32
hidden_units = 32

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim))
model.add(SimpleRNN(hidden_units))
model.add(Dense(2, activation='softmax'))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['acc'])

model.fit(X_train_padded, y_train, epochs=4, batch_size=64, validation_split=0.2) #에폭값은 4번으로 설정, 만일 정확도 떨어질시, 에폭수 증가시켜야함 

compliments = 0
criticisms = 0
for sentence in crawled_texts:
    encoded_sentence = tokenizer.texts_to_sequences([sentence])
    padded_sentence = pad_sequences(encoded_sentence, maxlen=max_len)
    prediction = model.predict(padded_sentence)
    
    if prediction[0][0] > prediction[0][1]:
        compliments += 1
    else:
        criticisms += 1

total_sentences = len(crawled_texts)
print(f"칭찬 횟수/전체 문장 수: {compliments}/{total_sentences}")
print(f"비판 횟수/전체 문장 수: {criticisms}/{total_sentences}") 
