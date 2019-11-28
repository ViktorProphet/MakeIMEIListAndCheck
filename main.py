# -*- coding:utf-8 -*-

import os
import makelist
import datetime
import shutil
import checkoutputcsv
import logging
from logging import getLogger, StreamHandler, FileHandler, Formatter


def get_prod_csvfilename():
    cwd = os.getcwd()
    path = os.path.join(cwd, 'res')
    dir_list = os.listdir(path)
    for name in dir_list:
        if name.startswith("本番中端末") and name.endswith(".csv"):
            return name
    return ""


if __name__ == "__main__":
    # loggerの設定
    logger = getLogger("LogImeiListMaker")
    # logレベルの設定
    logger.setLevel(logging.DEBUG)
    # logger handlerの設定
    stream_handler = StreamHandler()
    # handlerのログレベル設定
    stream_handler.setLevel(logging.INFO)
    # ログフォーマット設定
    handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(handler_format)
    # filehandlerの生成
    file_handler = FileHandler('log\\imeilist.log', 'a')
    # loggerにhandlerをセット
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)


    logger.info("==========logic start==========")

    # csvつくるやつ
    makelist.generate_imei_list()

    # 確認するやつ
    checkoutputcsv.is_correct_resultcsv()

    # 結果ファイルをGoogle Driveに必要ファイルをディレクトリを切って配置する
    # TODO: G SuiteアカウントにGoogle API Managerの閲覧・作成権限な無いため実装不可でした。。。

    # NEC送信用のzipファイルを作成する。
    if not os.path.isdir(os.getcwd() + '\\output\\IMEI一覧'):
        os.mkdir('output\\' + 'IMEI一覧')
    # 必要ファイルをコピー
    shutil.copy('.\\output\\IMEI一覧.csv', '.\\output\\IMEI一覧\\IMEI一覧.csv')
    # フォルダをzip
    shutil.make_archive('.\\output\\IMEI一覧', 'zip', root_dir='.\\output\\')


    # Gdriveに配置用のディレクトリ作成
    date_str = datetime.datetime.today().strftime('%Y%m%d')
    if not os.path.isdir('output\\' + date_str):
        os.mkdir('output\\' + date_str)
    # 必要ファイルをコピー
    shutil.copy('.\\output\\IMEI一覧.csv', '.\\output\\' + date_str + '\\IMEI一覧_' + date_str + '.csv')
    shutil.copy('.\\res\\license_info.csv', '.\\output\\' + date_str + '\\license_info_' + date_str + '.csv')
    prod_file_name = get_prod_csvfilename()
    shutil.copy('.\\res\\' + prod_file_name, '.\\output\\' + date_str + '\\' + prod_file_name[0:-4] + '_' + date_str + '.csv')

    logger.info("==========logic end==========")



