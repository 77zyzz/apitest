import requests
import json


class baseapi():
    def list_all_member(self):
        # 获取所有成员变量，排除掉成员函数
        attributes = [a for a in dir(self) if not callable(getattr(self, a))]
        attributes=[a for a in attributes if not a.startswith('__')]
        return attributes

# Censys可以免费注册获取API：https://censys.io/api
class censys(baseapi):
    censys_api_id = None
    censys_api_secret = None


    def run(self):

        data = {
            'query': f'parsed.names:google.com',
            'page': 1,
            'fields': ['parsed.subject_dn', 'parsed.names'],
            'flatten': True}
        resp = requests.post('https://search.censys.io/api/v1/search/certificates', json=data, auth=(self.censys_api_id, self.censys_api_secret))
        if not resp:
            return
        json = resp.json()
        status = json.get('status')
        if status == 'ok':
            return True
        else:
            return False




#这个不对，要重新写
# Bing可以免费注册获取API：https://azure.microsoft.com/zh-cn/services/
class bing(baseapi):
    ACCESS_KEY = ""
    def run(self):
        URL = "https://api.cognitive.microsoft.com/bing/v7.0/search"

        headers = {
            "Ocp-Apim-Subscription-Key": self.ACCESS_KEY
        }

        params = {
            "q": "Python"
        }

        response = requests.get(URL, headers=headers, params=params)

        if response.status_code == 200:
            return True
        else:
            return False

# SecurityTrails可以免费注册获取API：https://securitytrails.com/corp/api
class SecurityTrails(baseapi):
    securitytrails_api = None

    def run(self):
        URL = "https://api.securitytrails.com/v1/domains/search"

        headers = {
            "APIKEY": self.securitytrails_api
        }

        params = {
            "query": "example.com"
        }

        response = requests.get(URL, headers=headers, params=params)

        if response.status_code == 200:
            return True
        else:
            return False

# https://fofa.so/api
class fofa(baseapi):
    email = ""
    key = ""
    def run(self):

        url = "https://fofa.so/api/v1/info/my?email={}&key={}".format(self.email, self.key)

        # Send the request to the fofa API
        response = requests.get(url,verify = False)

        if response.status_code == 200:
            return True
        else:
            return False



class shodan(baseapi):

    API_KEY = "YOUR_API_KEY"
    def run(self):
        URL = "https://api.shodan.io/shodan/host/search"

        headers = {
            "Authorization": f"Basic {self.API_KEY}"
        }

        params = {
            "query": "ssh"
        }

        response = requests.get(URL, headers=headers, params=params)

        if response.status_code == 200:
            return True
        else:
            return False


















