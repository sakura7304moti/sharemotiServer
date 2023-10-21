"""
Flask Server
"""
import json
import os
import urllib
import glob
import sys
import traceback
import re
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_file
from flask import flash , redirect , url_for
from markupsafe import escape
from werkzeug.utils import secure_filename

"""
ファイルアップロード
"""
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""
Flask run
"""
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

# Twitter
from motitter.src import sqlite as motitter_sqlite
from motitter.src import const as motitter_const
import math

# Nitter
from monitter.src import sqlite as monitter_sqlite
from monitter.src import const as monitter_const

# Hololewd
from mottit.src import sqlite as hololewd_sqlite
from mottit.src import const as hololewd_const

# WordList
from sharemotiApi.src import wordList

# WordList2
from sharemotiApi.src import wordList2

# NameList
from sharemotiApi.src import const as sharemoti_const
from sharemotiApi.src import nameList

# YakiList
from sharemotiApi.src import yakiList

# SchoolList
from sharemotiApi.src import schoolList

# MannerList
from sharemotiApi.src import mannerList

#HaikuList
from sharemotiApi.src import haikuList

#HoloSong
from holosong.src import const as holosong_const
from holosong.src import utils as holosong_utils
from holosong.src import sqlite as holosong_sqlite

#ImageList
from sharemotiApi.src import imageList

#KaraokeList
from sharemotiApi.src import karaokeList

#VoiceList
from sharemotiApi.src import voiceList

#SsbuList
from sharemotiApi.src import ssbuList

config = motitter_const.api_option()
PAGE_SIZE = config.PAGE_SIZE

"""
Twitter API
"""


@app.route("/twitter/search", methods=["POST"])
def twitter_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    # JSONデータから必要なパラメータを抽出
    page_no = json_data.get("page_no", 1)
    page_size = json_data.get("page_size", 40)
    hashtag = json_data.get("hashtag", "")
    start_date = json_data.get("start_date", "")
    end_date = json_data.get("end_date", "")
    user_name = json_data.get("user_name", "")
    min_like = json_data.get("min_like", 0)
    max_like = json_data.get("max_like", 0)

    # search()関数を呼び出し
    records = motitter_sqlite.search(
        page_no, page_size, hashtag, start_date, end_date, user_name, min_like, max_like
    )

    # search_count()関数を呼び出し
    count = motitter_sqlite.search_count(
        hashtag, start_date, end_date, user_name, min_like, max_like
    )
    totalPages = math.ceil(count / page_size)

    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        ),
        "totalPages": totalPages,
    }

    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "{'records':[],'totalPages':0}"
    response = jsonify(json_data)
    return response


@app.route("/twitter/search/count", methods=["POST"])
def twitter_search_count_handler():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得

    hashtag = json_data.get("hashtag", "")
    start_date = json_data.get("start_date", "")
    end_date = json_data.get("end_date", "")
    user_name = json_data.get("user_name", "")
    min_like = json_data.get("min_like", 0)
    max_like = json_data.get("max_like", 0)

    # search_count()関数を呼び出し
    count = motitter_sqlite.search_count(
        hashtag, start_date, end_date, user_name, min_like, max_like
    )

    # レスポンスとして結果を返す
    response = jsonify(count=count)
    return response


@app.route("/twitter/hololist", methods=["GET"])
def twitter_get_hololist():
    json_data = json.dumps(motitter_const.holoList(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

"""
Monitter Nitter
"""
@app.route("/nitter/search", methods=["POST"])
def nitter_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    # JSONデータから必要なパラメータを抽出
    page_no = json_data.get("page_no", 1)
    page_size = json_data.get("page_size", 40)
    hashtag = json_data.get("hashtag", "")
    start_date = json_data.get("start_date", "")
    end_date = json_data.get("end_date", "")
    user_name = json_data.get("user_name", "")
    mode = json_data.get("mode","")
    min_like = json_data.get("min_like", 0)
    max_like = json_data.get("max_like", 0)

    # search()関数を呼び出し
    records = monitter_sqlite.search(
        page_no, page_size, hashtag, start_date, end_date, user_name,mode, min_like, max_like
    )

    # search_count()関数を呼び出し
    count = monitter_sqlite.search_count(
        hashtag, start_date, end_date, user_name,mode, min_like, max_like
    )
    totalPages = math.ceil(count / page_size)

    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        ),
        "totalPages": totalPages,
    }

    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "{'records':[],'totalPages':0}"
    response = jsonify(json_data)
    return response


@app.route("/nitter/search/count", methods=["POST"])
def nitter_search_count_handler():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得

    hashtag = json_data.get("hashtag", "")
    start_date = json_data.get("start_date", "")
    end_date = json_data.get("end_date", "")
    user_name = json_data.get("user_name", "")
    mode = json_data.get("mode","")
    min_like = json_data.get("min_like", 0)
    max_like = json_data.get("max_like", 0)

    # search_count()関数を呼び出し
    count = monitter_sqlite.search_count(
        hashtag, start_date, end_date, user_name,mode, min_like, max_like
    )

    # レスポンスとして結果を返す
    response = jsonify(count=count)
    return response


@app.route("/nitter/hololist", methods=["GET"])
def nitter_get_hololist():
    json_data = json.dumps(monitter_const.holoList(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

"""
Hololewd ホロライブのエロ画像
"""


@app.route("/hololewd/search", methods=["POST"])
def hololewd_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    # JSONデータから必要なパラメータを抽出
    page_no = json_data.get("page_no", 1)
    page_size = json_data.get("page_size", 40)
    fullName = json_data.get("full_name", "")
    firstName = json_data.get("first_name", "")
    lastName = json_data.get("last_name", "")
    min_like = json_data.get("min_like", 0)
    max_like = json_data.get("max_like", 0)

    # search()関数を呼び出し
    records = hololewd_sqlite.search(
        page_no, page_size, fullName, firstName, lastName, min_like, max_like
    )

    # search_count()関数を呼び出し
    count = hololewd_sqlite.search_count(
        fullName, firstName, lastName, min_like, max_like
    )
    totalPages = math.ceil(count / page_size)

    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        ),
        "totalPages": totalPages,
    }

    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "{'records':[],'totalPages':0}"
    response = jsonify(json_data)
    return response


@app.route("/hololewd/hololist", methods=["GET"])
def hololewd_get_hololist():
    ls = []
    df = hololewd_const.holo_df()
    for index, row in df.iterrows():
        fullName = row.FullName
        ls.append(fullName)
    json_data = json.dumps(ls, ensure_ascii=False)
    response = jsonify(json_data)
    return response


"""
WordList 名言集
"""
@app.route("/wordList/search", methods=["POST"])
def wordlist_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    text = json_data.get("text", "")

    records = wordList.search(text)
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response


@app.route("/wordList/save", methods=["POST"])
def wordlist_save():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")
    desc = json_data.get("desc", "")

    result = wordList.save(word, desc)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response


@app.route("/wordList/delete", methods=["POST"])
def wordlist_delete():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")
    desc = json_data.get("desc", "")

    res = wordList.delete(word, desc)
    result = {"status": res}
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response

"""
WordList2 名言集2
"""
@app.route("/wordList2/search", methods=["POST"])
def wordlist2_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    text = json_data.get("text", "")

    records = wordList2.search(text)
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response


@app.route("/wordList2/save", methods=["POST"])
def wordlist2_save():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")
    desc = json_data.get("desc", "")

    result = wordList2.save(word, desc)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response


@app.route("/wordList2/delete", methods=["POST"])
def wordlist2_delete():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")
    desc = json_data.get("desc", "")

    res = wordList2.delete(word, desc)
    result = {"status": res}
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response


"""
nameList あだ名一覧
"""
@app.route("/nameList/search", methods=["POST"])
def namelist_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    key = json_data.get("key", "")
    val = json_data.get("val", "")

    records = nameList.search(key, val)
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response


@app.route("/nameList/insert", methods=["POST"])
def namelist_insert():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    key = json_data.get("key", "")
    val = json_data.get("val", "")

    result = nameList.insert(key, val)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response


@app.route("/nameList/update", methods=["POST"])
def namelist_update():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    bkey = json_data.get("bkey", "")
    bval = json_data.get("bval", "")
    key = json_data.get("key", "")
    val = json_data.get("val", "")

    result = nameList.update(bkey, bval, key, val)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response


@app.route("/nameList/delete", methods=["POST"])
def namelist_delete():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    key = json_data.get("key", "")
    val = json_data.get("val", "")

    res = nameList.delete(key, val)
    result = {"status": res}
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response


@app.route("/nameList/init", methods=["GET"])
def namelist_init():
    nameList.init_update()


@app.route("/nameList/names", methods=["GET"])
def nameList_names():
    ls = sharemoti_const.ssbu_names()
    json_data = json.dumps(ls, ensure_ascii=False)
    response = jsonify(json_data)
    return response

"""
YakiList 焼き直し条約
"""
@app.route("/yakiList/search", methods=["POST"])
def yakiList_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    text = json_data.get("text", "")

    records = yakiList.search(text)
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response


@app.route("/yakiList/save", methods=["POST"])
def yakiList_save():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")
    yaki = json_data.get("yaki", "")

    result = yakiList.save(word, yaki)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response


@app.route("/yakiList/delete", methods=["POST"])
def yakiList_delete():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")
    yaki = json_data.get("yaki", "")

    res = yakiList.delete(word, yaki)
    result = {"status": res}
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response

"""
SchoolList 学校一覧
"""
@app.route("/schoolList/search", methods=["POST"])
def schoolList_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")

    records = schoolList.search(word)
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response


@app.route("/schoolList/save", methods=["POST"])
def schoolList_save():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")

    result = schoolList.save(word)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response


@app.route("/schoolList/delete", methods=["POST"])
def schoolList_delete():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")

    res = schoolList.delete(word)
    result = {"status": res}
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response

"""
MannerList 日本国失礼憲法
"""
@app.route("/mannerList/search", methods=["POST"])
def mannerList_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")

    records = mannerList.search(word)
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response


@app.route("/mannerList/save", methods=["POST"])
def mannerList_save():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")

    result = mannerList.save(word)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response


@app.route("/mannerList/delete", methods=["POST"])
def mannerList_delete():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")

    res = mannerList.delete(word)
    result = {"status": res}
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response

"""
HaikuList 王将マン俳句コンテスト
"""
@app.route("/haikuList/search",methods=["POST"])
def haikuList_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    id = int(json_data.get("id","-1"))
    haikuText = json_data.get("haikuText","")
    poster = json_data.get("poster","")
    detail = json_data.get("detail","")

    records = haikuList.select(id,haikuText,poster,detail)
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response

@app.route("/haikuList/insert",methods=["POST"])
def haikuList_insert():
    json_data = request.json
    first = json_data.get("first","")
    second = json_data.get("second","")
    third = json_data.get("third","")
    poster = json_data.get("poster","")
    detail = json_data.get("detail","")

    result = haikuList.insert(first,second,third,poster,detail)
    print(result.__dict__)
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

@app.route("/haikuList/update",methods=["POST"])
def haikuList_update():
    json_data = request.json
    id = int(json_data.get("id",-1))
    first = json_data.get("first","")
    second = json_data.get("second","")
    third = json_data.get("third","")
    poster = json_data.get("poster","")
    detail = json_data.get("detail","")

    result = haikuList.update(id,first,second,third,poster,detail)
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

@app.route("/haikuList/delete",methods=["POST"])
def haikuList_delete():
    json_data = request.json
    id = int(json_data.get("id",-1))
    result = haikuList.delete(id)
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

"""
ホロライブの歌ってみたを取得する
"""
@app.route("/holoSong/search",methods=["GET"])
def holosong_select():
    records = holosong_utils.get_cover_songs()
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response

@app.route("/holoSong/hololist", methods=["GET"])
def holosong_get_hololist():
    json_data = json.dumps(holosong_const.holoList(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

"""
ホロライブのオリキョクを取得する
"""
@app.route('/holoSong/ori',methods=["GET"])
def holosong_ori():
    records = holosong_utils.get_original_songs()
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response

"""
ホロライブのアルバムを取得する
"""
@app.route('/holosong/album',methods=["GET"])
def holosong_album():
    records = holosong_sqlite.select_album()
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response

@app.route('/holosong/album/music',methods=["GET"])
def holosong_album_music():
    records = holosong_sqlite.select_music()
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response

"""
ファイルアップロード・ダウンロード
"""
@app.route('/imageList/insert',methods=['POST'])
def imagelist_insert():
    json_data = request.json
    file_name = json_data.get("fileName","")
    title = json_data.get("title","")
    detail = json_data.get("detail","")
    
    result = imageList.insert(file_name,title,detail)
    
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response
    
@app.route('/imageList/upload', methods=['GET', 'POST'])
def imagelist_upload():
    # check if the post request has the file part
    print(request.files)
    if 'file' not in request.files:
        flash('No file part')
        jsondata = {"fileName":''}
        response = jsonify(jsondata)
        return response
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        print('No selected file')
        jsondata = {"fileName":''}
        response = jsonify(jsondata)
        return response

    #ext ok filename ok
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        
        # 現在の日時を取得
        now = datetime.datetime.now()
        formatted_datetime = now.strftime("%Y%m%d%H%M%S")
        save_file_name = formatted_datetime + '.' + ext
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], save_file_name))
        
        jsondata = {"fileName":save_file_name}
        response = jsonify(jsondata)
        return response
        
@app.route('/imageList/download',methods=['GET'])
def imagelist_download():
    #image file only
    file_name = request.args.get('file')
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'],file_name).replace('./','') , mimetype='image/jpeg')

@app.route("/imageList/search",methods=['GET'])
def imagelist_search():
    records = imageList.search()
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response

@app.route("/imageList/update",methods=["POST"])
def imagelist_update():
    json_data = request.json
    id = json_data.get("id",-1)
    title = json_data.get("title","")
    detail = json_data.get("detail","")
    
    result = imageList.update(id,title,detail)
    
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

@app.route("/imageList/delete",methods=["POST"])
def imagelist_delete():
    json_data = request.json
    id = json_data.get("id",-1)
    
    result = imageList.delete(id)
    
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

"""
カラオケ一覧
"""
@app.route("/karaoke/search",methods=['GET'])
def karaokelist_search():
    records = karaokeList.search()
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response

@app.route('/karaoke/download',methods=['GET'])
def karaokelist_download():
    id = int(request.args.get('id',-1))
    print(f'id -> {id}')
    rec = karaokeList.select(id)
    path = os.path.join('./','sharemotiApi','data','karaoke',rec.date,rec.file_name+'.mp3')
    print(path)
    return send_file(path , mimetype='audio/mpeg')

"""
ボイス一覧
"""
@app.route("/voice/search",methods=['GET'])
def voicelist_search():
    records = voiceList.search()
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response

@app.route('/voice/download',methods=['GET'])
def voicelist_download():
    id = int(request.args.get('id',-1))
    print(f'id -> {id}')
    rec = voiceList.select(id)
    path = os.path.join('./','sharemotiApi','data','voice',rec.file_name+'.mp3')
    print(path)
    return send_file(path , mimetype='audio/mpeg')

"""
スマブラの切り抜き
"""
@app.route("/ssbu/search",methods=['GET'])
def ssbulist_search():
    records = ssbuList.search()
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response

@app.route('/ssbu/download',methods=['GET'])
def ssbulist_download():
    id = int(request.args.get('id',-1))
    print(f'id -> {id}')
    rec = voiceList.select(id)
    path = os.path.join('./','sharemotiApi','data','ssbu',rec.year,rec.date,rec.file_name+'.mp4')
    print(path)
    return send_file(path , mimetype='video/mp4')

"""
その他のエンドポイント
"""
@app.route("/support/download_image",methods=["GET"])
def download_image():
    image_url = request.args.get('url')
    try:
        req = urllib.request.Request(image_url)
        req.add_header("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0")
        image_response = urllib.request.urlopen(req)
        return send_file(image_response, mimetype='image/jpeg')
    except Exception as e:
        return str(e), 400

if __name__ == "__main__":
    wordList.init()
    wordList2.init()
    nameList.init()
    yakiList.init()
    schoolList.init()
    mannerList.init()
    haikuList.init()
    holosong_sqlite.init()
    imageList.init()
    app.run(host="0.0.0.0", debug=False)
