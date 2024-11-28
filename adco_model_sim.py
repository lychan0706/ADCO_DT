from time import time
start = time()
from gensim.models import word2vec
from googletrans import Translator
# from tensorflow.keras.preprocessing.text import text_to_word_sequence
print(f"[adco_model_sim] importing completed : {time() - start:.2} sec")

def tokenize(text : str, delim : str) -> list[str]:
    tokens = []
    token = ''
    for char in text:
        if char not in delim:
            token += char
        elif token:
            tokens.append(token)
            token = ''
        else:
            continue
    tokens.append(token)
    return tokens

def translate_csv(path : str):
    # 번역기 초기화
    trans = Translator()

    # 파일 읽기
    with open(path, 'r', encoding='utf-8') as file:
        words = file.read().split(',')

    # 번역하기
    for ite in range(len(words)):
        words[ite] = trans.translate(words[ite], dest='en').text

    # 파일 쓰기
    content = ''
    for word in words:
        content += word + ','
    content = content[:-1]

    with open(path, 'w') as file:
        file.write(content)

def foo():
    data_path = 'C:\\Users\\ychn0\\OneDrive\\문서\\MyProgram\\Python\\pretrained_w2v_model.bin'
    model : word2vec.KeyedVectors = word2vec.KeyedVectors.load_word2vec_format(data_path, binary=True, limit=30000)
    print(model.vectors.shape)
    model.save_word2vec_format("datas\\short_w2v_model.bin")

def sim_model(text : str, threshold : float = 0.75, limit : int = 20000) -> float:
    """
    Parameter : text -> 크롤링 된 리뷰의 본문, threshold -> 단어의 유사성 판단 기준, limit -> 불러오는 데이터셋의 크기
    Return : similarity -> 기준 단어와 본문에 사용된 단어의 유사성
    limit은 못해도 5만개 이상이 되어야 정상적인 유사도를 산출해낼 수 있다
    0.1초에 약 2만개를 불러온다
    """
    start = time()

    # 미리 학습된 모델 불러오기
    # data_path = 'datas\\pretrained_w2v_model.bin' # 불러오는데 14초 -> 성능저하 극심
    data_path = 'datas\\short_w2v_model.bin' # 데이터셋 간소화 -> 300만개에서 50만개로 축소
    model : word2vec.KeyedVectors = word2vec.KeyedVectors.load_word2vec_format(data_path)
    # model : word2vec.KeyedVectors = word2vec.KeyedVectors.load(data_path)
    
    # model = word2vec.Word2Vec.load(data_path)

    # print(f"[adco_model_sim] data set size : {model.vectors.shape[0]} rows")
    print(f"[adco_model_sim] model reading completed : {time() - start:.2} sec")
    start = time()

    # 본문 번역하기
    trans = Translator()
    en_text = trans.translate(text=text, dest='en').text
    print(f"[adco_model_sim] translation completed : {time() - start:.2} sec")
    start = time()

    # 기준 단어 불러오기 
    csv_path = 'datas\\adco_data_words.csv'
    with open(csv_path, 'r', encoding='UTF-8') as csv_file:
        std_words = csv_file.read().split(',')
    print(f"[adco_model_sim] file reading completed : {time() - start:.2} sec")
    start = time()
    
    # 토큰화 진행
    # tokenized_text = text_to_word_sequence(en_text) 최적화 문제: import 시간 2.2초 단축, tokenize 시간 0.3초 단축
    delim = ' .,:;!?\t\n(){[}]\'\"'
    tokenized_text = tokenize(en_text, delim) # 최적화로 새로 만든 함수
    word_count = len(tokenized_text)
    print(f"[adco_model_sim] tokenization completed: {time() - start:.2} sec")
    start = time()

    # 유사도 계산
    sim_count = 0
    for token in tokenized_text:
        flag = False
        for std_word in std_words:
            local_sim : float = 0
            try:
                # local_sim = model.wv.similarity(std_word, token)
                local_sim = model.similarity(std_word, token)
                local_sim = (local_sim + 1) / 2
            except KeyError:
                pass
            except Exception as e:
                raise e
            if local_sim > threshold:
                # print(f"{std_word}, {token} = {local_sim}") # debug
                flag = True
                break
        if flag:
            sim_count += 1
    print(f"[adco_model_sim] similarity calculation completed : {time() - start:.2} sec")
    start = time()

    sim = sim_count / (word_count)
    return sim

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
    content : str = '''매장 분위기

손님이 많아서 요리조리 피해 찍다가

다 빠진 틈에 찍어본 사진 ㅎㅎ

​

물 셀프 정수기, 아기의자 있고

핸드폰 충전기, 대기 공간, 손 씻는 공간이 있다

​

내가 처음 방문한 2016년부터 지금까지 언제 가도

똑같이 깨끗하고 깔끔한 매장 :)'''
    sim : float = sim_model(text = content)
    print(sim)

if (__name__ == "__main__"):
    # main()
    foo()
    # translate_csv('datas\\adco_data_words.csv')