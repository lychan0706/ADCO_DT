import requests
from bs4 import BeautifulSoup

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

        # 제목 추출
        title = soup.find("title")

        # 내용 추출 (일단 전체 문장 가져옴, 후에 요약 정리)
        iframe = soup.find('iframe', {'id': 'mainFrame'})
        if iframe and 'src' in iframe.attrs:
            iframe_url = "https://blog.naver.com" + iframe['src']
            iframe_response = requests.get(iframe_url)
            if iframe_response.status_code == 200:
                iframe_soup = BeautifulSoup(iframe_response.text, 'html.parser')
                content_div = iframe_soup.find('div', {'class': 'se-main-container'})
                if content_div:
                    content = content_div.get_text(strip=True)
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
        return (title, content, image_count)


    except Exception as e:
        print(f"Error: {e}")
        return None
    # 작성자 : 이휘민
    # 입력 : str, 네이버 블로그 url
    # 내부 동작 : 네이버 블로그 본문과 블로그 이름만을 추출한다. 이미지가 총 몇개 사용되었는지도 계산
    # 출력 : tuple, (본문 내용 : str, 블로그 이름 : str)

    #return "None" # test value
blog_url = "https://blog.naver.com/qksdnjfgml/223655887934"
result = crawler(blog_url)
if result:
    print(f"Result: {result}")
else:
    print("Invalid or unsupported Naver blog URL.")
