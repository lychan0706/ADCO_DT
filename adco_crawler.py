import requests
from bs4 import BeautifulSoup
import re

#def remove_emojis(text):
    #emoji_pattern = re.compile(
        #"[\U00010000-\U0010FFFF" # 유니코드 이모티콘 범위
        #"\U0001F600-\U0001F64F" # 웃는 얼굴 및 감정
        #"\U0001F300-\U0001F5FF" # 기호 및 픽토그램
        #"\U0001F680-\U0001F6FF" # 교통 및 지도 기호
        #"\U0001F700-\U0001F77F" # 알케미 기호
        #"\U0001F780-\U0001F7FF" # 기타 기호
        #"\U0001F800-\U0001F8FF" # 추가 기호
        #"\U0001F900-\U0001F9FF" # 손동작 및 추가 이모티콘
        #"\U0001FA00-\U0001FAFF" # 도구 및 객체
        #"\U00002702-\U000027B0" # 기호
        #"\U0001F1E6-\U0001F1FF" # 국기
        #"\U00002600-\U000026FF" # 추가 기호 및 기호 확장
        #"\U00002700-\U000027BF" # 추가 기호 및 기호 확장
        #"\U0001F550-\U0001F567" # 시계 이모티콘
        #"\U00002728"            # 별: ✨
        #"\U00002B50"            # 별: ⭐
        #"\U00002605-\U00002606" # 별: ★, ☆
        #"\U0000231A-\U0000231B"   # 손목시계 (⌚) 및 모래시계 (⌛)
        #"\U0001F570"              # 기타 시계 이모티콘 (🕰️)
        #"\u200d"                  # Zero Width Joiner (글자 연결 기호)
        #"\ufe0f"                  # Variation Selector (이모티콘 변형)
        #"]+",  # 유니코드 이모티콘 범위
        #flags=re.UNICODE,
    #)   
    #return emoji_pattern.sub(r"", text)

    ##emoji_pattern = re.compile(
    ##    "[\U00010000-\U0010FFFF]",  # 유니코드 이모티콘 범위
    ##    flags=re.UNICODE,
    ##)
    ##return emoji_pattern.sub(r"", text)

    #"\U000024C2-\U0001F251"  # 기타

def filter_allowed_characters(text):
    # 허용 범위: 한글, 영문자, 숫자, 공백, 특정 기호
    allowed_pattern = re.compile(r"[^a-zA-Z0-9ㄱ-ㅎ가-힣\s!@#$%^&*()\-_=+\[\]{};:'\",.<>/?\\|`~]")
    return allowed_pattern.sub(" ", text)

def fix_spacing(text):
    # 1. 문장부호 뒤에 공백 추가
    text = re.sub(r"([.,!?])(?=\S)", r"\1 ", text)

    # 2. 숫자와 문자 사이에 공백 추가
    text = re.sub(r"(\d)([가-힣a-zA-Z])", r"\1 \2", text)
    text = re.sub(r"([가-힣a-zA-Z])(\d)", r"\1 \2", text)

    # 3. 영어 단어와 한글 사이에 공백 추가
    text = re.sub(r"([a-zA-Z])([가-힣])", r"\1 \2", text)
    text = re.sub(r"([가-힣])([a-zA-Z])", r"\1 \2", text)

    # 4. 연속된 공백을 하나로 줄임
    text = re.sub(r"\s+", " ", text).strip()

    return text


def remove_substring(input_string, substring_to_remove):
    return input_string.replace(substring_to_remove, " ")

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
                    content_div = remove_substring(content_div, "\u200b")
                    content_div = filter_allowed_characters(content_div)
                    content_div = fix_spacing(content_div)
                    #for i in range(0, len(content_div)):
                    #    if (content_div[i:i+2] == "  "):
                    #        content_div = content_div[:i+1] + content_div[i+2:]
                    content = content_div
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

if (__name__ == "__main__"):
    blog_url = "https://blog.naver.com/cherry_27_/223665563506"
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
