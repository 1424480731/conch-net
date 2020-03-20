from pymongo import MongoClient

import urllib.parse as parse
import base64
import time,random
settings = {
    "ip":'127.0.0.1',
    "port":27017,
}

class MongoBase(object):

    def __init__(self):

        try:
            self.conn = MongoClient(settings["ip"], settings["port"])
        except Exception as e:
            raise e

    def get_table(self,dbname,setname):

        dbconn = None
        table_conn = None

        try:
            dbconn = self.conn[dbname]
            table_conn = dbconn[setname]
        except:
            print('connect exception!!!')
        return table_conn

    def insert(self,dbname,setname,dic):
        
        table_conn = self.get_table(dbname,setname)
        table_conn.insert(dic)

    def update(self, dbname,setname,dic, newdic):
        table_conn = self.get_table(dbname, setname)
        table_conn.update(dic, newdic)

    def delete(self, dbname,setname,dic):
        table_conn = self.get_table(dbname, setname)
        status = table_conn.remove(dic)
        return status
    def dbFind(self, dbname,setname,dic):
        table_conn = self.get_table(dbname, setname)
        data = table_conn.find(dic)
        data = list(data)
        return data

    def findAll(self,dbname,setname,):

        table_conn = self.get_table(dbname, setname)
        for i in table_conn.find():
            print(i)

