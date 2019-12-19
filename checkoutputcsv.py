# -*- coding:utf-8 -*-

import os
import makelist
import logging
from logging import getLogger, StreamHandler, Formatter

logger = getLogger("LogImeiListMaker").getChild(" - checkoutputcsv")

def is_correct_resultcsv():
    logger.info("-----チェック 開始-----")
    # IMEI一覧.csv
    result_list = makelist.csv_to_list(os.getcwd(), "result")
    result_imeis = extract_imei(result_list, "result")

    # 本番中端末（xxxx）.csv
    prod_list = makelist.csv_to_list(os.getcwd(), "prod")
    prod_imeis = extract_imei(prod_list, "prod")

    # license_info.csv
    license_list = makelist.csv_to_list(os.getcwd(), "license")
    license_imeis = extract_imei(license_list, "license")

    # IMEI一覧のIMEIがlicenseに含まれていないことをチェック
    if is_imei_inculeded(result_imeis, license_imeis):
        logger.info("NG IMEI一覧のIMEIがlicense_info.csvに含まれています")
        logger.info("1回前のNECからのライセンスファイル上に同一IMEIが重複しています（被っていない）")
    else:
        logger.info("OK IMEI一覧のIMEIがlicense_info.csvに含まれていません")

    # licenseのIMEIがIMEI一覧に含まれていないことをチェック
    if is_imei_inculeded(license_imeis, result_imeis):
        logger.info("NG license_info.csvのIMEIはIMEI一覧.csvに含まれています")
        logger.info("1回前のNECからのライセンスファイル上に同一IMEIがない（被っていない）事を確認")
    else:
        logger.info("OK license_info.csvのIMEIはIMEI一覧.csvに含まれていせん")

    # 本番中端末のIMEIの内、IMEI一覧に含まれてるものがlicenseに含まれていないことをチェック
    if total_check_imei(prod_imeis, result_imeis, license_imeis):
        logger.info("本番中端末.csvのIMEIのうち、IMEI一覧に含まれているものはlicense_infoに含まれています")
        logger.info("※1回前のNECからのライセンスファイル上に同一IMEIがない（被っていない）事を確認")
    else:
        logger.info("OK 本番中端末.csvのIMEIのうち、IMEI一覧に含まれているものはlicense_infoに含まれていせん ")
    logger.info("-----チェック終了-----")

def extract_imei(list, mode):
    ret_list = []
    # imei_index = 999
    logger.info("csvの内容からIMEIのみを抽出")
    # 各csvのIMEI絡むのインデックス
    if mode == "result":
        imei_index = 4
    elif mode == "license":
        imei_index = 2
    else:
        imei_index = 16
    for i, row in enumerate(list):
        ret_list.append(row[imei_index])
    return ret_list


def is_imei_inculeded(fromlist, tolist):
    for i, imei in enumerate(fromlist):
        if imei in tolist:
            return True
    return False

def total_check_imei(fromlist, tolist1, tolist2):
    for i, imei in enumerate(fromlist):
        if imei in tolist1:
            if imei in tolist2:
                return True
    return False
