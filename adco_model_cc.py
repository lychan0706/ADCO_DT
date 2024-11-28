from time import time
start = time()
from googletrans import Translator
from textblob import TextBlob
# from nltk.tokenize import sent_tokenize
# import nltk
from adco_model_sim import tokenize
print(f"[adco_model_cc] importing completed : {time() - start:.2} sec")

def cc_model(text : str) -> tuple[float]:
    """
    Parameter : text -> 크롤링 된 리뷰의 본문
    Return : sentiments, subjectivity -> 리뷰의 감정 및 주관성 점수
    
    본문을 받아 영어로 번역 후 미리 훈련된 감정 분류기를 사용해 모든 문장의 평균 감정 점수와 주관성 점수를 산출
    """
    start = time()
    # 번역 후 토큰화
    translator = Translator()
    translated_text = translator.translate(text, src="ko", dest="en").text
    print(f"[adco_model_cc] translation completed : {time() - start:.2} sec")
    start = time()

    # nltk.download('punkt_tab')
    # sentences = sent_tokenize(translated_text)
    delim = '.:;!?\t\n(){[}]\"'
    sentences = tokenize(translated_text, delim = delim) # 최적화 문제로 직접 만든 함수 사용
    print(f"[adco_model_cc] sectence tokenization completed : {time() - start:.2} sec")
    start = time()
    
    senti_list = []
    subj_list = []

    for sentence in sentences:
        blob = TextBlob(sentence)

        senti = (blob.sentiment.polarity + 1) / 2
        senti_list.append(senti)
        
        subj = blob.sentiment.subjectivity
        subj_list.append(subj)

    # print(f"[adco_model_cc] {senti_list = }, {subj_list = }") # debug

    avg_sentiment = sum(senti_list) / len(senti_list) if senti_list else 0
    avg_subjectivity = sum(subj_list) / len(subj_list) if subj_list else 0
    print(f"[adco_model_cc] senti, subj calculation completed : {time() - start:.2} sec")
    start = time()

    # print(f"평균 Sentiment (감정 점수): {avg_sentiment:.2f}") # debug
    # print(f"평균 Subjectivity (주관성 점수): {avg_subjectivity:.2f}") # debug
    return avg_sentiment, avg_subjectivity

if (__name__ == "__main__"):
    text=("텍스트 블롭은 감정 분류를 거지같이 하고 주관성 검사도 정말 못하는 것 같다. 그래서 나는 너무 속상하다")
    print(cc_model(text))