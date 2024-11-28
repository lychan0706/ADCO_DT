from time import time
start = time()
total = time()
from adco_crawler import crawler
from adco_model_cc import cc_model
from adco_model_sim import sim_model
from adco_model_prob import prob_model
print(f"[adco_main] total importing completed : {time() - start:.2} sec")

# 1. 네이버 블로그 링크 입력
# 2. 크롤러에 입력, 크롤러가 본문 내용 반환
# 3. 본문 내용을 광고 판정 모델에 입력, 광고 확률 및 인자들 반환
# 4. 시각화 및 설명

def main(user_url = 'None') -> None:
    equal_sign_num = 70 # 쓰잘데기 없음
    start = time()

    # 1. 네이버 블로그 링크 입력
    if user_url == 'None':
        print('=' * equal_sign_num)
        user_url : str = input("Enter Naver Blog URL: ")

    print('=' * equal_sign_num)
    # 예외 처리
    test_url_list : str = ["blog.naver.com", ] # 올바른 url이 입력되었는지 검사하는 url 리스트
    wrong_url : bool = True
    
    for test_url in test_url_list:
        if (test_url in user_url):
            wrong_url = False
            break
    if (wrong_url):
        raise Exception(f"Invalid URL: \"{user_url}\"")
    
    print(f"[adco_main] getting url completed : {time() - start:.2} sec")
    start = time()
    
    # 2. 크롤러에 입력, 크롤러가 본문 내용 반환
    text : str
    blogger_name : str

    text, title, image_count = crawler(user_url) # text = 본문 내용; utf-8

    # 예외 처리
    if (type(text) != str):
        raise TypeError(f"Invalid Type.\n{type(text) = }") # 크롤러가 본문 내용 반환 실패
    
    print(f"[adco_main] crawling text completed : {time() - start:.2} sec")
    start = time()

    # 3. 본문 내용을 광고 판정 모델에 입력
    # 수정 사항 : comp crit x -> 감정 점수, 주관성 점수 
    senti, subj = cc_model(text)
    sim = sim_model(text, 0.8, 100000)

    prob = prob_model(senti, subj, sim)
    
    # 예외 처리
    if (type(prob) != float):
        raise TypeError(f"Invalid Type.\n{type(prob) = }")
    if not (0 < prob < 1):
        raise ValueError(f"prob Out of Range.\n{prob = }")
    
    print(f"[adco_main] calculate parameters completed : {time() - start:.2} sec")
    start = time()

    # 4. 시각화 및 설명
    if (subj < 0.2):
        senti_status = -1
    elif (senti < 0.1):
        senti_status = 0
    elif (senti < 0.5):
        senti_status = 1
    else:
        senti_status = 2

    sim_status : int

    if (sim < 0.05):
        sim_status = 0
    elif (sim < 0.01):
        sim_status = 1
    else:
        sim_status = 2

    visual_prob : int = int(prob * 10) * 10

    # 시각화
    print('=' * equal_sign_num)
    print(f"리뷰 제목 : {title}\n리뷰 URL : {user_url}\n광고 확률: {visual_prob}%")

    match (senti_status):
        case -1:
            print("객관적인 정보가 대부분이며, 개인적 의견이 거의 들어가지 않았어요.")
        case 0:
            print("적절한 비판과 함께 리뷰하고 있어요.")
        case 1:
            print("칭찬 위주로 리뷰하고 있어요.")
        case 2:
            print("과도한 칭찬의 사용으로 광고임이 의심돼요.")

    if ((senti_status > 0) ^ (sim_status > 0)):
        print("하지만 ", end = "")
    else:
        print("그리고 ", end = "")

    match (sim_status):
        case 0:
            print("광고에서 주로 보이는 단어가 많이 등장하지 않아요.")
        case 1:
            print("조금씩 부자연스러운 단어가 보여요.")
        case 2:
            print("광고에서 주로 나타나는 단어 사용이 많이 발견됐어요.")

    print('=' * equal_sign_num)
    print(f"[adco_main] {senti = :.2}, {subj = :.2}, {sim = :.2}, {prob = :.2}") # debug
    print(f"[adco_main] debug completed : {time() - start:.2} sec")
    
    print(f"{senti = }, {subj = }, {sim = }, {prob = }")

# 최종 디버그
if (__name__ == "__main__"):
    main('https://blog.naver.com/rkdminjee/223654824755')
    print(f"[adco_main] total time spent : {time() - total:.5} sec")