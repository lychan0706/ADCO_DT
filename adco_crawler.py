import requests
from bs4 import BeautifulSoup
import re

def remove_emojis(text):
    emoji_pattern = re.compile(
        "[\U00010000-\U0010FFFF" # 유니코드 이모티콘 범위
        "\U0001F600-\U0001F64F" # 웃는 얼굴 및 감정
        "\U0001F300-\U0001F5FF" # 기호 및 픽토그램
        "\U0001F680-\U0001F6FF" # 교통 및 지도 기호
        "\U0001F700-\U0001F77F" # 알케미 기호
        "\U0001F780-\U0001F7FF" # 기타 기호
        "\U0001F800-\U0001F8FF" # 추가 기호
        "\U0001F900-\U0001F9FF" # 손동작 및 추가 이모티콘
        "\U0001FA00-\U0001FAFF" # 도구 및 객체
        "\U00002702-\U000027B0" # 기호
        "\U0001F1E6-\U0001F1FF" # 국기
        "]+",  # 유니코드 이모티콘 범위
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r"", text)

    #"\U000024C2-\U0001F251"  # 기타


def remove_substring(input_string, substring_to_remove):
    return input_string.replace(substring_to_remove, "")

def crawler(url : str) -> tuple[str]: # 임시 함수
    try:
        # URL 확인
        if "blog.naver.com" not in url:
            return None
        
        # HTML 가져오기
        response = requests.get(url)

        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # 내용 추출
        iframe = soup.find('iframe', {'id': 'mainFrame'})
        if iframe and 'src' in iframe.attrs:
            iframe_url = "https://blog.naver.com" + iframe['src']
            iframe_response = requests.get(iframe_url)
            if iframe_response.status_code == 200:
                iframe_soup = BeautifulSoup(iframe_response.text, 'html.parser')
                content_div = iframe_soup.find('div', {'class': 'se-main-container'})
                # 제목 추출
                title_div = iframe_soup.find('div', {'class': 'se-module se-module-text se-title-text'})
                title = title_div.get_text(strip=True)
                #title = remove_substring(title_div, "\u200b")
                if content_div:
                    #전체 내용
                    content_div = content_div.get_text(strip=True)
                    content = remove_substring(content_div, "\u200b")
                    content = remove_emojis(content)
                else:
                    content = '내용을 가져올 수 없음'
                # 이미지 갯수
                images = iframe_soup.find_all('img')
                image_count = str(len(images))
            else:
                content = '내용을 가져올 수 없음'
                image_count = '0'
        else:
            content = '내용을 가져올 수 없음'
            image_count = '0'

        # tuple로 반환
        return (content, title, image_count)


    except Exception as e:
        print(f"Error: {e}")
        return None

blog_url = "https://blog.naver.com/happymil_0/223599083052"
result = crawler(blog_url)
if result:
    print(f"Result: {result}")
else:
    print("Invalid or unsupported Naver blog URL.")

# 작성자 : 이휘민
    # 입력 : str, 네이버 블로그 url
    # 내부 동작 : 네이버 블로그 본문과 블로그 이름만을 추출한다. 이미지가 총 몇개 사용되었는지도 계산
    # 출력 : tuple, (본문 내용 : str, 블로그 이름 : str)

    #return "None" # test value
