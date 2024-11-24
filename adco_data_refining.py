from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
from math import log
from adco_crawler import remove_emojis

def move_to_end(driver, times = 1):
    for i in range(times):
        wait(0.5)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

def init_file(file_dir):
    with open(file_dir, 'r', encoding='UTF-8') as file:
        if (len(file.read()) != 0):
            return
    with open(file_dir, 'w', encoding='UTF-8') as file:
        file.write(f'# line index 1 : total data 수, line index 3부터 data\n0\n000id|content\n')

def wait(times = 1):
    if (times <= 1):
        time.sleep(times)
        return
    for i in range(times, 0, -1):
        print(f"wating... {i} seconds left")
        time.sleep(1)

def write_html(url, max_tries = 1, headless = True):

    # Webdriver 세팅
    options = webdriver.ChromeOptions()
    if (headless):
        options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # # BS4 세팅
    # session = requests.Session()
    # headers = {
    #     "User-Agent": "user value"}

    # retries = Retry(total=5,
    #                 backoff_factor=0.1,
    #                 status_forcelist=[500, 502, 503, 504])

    # session.mount('http://', HTTPAdapter(max_retries=retries))

    html = ''

    try:
        # 더보기 존나 누르기
        # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        res = driver.get(url)
        driver.implicitly_wait(30)
        # Pagedown
        move_to_end(driver=driver, times=3)
        wait(1)
        tried_times = 0
        try:
            seemore_button = '#app-root > div > div > div > div:nth-child(6) > div:nth-child(2) > div.place_section.k1QQ5 > div.NSTUp > div > a' # 더보기 버튼
            for i in range(max_tries):
                temp = time.time()
                wait(1)
                driver.find_element(By.CSS_SELECTOR, seemore_button).click()
                move_to_end(driver=driver, times=2)
                tried_times += 1
                print(f"No. {i + 1} / {max_tries}, time spent: {- temp + time.time():.2f} sec")
        except Exception as e:
            print(f'stopped at {tried_times} times\n{e}')
        else :
            print(f'{max_tries} times completed')
        # 더보기 존나 누르기 끝

        wait(5 + int(log(tried_times, 2)))

        # html 가져오고 저장
        html = driver.page_source
        driver.close()
        
    except Exception as e:
        print(f"write_html: {e}")
        
    # with open("review source.txt", 'w', encoding="UTF-8") as file:
    #     file.write(html)
    return html

def extract_data(html, file_dir):
    # 저장한 html : str
    # file = open("review source.txt", 'r', encoding="UTF-8")
    # html = file.read()

    # 저장 csv 설정
    with open(file_dir, 'r', encoding="UTF-8") as rfile:
        data = rfile.read()
    total_data_num = len(data.split('\n')) - 4

    data_file = open(file_dir, 'w', encoding="UTF-8")

    try:
        # bs = BeautifulSoup(html, 'lxml')
        # reviews = bs.select('li.pui__X35jYm.EjjAW')

        reviews : list[str] = html.split("pui__vn15t2")[2:]

        total = len(reviews)
        print(f"total reviews : {total}")

        done = 0
        for re in reviews:
            # str manip
            content = re.split('xtsQN', maxsplit=1)[1].split('>', maxsplit=1)[1].split('</a>', maxsplit=1)[0].replace('<br>', ' ')
            # append sheet
            done += 1
            data += f"{done + total_data_num:0>5}|{content}\n"
        
        print(f"total reviews done : {done}")

    except Exception as e:
        print(f"extract_data: {e}")

    finally:
        # Save the file
        temp = data.split('\n', maxsplit=2)
        data = temp[0] + '\n총 ' + str(done + total_data_num) + '개\n' + temp[2]
        data_file.write(data)

    data_file.close()

def remove_emoji_process(file_dir):
    
    with open(file_dir, 'r', encoding='UTF-8') as file:
        content = file.read()

    with open(file_dir, 'w', encoding='UTF-8') as file:
        content = remove_emojis(content)
        file.write(content)
    
def main():
    file_dir = "datas\\review_data.txt" # csv로 하면 코드 요상해짐, '|'로 나누는 txt 파일 사용
    # 파일 생성
    init_file(file_dir=file_dir)
    
    # id_list = [1301313289] # test id
    id_list = [1301313289,1213806029,1750052528,1557359092,36357696,1137448595,1932032424,1801968019,1725794491]
    max_tries   = 40    # 40 이후로 급격히 느려짐... headless True 하면 빠르긴 한데
    headless    = False # headless True로 하면 source 이상해짐
    for id in id_list:
        url = f'https://m.place.naver.com/restaurant/{id}/review/visitor?entry=ple' # 추천순 정렬

        # 더보기 존나 누르고 html 저장
        html = write_html(url, max_tries, headless)

        # html 저장한거 불러와서 리뷰 추출
        extract_data(html=html, file_dir=file_dir)
    
    # emoji removal process 휘민씨 고마워요
    remove_emoji_process(file_dir=file_dir)

if (__name__ == "__main__"):
    main()
    # remove_emoji_process("datas\\review_data.txt")