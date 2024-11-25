import numpy as np
from numpy import dot
from numpy.linalg import norm
import urllib.request
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Okt
import pandas as pd

def cossim(A : np.array, B : np.array) -> np.float64:
    return dot(A, B) / (norm(A) * norm(B))

def doc_sim(text : str) -> float:
    pass

def remove_spaces():
    with open("ADCO\\adco_data_words.csv", 'r', encoding= "UTF-8") as rfile:
        content = rfile.read()
    with open("ADCO\\adco_data_words.csv", 'w', encoding= "UTF-8") as wfile:
        new_content = ""
        for char in content:
            if char != ' ':
                new_content += char
        wfile.write(new_content)

def main() -> None:
    # 데이터 파일을 2차원 텐서로 변환
    with open('datas\\review_data.txt', 'r', encoding='UTF-8') as file:
        content = file.read()
    train_data = content.split('\n')[3:-1]
    for ite in range(len(train_data)):
        train_data[ite] = train_data[ite].split('|')[1]

    # 결손 데이터 제거
    print(f"데이터 갯수 : {len(train_data)}")
    temp = train_data.copy()
    train_data.clear()

    for ite in range(len(temp)):
        if temp[ite] != '':
            train_data.append(temp[ite])
    print(f"결손 데이터 제거 후 데이터 갯수 : {len(train_data)}")

    train_data = pd.Series(train_data)
    print(train_data[:3])
    train_data = train_data.str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","", regex=True)
    print(train_data[:10])

    # 불용어 정의
    stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

    # 형태소 분석기 OKT를 사용한 토큰화 작업 (다소 시간 소요)
    okt = Okt()
    


if (__name__ == "__main__"):
    main()