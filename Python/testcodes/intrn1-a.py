import sys
import os

import pickle
import pandas as pd

import csv
import math
from _collections import OrderedDict

EXEDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(EXEDIR, "..", ".."))

# 定義
PRJ_ROOT_DIR = "C:/pleiades/workspace_nouritsu/web_apps"

GROUND_TRUTH_FILENAME = "選定キーワードリスト-dev001-200_20180820_1327.xlsx"
GROUND_TRUTH_SHEETNAME = "Sheet1"

PKL_FILE_LIMIT = 200
UNMATCHED_DEV_NUM = [
    5,  9, 12, 18, 24, 25, 27, 31, 32, 33,
 34, 37, 38, 39, 40, 41, 42, 43, 44, 46,
 47, 48, 49, 50, 51, 52, 53, 54, 57, 58,
 59, 62, 63, 64, 66, 67, 70, 71, 73, 74,
 76, 77, 86, 87, 89, 90, 93, 95, 96,100,
102,103,104,105,111,116,118,119,131,133,
134,135,136,139,140,141,143,144,145,146,
147,151,152,153,155,162,163,164,165,166,
167,168,173,175,176,178,179,180,181,186,
187,188,191,194,195,198,199
]
#一つのUNMATCHEDページに対して抜き出す単語の数
EXTRACT_WORD_NUM = 10
PKL_FILE_DIR = "D:/F-souya_intern/data/pdfs-texts-layout-per-file_pickle"
MY_DATA_FILE_PATH = r"D:/F-souya_intern"
from lib.nlp.pdf_term_extractor import PdfTermExtractor


