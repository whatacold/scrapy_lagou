# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_lagou.items import LagouPositionItem, LagouJobDescItem

class LagouSpider(scrapy.Spider):
    name = "lagou"
    allowed_domains = ["lagou.com"]
    #start_urls = [
    #        "http://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3"
    #        ]
    npages = 20 # 页数
    pn = 1      # page no.

    def start_requests(self):
        return [
                scrapy.FormRequest("http://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3",
                    formdata = {'kd' : 'C', 'first' : 'false', 'pn' : str(self.pn)},
                    callback = self.parse
                    ),
                ]

    def parse(self, resp):
        js = json.loads(resp.body_as_unicode())
        if not js['success']:
            print 'failed to get json'
        else:
            for i in range(js['content']['pageSize']):
                json_item = js['content']['result'][i]
                position = LagouPositionItem()
                position['company_short'] = json_item['companyName']
                position['company'] = json_item['companyShortName']
                position['company_id'] = json_item['companyId']
                position['company_size'] = json_item['companySize']
                position['education'] = json_item['education']
                position['finance_stage'] = json_item['financeStage']
                position['industry'] = json_item['industryField']
                position['position_type'] = json_item['positionType']
                position['position_name'] = json_item['positionName']
                position['position_id'] = json_item['positionId']
                position['advantage'] = json_item['positionAdvantage']
                position['salary'] = json_item['salary']
                position['work_year'] = json_item['workYear']
                yield position

                yield scrapy.Request('http://www.lagou.com/jobs/' + str(json_item['positionId']) + '.html',
                        callback = self.parse_job_desc
                        )

        # FIXME avoid duplicate
        self.pn = self.pn + 1
        if self.pn > 2:
            return
        yield scrapy.FormRequest("http://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3",
                    formdata = {'kd' : 'C', 'first' : 'false', 'pn' : str(self.pn)},
                    callback = self.parse
                    )


    # 解析职位信息json
    def parse_job_position(self, resp):
        pass

    # 解析职位描述html页面
    def parse_job_desc(self, resp):
        jd = LagouJobDescItem()
        jd['dept'] = resp.xpath('//*[@id="container"]/div[1]/dl[1]/dt/h1/div/text()')
        jd['job_desc'] = resp.xpath('//*[@id="container"]/div[1]/dl[1]/dd[2]')
        # jd.['work'] = resp.xpath()
        # jd.['requirement'] = resp.xpath()
        yield jd
