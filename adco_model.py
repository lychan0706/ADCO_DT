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

    return 0.2 , 0.1, 0.0, 0.3 # test value