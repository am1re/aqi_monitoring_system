import re
from urllib.parse import urljoin

from scrapy import Selector
from scrapy.spiders import Spider, Request


class IqairSpider(Spider):
    name = 'iqair'
    start_urls = ['https://www.iqair.com/air-pollution-data-api']

    def parse(self, response):
        root = Selector(response)

        countries_links = root.xpath('//div[@class="air-api-global-coverage-country"]//a[@class="link-secondary"]'
                                     '/@href').getall()

        for link in countries_links:
            yield Request(urljoin(response.url, link), callback=self.parse_country_page)
        # i = 0
        # for link in countries_links:
        #     i = i + 1
        #     if i > 1:
        #         break
        #     yield Request(urljoin(response.url, link), callback=self.parse_country_page)

    def parse_country_page(self, response):
        root = Selector(response)
        states_links = root.xpath("//div[@class='tags-list']//a[contains(concat(' ',normalize-space(@class),' '),"
                                  "' tags-list-item ')]/@href").getall()
        if len(states_links) > 0:
            for link in states_links:
                yield Request(urljoin(response.url, link), callback=self.parse_country_page)
        else:
            yield self.parse_page(response)

    @staticmethod
    def parse_page(response):
        root = Selector(response)
        temp = root.xpath("//span[@class='forecast-info-icon-temp']/text()").get()
        humidity = root.xpath("//div[span[@title='Humidity']]/span[@class='item-label-val']/text()").get()
        wind_speed = root.xpath("//div[span[@title='Wind']]/span[@class='item-label-val']/text()").get()
        pressure = root.xpath("//div[span[@title='Pressure']]/span[@class='item-label-val']/text()").get()
        aqi = root.xpath("//div[@class='aqi-card-info-number']/span[@class='aqi']/text()").get()
        date = root.xpath("//div[@class='page-title']//time/@datetime").get()
        country = root.xpath("//a[contains(concat(' ',normalize-space(@class),' '),' breadcrumb-item ')][1]/text()") \
            .get()
        city1 = root.xpath("//a[contains(concat(' ',normalize-space(@class),' '),' breadcrumb-item ')][2]/text()") \
            .get()
        city2 = root.xpath("//a[contains(concat(' ',normalize-space(@class),' '),' breadcrumb-item is-active ')]"
                           "/text()") \
            .get()

        if temp and humidity and wind_speed and pressure and aqi and date and country and city1 and city2:
            return {
                'temp': parse_temp(temp),
                'humidity': parse_humidity(humidity),
                'wind_speed': parse_windspeed(wind_speed),
                'pressure': parse_pressure(pressure),
                'aqi': parse_aqi(aqi),
                'country': country,
                'city1': city1,
                'city2': city2,
                'date': date,
                'origin_url': response.url
            }


def parse_temp(temp):
    return int(remove_non_numeric(temp))


def parse_humidity(humidity):
    return int(remove_non_numeric(humidity))


def parse_windspeed(windspeed):
    return round(float(remove_non_numeric(windspeed)) * 1.60934, 1)  # mph to kmh


def parse_pressure(pressure):
    return int(remove_non_numeric(pressure))  # mbar (millibar)


def parse_aqi(aqi):
    return int(remove_non_numeric(aqi))


def remove_non_numeric(line):
    return re.sub('[^0-9.]', '', line)
