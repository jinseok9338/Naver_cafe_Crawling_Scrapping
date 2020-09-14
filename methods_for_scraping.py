import requests
import BeautifulSoup as bs
import re
import pandas as pd
import uuid
import requests
import rsa
import lzstring
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

class Methods:

    url_for_login_page = ""
    url_for_query_page ="" #First Page when we find item
    url_for_next_page =""   #Second Page when we find item

    #How can we access the page with credential That's the key Here
    #Teach Web Crawling first then Scraping then they realize that it's a different way of doing things and different mentality



    def __init__(self,item):
        self.query = item
        self.price = None
        self.num_of_item = 40
        self.date = None
        self.mean_price = False
        self.headers = "" #Put your header here
        self.response = requests.get(self.url)
        self.content = self.response.content
        self.naver_id =""
        self.naver_pw =""


    def find_the_urls_for_item(self,num_of_item = None):
        if not num_of_item:
            num_of_item = self.num_of_item
        else:
            num_of_item = num_of_item
        soup = bs(self.content,"html.parser")
        count = 0
        url = lists = soup.find_all('a' ,'href')

    def encrypt_account(self):  # userid , userpassword #This handles the encryption of id and pw
        key_str = requests.get('https://nid.naver.com/login/ext/keys.nhn').content.decode(
            "utf-8")  # key string is used for
        # print(key_str) # gnBuoug77ISvzejZGj5pa3APIz39jWdA,100015771,96286d60ec92a01165a1b3019038337ad420571320daa32f2b684ec17d5c30e578a83adb1e77d7f87602f35670e23d1e767b12d62a516081a8407a8e197b13dce80e057d7619b23a62a29afbd5e25d3816eba79d8e074ea360e08641795d04af81d781c537e7bc792aac3c57d240fb4e90a62ef04dcdb25d9eb79cc1528bd281,010001

        sessionkey, keyname, e_str, n_str = key_str.split(',')
        e, n = int(e_str, 16), int(n_str, 16)
        message = ''.join([chr(len(s)) + s for s in [sessionkey, self.naver_id, self.naver_pw]]).encode()
        # print(message) # b' JeDo3lxQ6oPSibsWr34Tm0dEROkk9VWR\x00\x00'
        pubkey = rsa.PublicKey(e, n)
        # print(pubkey) #PublicKey(134485779069419674894505277194872498267707146330362320468176405098541438197339275698384407038097261629096317107108911100858269802782749083671488837602624014535641733670469435496720926550167132724537741510732765210128804006550230739559919684832463977001404392191244441594678011773361936033807684267960536219327, 65537)
        encrypted = rsa.encrypt(message, pubkey).hex()
        # print(encrypted) # c3ccacf6fb2668abbf5bf2aa73d2937c1390604c78c17947bf1f33778b8d43a126d605ca27c9fde4f9450a2fd373e6b4a0e5ddb8e606e0ebb8686006855b8b67f8ded2cdb500ee22e3e24c298b64e981d4adea4c2554cba5cce0cc05036b83046cf40f694277509e3ca2615fb17b7c21a58c07af8a879e1cab79e20be90678f3

        return keyname, encrypted

    def naver_session(self):
        encnm, encpw = self.encrypt_account()

        s = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504]
        )

        s.mount('https://', HTTPAdapter(max_retries=retries))
        request_headers = {
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36" # Put your User_Agent here
        }

        bvsd_uuid = uuid.uuid4()
        encData = '{"a":"%s-4","b":"1.3.4","d":[{"i":"id","b":{"a":["0,%s"]},"d":"%s","e":false,"f":false},{"i":"%s","e":true,"f":false}],"h":"1f","i":{"a":"Mozilla/5.0"}}' % (
            bvsd_uuid, self.naver_id, self.naver_id, self.naver_pw)
        bvsd = '{"uuid":"%s","encData":"%s"}' % (bvsd_uuid, lzstring.LZString.compressToEncodedURIComponent(encData))

        resp = s.post('https://nid.naver.com/nidlogin.login', data={
            'svctype': '0',
            'enctp': '1',
            'encnm': encnm,
            'enc_url': 'http0X0.0000000000001P-10220.0000000.000000www.naver.com',
            'url': 'www.naver.com',
            'smart_level': '1',
            'encpw': encpw,
            'bvsd': bvsd
        }, headers=request_headers)

        finalize_url = re.search(r'location\.replace\("([^"]+)"\)', resp.content.decode("utf-8")).group(1)
        s.get(finalize_url)

        return s

    def find_information(self):
        price =""
        contact_info =""
        url_for_pic =""


    def find_mean_price(self):
        pass











