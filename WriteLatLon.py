# pip install opencage
import os
from opencage.geocoder import OpenCageGeocode
import csv

output_file = 'country_lat_lon.csv'

# OpenCage API 키
class NationLatLon:
    opencage_api_key = "a621178fb7114289bd76e77012864fa5"
    geocoder = OpenCageGeocode(opencage_api_key)

    def __init__(self):
        self.lat_lon_list = dict()
        self.output_file = output_file

    def initialize_csv(self):
        if not os.path.exists(self.output_file):
            with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['country_eng_name', 'latitude', 'longitude'])

    def get_country_lat_lon(self, country_name):
        results = NationLatLon.geocoder.geocode(country_name)
        if results:
            return results[0]['geometry']['lat'], results[0]['geometry']['lng']
        else:
            return None

    def add_country_lat_lon(self, country_list):
        for index, country in enumerate(country_list):
            country_name = country['country_eng_name']
            lat_lon = self.get_country_lat_lon(country_name)
            if lat_lon:
                self.lat_lon_list[country_name] = lat_lon
                self.append_to_csv(country_name, lat_lon)
                print(index, country_name, lat_lon)
            elif country_name == 'CapeVerde':  # 이것만 이름 조금 다름
                country_name = 'Cape Verde'
                lat_lon = self.get_country_lat_lon(country_name)
                self.lat_lon_list[country_name] = lat_lon
                self.append_to_csv(country_name, lat_lon)
                print(index, country_name, lat_lon)
            else:
                print("Can't Find", index, country_name)
        print('csv out End')
        return True

    def append_to_csv(self, country_name, lat_lon):
        with open(self.output_file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([country_name, lat_lon[0], lat_lon[1]])

    def load_lat_lon_from_csv(self):
        try:
            with open(self.output_file, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    country_name = row['country_eng_name']
                    latitude = float(row['latitude'])
                    longitude = float(row['longitude'])
                    self.lat_lon_list[country_name] = (latitude, longitude)
        except FileNotFoundError:
            print(f"{self.output_file} 파일을 찾을 수 없습니다.")

    def print_country_lat_lon(self, country):
        country_name = country['country_eng_name']
        if self.lat_lon_list[country_name]:
            print(f"{country_name}의 위도: {self.lat_lon_list[country_name][0]}, "
                  f"경도: {self.lat_lon_list[country_name][1]}")
        else:
            print(f"{country_name}의 정보를 찾을 수 없습니다.")

    def print_all_country_lat_lon(self):
        index = 0
        for eng_name, lat_lon in self.lat_lon_list.items():
            print("{0} {1}: ({2}, {3})".format(index, eng_name, lat_lon[0], lat_lon[1]))
            index += 1
