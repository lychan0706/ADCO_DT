# from adco_crawler import crawler
# from adco_model import model 

# 1. 네이버 블로그 링크 입력
# 2. 크롤러에 입력, 크롤러가 본문 내용 반환
# 3. 본문 내용을 광고 판정 모델에 입력, 광고 확률 및 인자들 반환
# 4. 시각화 및 설명

def crawler(url : str) -> tuple[str]: # 임시 함수
    # 작성자 : 이휘민
    # 입력 : str, 네이버 블로그 url
    # 내부 동작 : 네이버 블로그 본문과 블로그 이름만을 추출한다. 이미지가 총 몇개 사용되었는지도 계산
    # 출력 : tuple, (본문 내용 : str, 블로그 이름 : str)

    return "None" # test value

def adco_model(text : str) -> tuple[float]:
    # 작성자: 정윤수, 이유찬
    # 입력 : str, 추출한 본문 내용
    # 내부 동작 : 본문을 미리 학습시킨 모델에 입력해 칭찬 비율, 비판 비율, 가이드라인 유사도를 얻고, 이를 다른 모델에 넣어 광고 확률을 구한다.
    # 출력 : tuple, (광고 확률 : float, 칭찬 비율 : float, 비판 비율 : float, 가이드라인 유사도 : float)
    # 기타 : 모델 학습은 다른 함수에서 진행, 해당 함수는 학습 완료된 모델을 사용
    prob : float # 광고 확률
    comp : float # 칭찬 비율
    crit : float # 비판 비율
    sim : float # 가이드라인 유사도

    return 0.2 , 0.1, 0.0, 0.3 # test value

def main() -> None:
    equal_sign_num = 70 # 쓰잘데기 없음

    # 1. 네이버 블로그 링크 입력
    print('=' * equal_sign_num)
    user_url : str = input("Enter Naver Blog URL: ")
    # 예외 처리
    test_url_list : str = ["blog.naver.com", ] # 올바른 url이 입력되었는지 검사하는 url 리스트
    wrong_url : bool = True

    for test_url in test_url_list:
        if (test_url in user_url):
            wrong_url = False
            break
    if (wrong_url):
        raise Exception(f"Invalid URL: \"{user_url}\"")
    
    # 2. 크롤러에 입력, 크롤러가 본문 내용 반환
    text : str
    blogger_name : str

    try:
        text = crawler(user_url)[0] # text = 본문 내용; unicode
    # 예외 처리
    except:
        raise Exception("크롤러 내부 이슈")
    if (type(text) != str):
        raise TypeError(f"Invalid Type.\n{type(text) = }") # 크롤러가 본문 내용 반환 실패

    # 3. 본문 내용을 광고 판정 모델에 입력
    try:
        prob, comp, crit, sim = adco_model(text)
    # 예외 처리
    except:
        raise Exception("모델 내부 이슈")
    if (type(prob) != float):
        raise TypeError(f"Invalid Type.\n{type(prob) = }")
    if not (0 < prob < 1):
        raise ValueError(f"ad_probability Out of Range.\n{prob = }")
    
    # 4. 시각화 및 설명
    personal_opinion : float = comp + crit
    comp_ratio : float = comp / (personal_opinion)
    comp_status : int

    if (personal_opinion < 0.2):
        comp_status = -1
    elif (comp_ratio < 0.7):
        comp_status = 0
    elif (comp_ratio < 0.9):
        comp_status = 1
    else:
        comp_status = 2

    sim_status : int

    if (sim < 0.2):
        sim_status = 0
    elif (sim < 0.4):
        sim_status = 1
    else:
        sim_status = 2

    visual_prob : int = int(prob * 10) * 10

    # 시각화
    print('=' * equal_sign_num)

    print(f"광고 확률: {visual_prob}%")

    if (comp_status == -1):
        print("객관적인 정보가 대부분이며, 개인적 의견이 거의 들어가지 않았어요.")
    elif (comp_status == 0):
        print("적절한 비판과 함께 리뷰하고 있어요.")
    elif (comp_status == 1):
        print("칭찬 위주로 리뷰하고 있어요.")
    else:
        print("과도한 칭찬의 사용으로 광고임이 의심돼요.")

    if (comp_status == sim_status):
        print("그리고 ", end = "")
    else:
        print("하지만 ", end = "")

    if (sim_status == 0):
        print("광고에서 주로 보이는 단어가 많이 등장하지 않아요.")
    elif (sim_status == 1):
        print("조금씩 부자연스러운 단어가 보여요.")
    else:
        print("광고에서 주로 나타나는 단어 사용이 많이 발견됐어요.")

    print('=' * equal_sign_num)

    return None

if (__name__ == "__main__"):
    main()