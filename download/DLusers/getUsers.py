#!/usr/bin/python3

from requests_oauthlib import OAuth1Session

import time, json, os, sys
from datetime import datetime

import config ## SECRET

INIT_PARAMS_DIC = {
    'screen_name': 'BLAZBLUE_PR'
}

class TwUsers:
    URL_TEMPLATE = 'https://api.twitter.com/1.1/users/show.json?{}'

    def __init__(self,params_dic: dict):
        self.setParams(params_dic)
        self.setSession()

    def setSession(self):
        session = OAuth1Session(
            config.CONSUMER_KEY,
            client_secret=config.CONSUMER_SECRET,
            resource_owner_key=config.ACCESS_TOKEN,
            resource_owner_secret=config.ACCESS_TOKEN_SECRET)
        self.session = session

    def setParams(self, param: dict):
        self.params_dic = param

    def setScreenName(self, screen_name: str):
        self.params_dic['screen_name'] = screen_name


    # API URL内のパラメータを生成
    # 例) 'screen_name=sampleName&cursor=-1&count=5000'
    def makeParams_str(self) -> str:
        param_list = []
        for key in self.params_dic:
            oneParam_str = '='.join([str(key),str(self.params_dic[key])])
            param_list += [oneParam_str]
        param_str = '&'.join(param_list)
        return param_str


    # API発行用URLにパラメータを代入する
    def makeUrl(self) -> str:
        param_str = self.makeParams_str()
        return self.URL_TEMPLATE.format(param_str)


    # URLから、ユーザーのIDを全取得
    def getUser(self):

        print(self.params_dic['screen_name'])

        url = self.makeUrl()

        while True:
            try:
                req_result = self.session.get(url)
            except:
                # 例外が発生したら、(おそらく接続の問題なので)sleep後にcontinue
                print(sys.exc_info()[0])
                time.sleep(10)
                continue
            break
        res = req_result.json()

        return res


    # API利用制限が回復するまで、sleep
    def sleepUntil(self,header_arg):
        limit_reset = int( header_arg['x-rate-limit-reset'] )
        end_time = datetime.fromtimestamp(limit_reset)

        time_second = (end_time - datetime.now()).seconds + 5
        endTime_str = end_time.strftime("%Y/%m/%d %H:%M:%S")
        print('SLEEP UNTIL: ' + endTime_str)
        time.sleep(time_second)

# データ読み込み
def read_singleData(f_name):
    f = open(f_name)
    d_list = f.read().split('\n')
    f.close()
    # 空行があれば除去
    while '' in d_list:
        d_list.remove('')
    return d_list

if __name__ == '__main__':
    SN_list  = read_singleData('screen_name.txt')
    key_list = read_singleData('key_list.txt')

    # twitterへの接続オブジェクト生成
    tw = TwUsers(INIT_PARAMS_DIC)

    # ユーザー情報格納用配列
    users_list = []

    # それぞれのscreen_nameのユーザー情報を取得する
    for sn in SN_list:
        tw.setScreenName(sn)
        res = tw.getUser()

        if 'errors' in res:
            continue

        res_list = []

        for k in key_list:
            res_list += [str(res[k])]

        users_list += [res_list]
    
    f = open('users.csv','w')
    sep = ','

    f.write( sep.join(key_list) )
    f.write('\n')

    for u in users_list:
        f.write( sep.join(u) )
        f.write('\n')