class ScoreDecision():
    def run(self):
        # parser = argparse.ArgumentParser()
        # parser.add_argument('input_dir',  type=str, help='テキストを含むルートディレクトリパス')
        # parser.add_argument('output_dir', type=str, help='データ出力先とするルートディレクトリパス')
        # parser.add_argument('--df',       type=str, help='DFピックルファイル(.pkl)のパス(TF-IDFを計算する場合は必要)')
        # parser.add_argument('--limit',    type=int, default=0, help='処理するファイル数の制限。default=0(制限なし)')
        # args = parser.parse_args()

        #------------------------------------------------
        # マスタファイルのパスを指定して抽出器を作成する
        #------------------------------------------------
        masterdir = os.path.join(PRJ_ROOT_DIR, "master")
        master_info = {
            "world"          : os.path.join(masterdir, "WorldMaster.xlsx"),
            "region"         : os.path.join(masterdir, "RegionMaster.xlsx"),
            "country"        : os.path.join(masterdir, "CountryMaster.xlsx"),
            "country-region" : os.path.join(masterdir, "CountryRegionMaster.xlsx"),
            "city"           : os.path.join(masterdir, "CityMaster.xlsx"),
        }
        extractor = PdfTermExtractor(master_info, os.path.join(masterdir, "terms-df.pkl"))

        # シートを pandas DataFrame 形式で取得する
        xl_path = os.path.join(masterdir, GROUND_TRUTH_FILENAME)
        xl_book = pd.ExcelFile(xl_path)
        xl_sheet_df = xl_book.parse(sheetname=GROUND_TRUTH_SHEETNAME, header=None)

        #スコアflr-uniqでマッチしなかったページについて、flr-uniqのソートで上位5ワードを格納する
        #term_score_lists = 
        #{ 'dev_num' : [ {'term' : term, 'score_name' : score, ... } , { } , ...] , ' ' : [ ] , ...}
        term_score_lists = {}
        
        # １行毎に処理する
        files_count = 0
        #ページ番号, 評価項目1~7のマッチ , 世界/地域/国のマッチ が格納されているdict、
        #value のリストにはdev_numに対応した結果が格納される
        #>>ファイル単位のループ
        for index, row in xl_sheet_df.iterrows():

            if PKL_FILE_LIMIT <= files_count:
                print("リミット終了 files_count=", files_count)
                break
            #----------------
            # 正解情報の取得
            #----------------
            fileno = row[0]
            if math.isnan(fileno) or fileno == 0.0:
                continue
            #ファイルナンバーがflr-uniqのマッチしていないページでないとき、目的のページでないためループを飛ばす
            if not int(fileno) in UNMATCHED_DEV_NUM:
                print("目的のページでない")
                continue

            filename = "dev{:03}.pkl".format(int(fileno))
            keyword = row[1]
            if keyword:
                result_keywords = keyword.split("\n")
            else:
                result_keywords = keyword

            result_world   = row[2] if isinstance(row[2], str) else ""
            result_region  = row[5] if isinstance(row[5], str) else ""
            result_country = row[8] if isinstance(row[8], str) else ""

            print(index, filename, result_keywords, result_world, result_region, result_country)

            #----------------
            # 対応する pkl ファイルを解析してキーワードを取得する
            #----------------
            with open(os.path.join(PKL_FILE_DIR, filename), "rb") as fr:
                tl_text = pickle.load(fr)

                # 単語集出
                #terms = {'word' : {'score' : {'basic' : {'項目' : 値 } , {'項目' : 値 } , ... }}}
                terms = extractor.get_terms(tl_text)

                #単語をソート(sort orderd by flr-uniq)
                #sorted_terms = ( 'word' , { 'score' : {'basic' : {'項目' : 値 } , {'項目' : 値 } , ... }, ... }) , ...)
                sorted_terms = self.sort_terms(terms)
                
                #使用するscore項目名
                score_name_list = [ 'flr-uniq' , 'tf' , 'tf-idf' , 'c-value' , 'mc-value']
                
                #ソートされた単語を並び変えて代入
                #term_score_lists = 
                #{ 'dev_num' : [ {'term' : term, 'score_name' : score, ... } , { } , ...] , ' ' : [ ] , ...}
                term_score_lists[int(fileno)] = []
                term_score_list = term_score_lists [int(fileno)]
                #ソートされた単語から上位10位まででループを回す
                for sorted_term in sorted_terms[0 : EXTRACT_WORD_NUM]:
                    #sorted_term -> 0 -> 単語
                    term = sorted_term[0] #単語
                    #listに{'term' : 単語 } を追加
                    term_score_list.append({'term' : term })
                    
                    #score_nameでループを回す
                    for score_name in score_name_list:
                        #sorted_term -> 1 -> score -> basic -> 各スコア辞書
                        score = sorted_term[1]['score']['basic'][score_name] 
                        #listの最高尾の要素に 'score_name' : score の要素を追加
                        term_score_list[-1][score_name] =  score 
                    
                files_count += 1
            #<<with構文 end
        #<<ファイル単位のループ
            
        #sortしたtermsをcsvにして出力
        self.output_unmatched_terms_socores_csv(term_score_lists)
        
        
    def sort_terms(self, terms):
        """
        termsをソートして、returnする関数。参照渡しではない。
        """
        def sort_func_flr_uniq (item):
            """
            ソートするキーを返す。この関数ではscoreの中のflr-uniqを使用する。
            """
            return item[1]["score"]["basic"]["flr-uniq"]
        
        sorted_terms = sorted(terms.items(), key =sort_func_flr_uniq, reverse = True)
        #sorted_terms = [( 'word' , { 'score' : {'basic' : {'項目' : 値 } , {'項目' : 値 } , ... }, ... }) ,( ) , ..]
        #od(sorted_terms) = orderedDict([ {'word' : {'score' : {'basic' : {'項目' : 値 } , {'項目' : 値 } , ... }, ... } , ... ])
        return sorted_terms
   

        def output_unmatched_terms_socores_csv(self, term_score_lists):
            """
            :term_score_lists = { 'dev_num' : [ {'term' : term, 'score_name' : score, ... } , { } , ...] , ' ' : [ ] , ...}
            """
            score_names = ['terms' , 'flr-uniq' , 'tf' , 'tf-idf' , 'c-value' , 'mc-value']
            with open(r'%s/unmatched_pages_flr_uniq_words_multiscore.csv'%MY_DATA_FILE_PATH,'w',encoding="utf-8") as csv_file:
                #header部分
                header = [[],[]]
                header[0] = ['dev_num']
                header[0].extend(['terms'])
                header[0].extend(['term%s'%(i+1) for i in range(EXTRACT_WORD_NUM)])#dev_num , terms , term1 , term2...
                header[1] = ['']
                header[1].extend(['score_name'])
                header[1].extend(['score' for i in range(EXTRACT_WORD_NUM)])
                writer = csv.writer(csv_file, header, lineterminator='\n',delimiter='\t')#           , score_name , score , score...
                #header書き込み
                writer.writerows(header)
                
                #データ部分
                rows = []
                for dev_num , term_score_list in term_score_lists.items():
                    #termの行を作成
                    rows[0] = []
                    rows[0].append([dev_num])#dev_num
                    rows[0].append(['terms'])#dev_num , 'terms'
                    for term_score in term_score_list:
                        rows[0].append(term_score['term'])#dev_num , 'terms' , term1 , term2, ... 
                    
                    #score項目でループを回す
                    for i , score_name in enumerate(score_names) :
                        #各scoreの行を作成
                        rows[i + 1] = []
                        rows[i + 1].append([''])# '' 
                        rows[i + 1].append([score_name])# '' , score_name
                        for term_score in term_score_list:
                            rows[i + 1].append(term_score['score_name']) # '' , score_name , score1 , score2 , ....
                            
                #データ書き込み
                writer.writerows(rows)

if __name__ == '__main__':
    ScoreDecision().run()
