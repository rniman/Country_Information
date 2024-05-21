import http.client
from xml.etree import ElementTree
from html import unescape
import re
import json

class CountryInfoFetcher:
    def __init__(self, service_key):
        self.url = "apis.data.go.kr"
        self.service_key = service_key
        self.basic_query = f"/1262000/CountryBasicService/getCountryBasicList?serviceKey={service_key}&numOfRows=200"
        self.overview_query = f"/1262000/OverviewGnrlInfoService/getOverviewGnrlInfoList?serviceKey={service_key}&numOfRows=200"

    def fetch_country_data(self, query):
        # API 요청 보내기
        conn = http.client.HTTPConnection(self.url)
        conn.request("GET", query)
        req = conn.getresponse()

        if req.status == 200:
            response_data = req.read().decode('utf-8')
            return response_data
        else:
            raise Exception(f"Error: {req.status} {req.reason}")

    def parse_basic_data(self, xml_data):
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
            if country_name == '대만':  # 대만 국기 오류 있어서 이것만 직접 수정
                country_img_url = 'data:image/png;base64,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'
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
        country_list.sort(key=lambda x: x["country_name"])

        return country_list

    def parse_overview_data(self, json_data):
        # JSON 데이터 파싱하기
        try:
            overview_items = json.loads(json_data)
            overview_data = {}
            for item in overview_items.get("data", []):
                country_name = item.get("country_nm", "N/A")
                population = item.get("population", "N/A")
                area = item.get("area", "N/A")

                overview_data[country_name] = {
                    "population": population,
                    "area": area
                }

            return overview_data
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return {}

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

        return population, area

    def merge_data(self, basic_data, overview_data):
        # N/A 값 보충하기
        for country in basic_data:
            name = country["country_name"]
            if name in overview_data:
                if country["population"] == "N/A":
                    country["population"] = overview_data[name].get("population", "N/A")
                if country["area"] == "N/A":
                    country["area"] = overview_data[name].get("area", "N/A")
        return basic_data

    def print_country_data(self, country_list):
        # 파싱한 국가 데이터 출력하기
        for index, country in enumerate(country_list):
            print(f"[{index + 1}] 국가명: {country['country_name']}")
            print(f"영문명: {country['country_eng_name']}")
            print(f"대륙: {country['continent']}")
            print(f"이미지 URL: {country['country_img_url']}")
            print(f"국가코드: {country['country_id']}")
            print(f"인구수: {country['population']}")
            print(f"면적: {country['area']} km^2")
            print(f"국가 기본정보: {country['country_basic']}\n\n")


# 클래스 사용 예제
# service_key = "TM2mB7BkLj7%2B1mK%2FbNgWbxjMPtdffuyVQbT46zhjwGtnC%2FEA6FQwymPyHVNcFFdJN%2FaQuqSYutGF33dW20COZg%3D%3D"
# fetcher = CountryInfoFetcher(service_key)
#
# basic_xml_data = fetcher.fetch_country_data(fetcher.basic_query)
# overview_json_data = fetcher.fetch_country_data(fetcher.overview_query)
#
# if basic_xml_data and overview_json_data:
#     basic_country_list = fetcher.parse_basic_data(basic_xml_data)
#     overview_data = fetcher.parse_overview_data(overview_json_data)
#     complete_country_list = fetcher.merge_data(basic_country_list, overview_data)
#     fetcher.print_country_data(complete_country_list)
