import random
import requests

from bs4 import BeautifulSoup
    
class Breaker:
    def __init__(self, proxies):
        self.session = requests.Session()
        self.proxies = proxies

    def authorize(self, token, authorize_url, guild):
        if self.proxies == None:
            proxies = None
        else:
            proxy = random.choice(self.proxies)
            proxies = {
                "http": proxy,
                "https": proxy
            }

        authorize_endpoint_url = authorize_url.replace("https://discord.com/oauth2/authorize", "https://discord.com/api/v9/oauth2/authorize")

        response = self.session.post(
            authorize_endpoint_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": token
            },
            json={
                "authorize": True,
                "guild_id": guild,
                "integration_type": 0,
                "permissions": "0"
            },
            proxies=proxies
        )

        if response.status_code == 200:
            return True, response.json()["location"]
        else:
            return False, None
        
    def verify(self, location):
        html = self.session.get(location).text

        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("title").get_text()

        if "成功" in title:
            return True
        else:
            return False