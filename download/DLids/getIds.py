#!/usr/bin/python3

from requests_oauthlib import OAuth1Session

import time, json, os, sys
from datetime import datetime

import config ## SECRET

GET_FOLLOWER_INIT_PARAMS_DIC = {
    'cursor': -1,
    'count': 5000,
    # 'screen_name': 'tasasei_psi'
    'screen_name': 'BLAZBLUE_PR'
}

class TwIds:
    GET_FOLLOWEER_URL = 'https://api.twitter.com/1.1/followers/ids.json?{}'

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

    def setCursor(self, cursor):
        self.params_dic['cursor'] = int(cursor)

    def getCursor(self):
        return self.params_dic['cursor']

    def initCursor(self):
        self.setCursor(-1)

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


    # API発行用URLにユーザー名を代入する
    def makeUrl(self) -> str:
        param_str = self.makeParams_str()
        return self.GET_FOLLOWEER_URL.format(param_str)


    # 入手したid配列をファイルに書き込み
    def writeData(self, ids_ar: list):
        # 一度setを経由して、重複を取り除く
        ids_set = set(ids_ar)
        ids_ar  = list(ids_set)

        idsStr_ar = map(str,ids_ar)
        dirPath = 'ids'
        f_name = self.params_dic['screen_name'] + '.txt'

        out_name = dirPath + '/' + f_name

        # 作成先のフォルダが存在しなければフォルダを作る
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        f = open(out_name, 'w')
        f.write('\n'.join(idsStr_ar))
        f.close()


    # URLから、ユーザーのIDを全取得
    def getFollower(self):

        print(self.params_dic['screen_name'])

        ids = []

        next_cursor = self.getCursor()
        while next_cursor != 0:
            url = self.makeUrl()
            try:
                req_result = self.session.get(url)
            except:
                # 例外が発生したら、(おそらく接続の問題なので)sleep後にcontinue
                print(sys.exc_info()[0])
                time.sleep(10)
                continue

            res = req_result.json()
            header = req_result.headers

            # データ取得に失敗したら(おそらくパラメータが間違えてるので)return
            if 'errors' in res:
                print(res['errors'])
                return

            ids += res['ids']

            next_cursor = res['next_cursor']
            self.setCursor(next_cursor)

            print('next_cursor: ' + str(next_cursor))

            if header['x-rate-limit-remaining'] == '0':
                self.sleepUntil(header)

        # 入手したIDをファイルに出力
        self.writeData(ids)


    # API利用制限が回復するまで、sleep
    def sleepUntil(self,header_arg):
        limit_reset = int( header_arg['x-rate-limit-reset'] )
        end_time = datetime.fromtimestamp(limit_reset)

        time_second = (end_time - datetime.now()).seconds + 5
        endTime_str = end_time.strftime("%Y/%m/%d %H:%M:%S")
        print('SLEEP UNTIL: ' + endTime_str)
        time.sleep(time_second)


if __name__ == '__main__':
    f = open('screen_name.txt','r')
    SN_list = f.read().split('\n')
    f.close()

    tw = TwIds(GET_FOLLOWER_INIT_PARAMS_DIC)
    for sn in SN_list:
        print()
        if sn is '':
            continue
        tw.initCursor()
        tw.setScreenName(sn)
        tw.getFollower()
