import scrapy


class GdpDebtSpider(scrapy.Spider):
    name = "gdp_debt"
    allowed_domains = ["worldpopulationreview.com"]
    start_urls = ["https://worldpopulationreview.com/country-rankings/countries-by-national-debt"]

    def parse(self, response):
        table = response.xpath("(//tbody)[3]")
        rows = table.xpath(".//tr")
        for row in rows:
            name = row.xpath(".//th/a/text()").get()
            gdp_debt = row.xpath(".//td[1]/text()").get()
            yield {
                'country_name': name,
                'gdp_debt': gdp_debt
            }
            # logging.info(response.url)
