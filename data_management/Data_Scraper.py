
import requests
class DataScraper:

    def send_request(self, url, **kwargs):

        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            print("Error: ", e)
            return None

