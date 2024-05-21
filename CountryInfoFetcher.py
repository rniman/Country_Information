import http.client
from xml.etree import ElementTree
from html import unescape
import re

class CountryInfoFetcher:
    def __init__(self, service_key):
        self.url = "apis.data.go.kr"
        self.service_key = service_key
        self.query = f"/1262000/CountryBasicService/getCountryBasicList?serviceKey={service_key}&numOfRows=200"
        self.NA_NUM = 0
        self.NA_POP_NUM = 0

    def fetch_country_data(self):
        # API 요청 보내기
        conn = http.client.HTTPConnection(self.url)
        conn.request("GET", self.query)
        req = conn.getresponse()

        if req.status == 200:
            strXml = req.read().decode('utf-8')
            return strXml
        else:
            print(f"Error: {req.status} {req.reason}")
            return None

    def parse_country_data(self, xml_data):
        # XML 데이터 파싱하기
        tree = ElementTree.fromstring(xml_data)
        item_elements = tree.iter("item")  # item 엘리먼트를 가져옴

        country_list = []
        for item in item_elements:
            country_name = item.findtext("countryName", default="N/A")
            country_eng_name = item.findtext("countryEnName", default="N/A")
            continent = item.findtext("continent", default="N/A")
            country_id = int(item.findtext("id", default='-1'))
            country_basic = item.findtext("basic", default="N/A")
            country_basic = self.clean_html(country_basic)
            country_img_url = item.findtext("imgUrl", default="N/A")
            population, area = self.extract_additional_info(country_basic)
            country_list.append({
                "country_name": country_name,
                "country_eng_name": country_eng_name,
                "continent": continent,
                "country_id": country_id,
                "country_basic": country_basic,
                "country_img_url": country_img_url,
                "population": population,
                "area": area
            })

        return country_list

    def clean_html(self, raw_html):
        clean_text = unescape(raw_html)  # Convert HTML entities
        clean_text = re.sub('<br\s*/?>', '\n', clean_text)  # Convert <br> to new lines
        clean_text = re.sub('<.*?>', '', clean_text)  # Remove remaining HTML tags
        return clean_text

    def extract_additional_info(self, basic_info):
        # 인구수 및 면적 추출
        population = "N/A"
        area = "N/A"

        population_match = re.search(r'인구\s*[:약]*\s*([\d,]+)\s*만*명*', basic_info)
        area_match = re.search(r'면적\s*:\s*([\d,만]+)', basic_info)

        if population_match:
            population_text = population_match.group(1).replace(',', '')
            if '만' in population_match.group(0):
                population = str(int(float(population_text) * 10000))
            else:
                population = population_text

        if area_match:
            area_text = area_match.group(1).replace(',', '')  # Remove commas
            if '만' in area_text:
                area_text = area_text.replace('만', '')
                try:
                    area = str(int(float(area_text) * 10000))
                except ValueError:
                    area = "N/A"  # Handle potential conversion errors
            else:
                area = area_text

        if population == "N/A":
            self.NA_POP_NUM += 1

        if area == "N/A":
            self.NA_NUM += 1

        return population, area

    def print_country_data(self, country_list):
        # 파싱한 국가 데이터 출력하기
        for index, country in enumerate(country_list):
            print(f"[{index + 1}] 국가명: {country['country_name']}")
            print(f"영문명: {country['country_eng_name']}")
            print(f"대륙: {country['continent']}")
            print(f"이미지 URL: {country['country_img_url']}")
            print(f"국가코드: {country['country_id']}")
            print(f"인구수: {country['population']}")
            print(f"면적: {country['area']} km^2\n")
            # print(f"국가 기본정보: {country['country_basic']}\n\n")

# 클래스 사용 예제
service_key = "TM2mB7BkLj7%2B1mK%2FbNgWbxjMPtdffuyVQbT46zhjwGtnC%2FEA6FQwymPyHVNcFFdJN%2FaQuqSYutGF33dW20COZg%3D%3D"
fetcher = CountryInfoFetcher(service_key)

xml_data = fetcher.fetch_country_data()
if xml_data:
    country_list = fetcher.parse_country_data(xml_data)
    fetcher.print_country_data(country_list)

print(fetcher.NA_NUM)
print(fetcher.NA_POP_NUM)