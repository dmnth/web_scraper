#! /usr/bin/env python3

import scrapy
import re

class VesselSpider(scrapy.Spider):

    name = 'vessels'
    start_urls = ['https://www.vesselfinder.com/vessels']

    def parse(self, response):
        vessels = response.css('tbody')
        for vessel in vessels.css('tr'):
            vessel_name = vessel.css('div.slna::text').get()
            vessel_type = vessel.css('div.slty::text').get()
            year_built = vessel.css('td.v3::text').get()
            size = vessel.css('td.v6::text').get()
            link = vessel.css('tr td.v2 a.ship-link::attr(href)').get()
            imo_pattern = re.compile('(?<=IMO-)[0-9]+')
            msi_pattern = re.compile('(?<=MSI-)[0-9]+')
            imo = imo_pattern.search(link)
            msi = imo_pattern.search(link)
            '''
            vessel_link = response.urljoin(link)
            if vessel_link is not None:
                yield response.follow(vessel_link, callback=self.parse_imo)
            '''
            result = {
                    'name': vessel_name,
                    'type': vessel_type,
                    'year built': year_built,
                    'size': size,
                    'imo': imo.group(),
                    'msi': msi.group(),
                    }
            yield result 

    def parse_imo(self, response):
        def extract_imo(query):
            result = response.css(query).get().split('/')[0].rstrip()
            if result:
                return result

        yield {
                'imo': extract_imo('td.v3.v3np::text'),
                }
