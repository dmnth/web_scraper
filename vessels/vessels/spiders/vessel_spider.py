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
            msi = msi_pattern.search(link)
            result = {
                    'name': vessel_name,
                    'type': vessel_type,
                    'year built': year_built,
                    'size': size,
                    'imo': imo.group(),
                    'msi': msi.group(),
                    }
            yield result 

        next_page = response.css('nav a.pagination-next::attr(href)').get() 
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
