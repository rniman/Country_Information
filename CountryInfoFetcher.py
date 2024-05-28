import http.client
from xml.etree import ElementTree
from html import unescape
import re
import json


# def clean_html(raw_html):
#     # HTML 엔터티 변환
#     clean_text = unescape(raw_html)
#     # <br> 태그를 줄바꿈 문자로 변환
#     clean_text = re.sub(r'<br\s*/?>', '\n', clean_text)
#     # 나머지 HTML 태그 제거
#     clean_text = re.sub(r'<.*?>', '', clean_text)
#     # 특정 특수 문자 제거 (예: 음표)
#     clean_text = re.sub(r'[♪]', '', clean_text)
#     # 기타 비 ASCII 문자 제거 (한글 및 공백은 유지)
#     clean_text = re.sub(r'[^\x00-\x7F가-힣ㄱ-ㅎㅏ-ㅣ\s]', '', clean_text)
#     # 불필요한 공백 제거
#     clean_text = clean_text.strip()
#     return clean_text

class CountryInfoFetcher:
    def __init__(self, service_key):
        self.url = "apis.data.go.kr"
        self.service_key = service_key
        self.basic_query = f"/1262000/CountryBasicService/getCountryBasicList?serviceKey={service_key}&numOfRows=200"
        self.overview_query = f"/1262000/OverviewGnrlInfoService/getOverviewGnrlInfoList?serviceKey={service_key}&numOfRows=200"
        self.accident_query = f"/1262000/AccidentService/getAccidentList?serviceKey={service_key}&numOfRows=200"
        self.warning_query = f"/1262000/TravelWarningService/getTravelWarningList?serviceKey={service_key}&numOfRows=200"



    def load_taiwan_flag_data(self):
        with open('TaiwanImageUrl.txt', 'r') as file:
            return file.read()

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
            if country_eng_name == 'Solomon lslands':  # 오타 수정
                country_eng_name = 'Solomon Islands'
            continent = item.findtext("continent", default="N/A")
            country_id = int(item.findtext("id", default='-1'))
            country_basic = item.findtext("basic", default="N/A")
            country_basic = self.clean_html(country_basic)
            country_basic = country_basic + str("\n\n-외교부_국가별 기본정보-")
            country_img_url = item.findtext("imgUrl", default="N/A")
            if country_name == '대만':  # 대만 국기 오류 있어서 이것만 직접 수정
                country_img_url = self.load_taiwan_flag_data()
            # population, area = self.extract_additional_info(country_basic)
            country_list.append({
                "country_name": country_name,
                "country_eng_name": country_eng_name,
                "continent": continent,
                "country_id": country_id,
                "country_basic": country_basic,
                "country_img_url": country_img_url,
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

    def parse_accident_data(self, xml_data):
        tree = ElementTree.fromstring(xml_data)
        item_elements = tree.iter("item")

        accident_data = {}
        for item in item_elements:
            country_name = item.findtext("name", default="N/A")
            accident_news = item.findtext("news", default="N/A")
            accident_news = self.clean_html(accident_news)
            if country_name not in accident_data:
                accident_data[country_name] = []
            accident_data[country_name].append(accident_news)
        return accident_data

    def parse_warning_data(self, xml_data):
        tree = ElementTree.fromstring(xml_data)
        item_elements = tree.iter("item")

        warning_data = {}
        for item in item_elements:
            country_name = item.findtext("countryName", default="N/A")

            all_info = dict()
            all_info['control'] = item.findtext("control", default="N/A")
            all_info['controlPartial'] = item.findtext("controlPartial", default="N/A")
            all_info['controlNote'] = item.findtext("controlNote", default="N/A")
            all_info['attention'] = item.findtext("attention", default="N/A")
            all_info['attentionPartial'] = item.findtext("attentionPartial", default="N/A")
            all_info['attentionNote'] = item.findtext("attentionNote", default="N/A")
            all_info['limita'] = item.findtext("limita", default="N/A")
            all_info['limitaPartial'] = item.findtext("limitaPartial", default="N/A")
            all_info['limitaNote'] = item.findtext("limitaNote", default="N/A")
            all_info['imgUrl2'] = item.findtext("imgUrl2", default="N/A")

            # control = item.findtext("control", default="N/A")
            # control_partial = item.findtext("controlPartial", default="N/A")
            # control_note = item.findtext("controlNote", default="N/A")
            #
            # attention = item.findtext("attention", default="N/A")
            # attention_partial = item.findtext("attentionPartial", default="N/A")
            # attention_note = item.findtext("attentionNote", default="N/A")
            #
            # limita = item.findtext("limita", default="N/A")
            # limita_partial = item.findtext("limitaPartial", default="N/A")
            # limita_note = item.findtext("limitaNote", default="N/A")

            if country_name not in warning_data:
                warning_data[country_name] = dict()

            for key, value in all_info.items():
                if value == 'N/A':
                    continue
                warning_data[country_name][key] = value


        return warning_data

    def clean_html(self, raw_html):
        clean_text = unescape(raw_html)  # Convert HTML entities
        clean_text = re.sub('<br\s*/?>', '', clean_text)  # Convert <br> to new lines
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

    def merge_supplement_data(self, basic_data, overview_data):
        # 국가 이름 매핑 딕셔너리
        country_name_mapping = {
            '가이아나공화국': '가이아나',
            '네팔': '네팔연방',
            '마이크로네시아': '마이크로네시아연방',
            '미국': '미합중국',
            '베네수엘라': '베네수엘라볼리바르',
            '중앙아프리카공화국': '중앙아프리카',
            '키르기스스탄': '키르기즈공화국',
            '튀르키예': '튀르키예공화국'
        }

        # N/A 값 보충하기
        for country in basic_data:
            name = country["country_name"]
            mapped_name = country_name_mapping.get(name, name)  # 매핑된 이름 가져오기, 기본값은 원래 이름
            if mapped_name in overview_data:
                country["population"] = overview_data[mapped_name].get("population", "N/A")
                country["area"] = overview_data[mapped_name].get("area", "N/A")
            elif name == '마카오':
                country["population"], country["area"] = self.extract_additional_info(country['country_basic'])
                country["population"] = 695200
            elif name == '홍콩':
                country["population"], country["area"] = self.extract_additional_info(country['country_basic'])
                country["population"] = 7346000
            elif '교황청' in overview_data:
                pass
            # if name in overview_data:
            #     country["population"] = overview_data[name].get("population", "N/A")
            #     country["area"] = overview_data[name].get("area", "N/A")
            # elif name == '가이아나공화국' and '가이아나' in overview_data:
            #     country["population"] = overview_data['가이아나'].get("population", "N/A")
            #     country["area"] = overview_data['가이아나'].get("area", "N/A")
            # elif name == '네팔' and '네팔연방' in overview_data:
            #     country["population"] = overview_data['네팔연방'].get("population", "N/A")
            #     country["area"] = overview_data['네팔연방'].get("area", "N/A")
            # elif name == '마이크로네시아' and '마이크로네시아연방' in overview_data:
            #     country["population"] = overview_data['마이크로네시아연방'].get("population", "N/A")
            #     country["area"] = overview_data['마이크로네시아연방'].get("area", "N/A")
            # elif name == '미국' and '미합중국' in overview_data:
            #     country["population"] = overview_data['미합중국'].get("population", "N/A")
            #     country["area"] = overview_data['미합중국'].get("area", "N/A")
            # elif name == '베네수엘라' and '베네수엘라볼리바르' in overview_data:
            #     country["population"] = overview_data['베네수엘라볼리바르'].get("population", "N/A")
            #     country["area"] = overview_data['베네수엘라볼리바르'].get("area", "N/A")
            # elif name == '중앙아프리카공화국' and '중앙아프리카' in overview_data:
            #     country["population"] = overview_data['중앙아프리카'].get("population", "N/A")
            #     country["area"] = overview_data['중앙아프리카'].get("area", "N/A")
            # elif name == '키르기스스탄' and '키르기즈공화국' in overview_data:
            #     country["population"] = overview_data['키르기즈공화국'].get("population", "N/A")
            #     country["area"] = overview_data['키르기즈공화국'].get("area", "N/A")
            # elif name == '튀르키예' and '튀르키예공화국' in overview_data:
            #     country["population"] = overview_data['튀르키예공화국'].get("population", "N/A")
            #     country["area"] = overview_data['튀르키예공화국'].get("area", "N/A")
            # elif name == '마카오':
            #     country["population"], country["area"] = self.extract_additional_info(country['country_basic'])
            #     country["population"] = 695200
            # elif name == '홍콩':
            #     country["population"], country["area"] = self.extract_additional_info(country['country_basic'])
            #     country["population"] = 7346000
            # elif '교황청' in overview_data:
            #     pass
        return basic_data

    def merge_accident_data(self, basic_data, accident_data):
        for country in basic_data:
            name = country["country_name"]
            if name in accident_data:
                country["accident_info"] = "[외교부 사고 정보(2/3)]\n\n" + "".join(accident_data[name])
            else:
                country["accident_info"] = "[외교부 사고 정보(2/3)]\n\n정보 없음"

            country["accident_info"] += str("\n\n-외교부_사건사고 현황-")
        return basic_data

    def merge_warning_data(self, basic_data, warning_data):
        warning_name_mapping = {
            'control': '여행 경보',
            'controlPartial': '여행 경보',
            'controlNote': '여행 경보 내용',
            'attention': '여행 경보',
            'attentionPartial': '여행 경보',
            'attentionNote': '여행 경보 내용',
            'limita': '여행 경보',
            'limitaPartial': '여행 경보',
            'limitaNote': '여행 경보 내용',
            'imgUrl2': '여행위험지도 경로'
        }
        for country in basic_data:
            name = country["country_name"]
            if name in warning_data:
                country["warning_info"] = "[외교부 여행 경보(3/3)]\n\n"
                for key, value in warning_data[name].items():
                    country["warning_info"] += str("{0}: {1}\n".format(warning_name_mapping[key], value))
            else:
                country["warning_info"] = "[외교부 여행 경보(3/3)]\n\n정보 없음"

            country["warning_info"] += str("\n\n-외교부_여행경보제도-")
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
            print(f"면적: {country['area']} km^2\n")
            # print(f"국가 기본정보: {country['country_basic']}\n\n")
            # print(f"국가 사건사고: {country['accident_info']}\n\n")
            print(f"국가 여행경보: {country['warning_info']}\n\n")


# 클래스 사용 예제
if __name__ == "__main__":
    service_key = "TM2mB7BkLj7%2B1mK%2FbNgWbxjMPtdffuyVQbT46zhjwGtnC%2FEA6FQwymPyHVNcFFdJN%2FaQuqSYutGF33dW20COZg%3D%3D"
    fetcher = CountryInfoFetcher(service_key)

    basic_xml_data = fetcher.fetch_country_data(fetcher.basic_query)
    overview_json_data = fetcher.fetch_country_data(fetcher.overview_query)
    accident_xml_data = fetcher.fetch_country_data(fetcher.accident_query)
    warning_xml_data = fetcher.fetch_country_data(fetcher.warning_query)

    if basic_xml_data and overview_json_data:
        basic_country_list = fetcher.parse_basic_data(basic_xml_data)
        overview_data_list = fetcher.parse_overview_data(overview_json_data)
        accident_data_list = fetcher.parse_accident_data(accident_xml_data)
        warning_data_list = fetcher.parse_warning_data(warning_xml_data)

        complete_country_list = fetcher.merge_supplement_data(basic_country_list, overview_data_list)
        complete_country_list = fetcher.merge_accident_data(complete_country_list, accident_data_list)
        complete_country_list = fetcher.merge_warning_data(complete_country_list, warning_data_list)

        fetcher.print_country_data(complete_country_list)
