# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouPositionItem(scrapy.Item):
    # define the fields for your item here like:
    company_short = scrapy.Field()
    company = scrapy.Field()            # company name
    company_id = scrapy.Field()
    company_size = scrapy.Field()       # 公司规模
    education = scrapy.Field()          # 学历要求
    finance_stage = scrapy.Field()
    industry = scrapy.Field()           # 行业
    position_type = scrapy.Field()      # 职位类型
    position_name = scrapy.Field()
    position_id = scrapy.Field()        # 职位id
    advantage = scrapy.Field()          # 职位诱惑
    salary = scrapy.Field()
    work_year = scrapy.Field()          # 工作年限


class LagouJobDescItem(scrapy.Item):
    # define the fields for your item here like:
    dept = scrapy.Field()
    job_desc = scrapy.Field()           # 职位描述
    # work = scrapy.Field()               # 工作职责
    # requirement = scrapy.Field()        # 任职要求