class  MongoChengJiApi(MongoBase):

    def __init__(self):
        self.dbname = 'zf'
        self.setname = 'cjzf'
        super().__init__()

    @staticmethod
    def chose_complete_msg(data,precision=1,type='全国'):

        ret_html = []
        html_tmp = []
        html_box = data.get('html_box')
        for html in html_box:

            msg = html.get('data')
            if msg:
                decoration_situation = msg.get('decoration_situation')
                source = msg.get('source')
                area = msg.get('area')
                housing_estate = msg.get('housing_estate')
                view_box = msg.get('view_box')
                phone = msg.get('phone')
                img_box = msg.get('img_box')
                header_link = msg.get('header_link')
                name = msg.get('name')
                storey = msg.get('storey')
                address = msg.get('address')
                price = msg.get('price')
                layout = msg.get('layout')
                deposit = msg.get('deposit')
                orientation = msg.get('orientation')
                title = msg.get('title')
                pubdate = msg.get('pubdate')
                img_url = msg.get('img_url')
                msg_list = [
                    decoration_situation,source,area,housing_estate,price,\
                    view_box,phone,img_box,header_link,name,storey,address,\
                    layout,deposit,orientation,title,pubdate,img_url
                ]
                if msg_list.count(None)<=precision:
                    html_tmp.append(html)
        if type=='全国':
            if len(html_tmp)>14:
                for i in range(20):
                    index = random.randint(0,len(html_tmp))
                    ret_html.append(html_tmp[index])
            return ret_html
        else:
            return html_tmp
    @staticmethod
    def choose_fy_by_price(datas,cond):
        start_price = int(cond.get('start_price'))
        end_price = int(cond.get('end_price'))
        ret_html=[]
        for data in datas:

            if data.get('data').get('price') and '面' not in data.get('data').get('price'):
                price = int(data.get('data').get('price')[:-1])
                if price>=start_price and price<=end_price:
                    ret_html.append(data)
        return ret_html

    @staticmethod
    def choose_fy_by_id(cond,datas):
        id = cond.get('id')
        for data in datas:
            if data.get('id')==id:
                return data
    @staticmethod
    def choose_fy_by_id_for_all(cond,datas):

        id = cond.get('id')
        html_box = datas.get('html_box')
        for html in html_box:
            if html.get('id') == id:
                return html

    def get_location(self,cond):

        area = cond.get('cond')
        table_conn = self.get_table(self.dbname, self.setname)
        pipeline = [
            {'$match': {'area': area}},
            {'$unwind': '$district_box'},
            {'$project': {'district_box.road_box.road': 1, 'district_box.district': 1,'_id':0}}
        ]
        ret = list(table_conn.aggregate(pipeline))
        return ret

    def get_html_box_from_data(self,type,datas):

        ret_box = {}
        html_box =[]
        for data in datas:
            district_box = data.get('district_box')
            if isinstance(district_box,dict):
                district_box = [district_box]
            for district in district_box:
                road_box = district.get('road_box')
                if road_box:
                    if isinstance(road_box, dict):
                        road_box = [road_box]
                    for road in road_box:
                        html_box.extend(road.get('html_box'))
        ret_box.update(type)
        ret_box.update({'html_box':html_box})
        return ret_box

    def get_fy_from_all(self,cond):

        table_conn = self.get_table(self.dbname, self.setname)
        ret = list(table_conn.find({}))
        ret_format =self.get_html_box_from_data(cond,ret)
        return ret_format
    def get_fy_by_city(self,cond):

        city = cond.get('cond')
        table_conn = self.get_table(self.dbname,self.setname)
        ret = list(table_conn.find({'area':city}))
        ret_format =self.get_html_box_from_data(cond,ret)
        return ret_format

    def get_fy_by_district(self,cond):

        district = cond.get('cond')
        table_conn = self.get_table(self.dbname, self.setname)
        ret = list(table_conn.find({'district_box.district':district},{'district_box.$.roadbox':1}))
        ret_format = self.get_html_box_from_data(cond, ret)
        return ret_format

    def get_fy_by_road(self,cond):

        road = cond.get('cond')
        table_conn = self.get_table(self.dbname, self.setname)
        pipeline = [
                        {'$match':{'district_box.road_box.road':road}},
                        {'$unwind':'$district_box'},
                        {'$unwind':'$district_box.road_box'},
                        {'$match':{'district_box.road_box.road':road}},
                    ]
        ret = list(table_conn.aggregate(pipeline))
        ret_format = self.get_html_box_from_data(cond, ret)
        return ret_format


    def upToDateRent(self,cond):

        ret_list = self.get_fy_from_all(cond)
        html_box=self.chose_complete_msg(ret_list)
        return html_box


    def get_city_list(self,cond):
        ret_list = self.get_fy_by_city(cond)
        html_box=self.chose_complete_msg(ret_list,precision=14,type=None)
        return html_box

    def get_district_list(self,cond):
        ret_list = self.get_fy_by_district(cond)
        html_box=self.chose_complete_msg(ret_list,precision=14,type=None)
        return html_box

    def get_road_list(self,cond):
        ret_list = self.get_fy_by_road(cond)
        html_box=self.chose_complete_msg(ret_list,precision=14,type=None)
        return html_box

    def get_fy_by_cond(self,cond):

        cond_content = cond.get('cond')
        html_box = []
        if cond_content=='全国':
            html_box=self.upToDateRent(cond)
        if not html_box:
            html_box=self.get_city_list(cond)

        if not html_box:
            html_box=self.get_district_list(cond)

        if not html_box:
            html_box=self.get_road_list(cond)
        return html_box

    def get_road_list_by_price(self,cond):

        html_box_t = self.get_road_list(cond)
        html_box=self.choose_fy_by_price(html_box_t,cond)
        return html_box

    def find_fy_by_id(self, cond):

        location = cond.get('cond')
        fy={}
        if location=="全国":
            ret_list = self.get_fy_from_all(cond)
            fy = self.choose_fy_by_id_for_all(cond,ret_list)
        else:
            html_box=self.get_fy_by_cond(cond)
            fy = self.choose_fy_by_id(cond,html_box)
        return fy


if __name__ == '__main__':

   ml = MongoBase()
   ml = MongoChengJiApi()
   dbname = 'zf'
   setname = 'cjzf'
   # print(ml.base_all())
   # print(ml.get_detail_msg_by_area({'area':'北京'}))
   # ml.get_area_district()
   # ml.get_fymsg_by_area_district({'area':'阿里','district':'噶尔县'})
   # ml.get_fymsg_by_area_district({'area':'阿勒泰','district':'阿勒泰市'})
   # print(ml.get_fy_by_city({'city':'阿勒泰'}))
   # print(ml.get_fy_by_district({'district':'阿勒泰市'}))
   # print(ml.get_fy_by_road({'road':'光山县'}))
   # print(ml.get_fy_from_all())
   # for i in ml.upToDateRent({'cond':'全国'}):
   #     print(i)
   #     input()

   # print(ml.get_fy_by_cond({'cond':'阿勒泰'}))
   # print(ml.get_location({'cond':'阿勒泰'}))
   # print(ml.get_road_list_by_price({'cond':'阿勒泰市','start_price':50,'end_price':6000}))
   print(ml.find_fy_by_id({'cond':'阿勒泰市','id':'c8eb0012ff9b4afc'}))