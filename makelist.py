# -*- coding:utf-8 -*-
import os
import csv
import operator
import logging
from logging import getLogger, StreamHandler, Formatter

logger = getLogger("LogImeiListMaker").getChild(" - makelist")

def generate_imei_list():
    logger.info("-----ファイル出力 開始-----")
    mode = "prod"
    csv_lines_list = csv_to_list(os.getcwd(), mode)
    removed_list = remove_unuse_columns(csv_lines_list)  # 本番中端末csv由来のlist

    mode = "license"
    license_list = csv_to_list(os.getcwd(), mode)

    output_list = []
    for removed_list_elem in removed_list:
        one_imei = removed_list_elem[4]

        if not_include_imei_in_license_list(one_imei, license_list):
            output_list.append(removed_list_elem)
    create_result_csv_file(output_list)
    logger.info("-----ファイル出力 完了-----")


def not_include_imei_in_license_list(imei, lic_list):
    for license in lic_list:
        if imei in license:
            return False
    return True


def get_target_file_path(path, mode):
    if mode == "result":
        for files in os.listdir(path + "\\output"):
            if files.startswith("IMEI一覧") and files.endswith(".csv"):
                return path + "\\output\\" + files  # IMEI一覧.csv
    else:
        for files in os.listdir(path + "\\res"):
            if mode == "prod":
                if files.startswith("本番中端末") and files.endswith(".csv"):
                    return path + "\\res\\" + files  # 本番中端末（xxxx）.csv
            elif mode == "license":
                if files.startswith("license_info") and files.endswith(".csv"):
                    return path + "\\res\\" + files  # license_info.csv


def csv_to_list(cwd_path, mode):
    path = get_target_file_path(cwd_path, mode)
    logger.debug("CSVファイル読込：" + path)
    enc = 'utf-8'
    if mode == "result":
        # IMEI一覧はcp932(shift-jis)でエンコード
        enc = 'cp932'
    with open(path, "r", encoding=enc) as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # remove header
        if mode == "prod":
            # CMSから出力した一覧CSVをIMEIでソート
            result = sorted(csv_reader, key=operator.itemgetter(16))
        elif mode == "license":
            # license一覧CSVをIMEIでソート
            result = sorted(csv_reader, key=operator.itemgetter(2))
        else:
            result = sorted(csv_reader, key=operator.itemgetter(4))
        return list(result)



def remove_unuse_columns(csv_elem_list):
    # 抜き出すカラム
    # 1  : デバイス名
    # 2  : 管理番号
    # 3  : 物件名
    # 15 : 端末モデル名
    # 16 : IMEI
    # 25 : 設置完了日時
    logger.info("本番中端末.csvの不要カラムを除去")
    need_columns_idx = (1, 2, 3, 15, 16, 25)
    ret_list = []
    for idx, elem in enumerate(csv_elem_list):
        tmp_list = []
        for i, column in enumerate(elem):
            if i in need_columns_idx:
                tmp_list.append(column)
        if tmp_list[4] != '':
            ret_list.append(tmp_list)
    return ret_list


def create_result_csv_file(output_list):
    logger.info("出力ファイル作成")
    # CSV書き込み
    with open(os.path.join("output", "IMEI一覧.csv"), 'w', newline="") as csv_file:
        # header を設定
        column_names = ['デバイス名', '管理番号', '物件名', '端末モデル', 'IMEI', '設置完了日時']
        writer = csv.DictWriter(csv_file, fieldnames=column_names)
        writer.writeheader()  # header書き込み
        for i, row in enumerate(output_list):
            # カラム名をkeyにリスト内容をvalueにしたdictに変換
            row_dict = dict(zip(column_names, row))
            writer.writerow(row_dict)
