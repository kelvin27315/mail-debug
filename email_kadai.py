"""
課題で設定したe-mailの設定をチェックするプログラム
"""

from pathlib import Path
import codecs
import email
import time
import re
import pandas as pd

def read_mails():
    """
    同階層にあるmailフォルダの中に入っているメールのファイルを読み込む
    """
    path = Path.cwd() / "mail"
    mails_path = list(path.iterdir())
    mails = []
    for m in mails_path:
        with open(m, 'rb') as f:
            mails.append(email.message_from_bytes(f.read()))
    return mails

if __name__ == "__main__":
    mails = read_mails()
    stu = pd.DataFrame({"Date": 0,
                        "addres": ["" for i in range(len(mails))],
                        "From tf": False,
                        "From": "",
                        "Reply-To tf": False,
                        "Reply-To": "",
                        "ORGANIZATION tf": False,
                        "ORGANIZATION": "",
                        "X-MAILER": "",
                        "Content": ""})

    #メールのファイルを１つづつチェックしてDataFrameに反映させる
    for i,mail in enumerate(mails):
        #メールアドレスと送信者名(From)を反映
        head = email.header.decode_header(mail.get("From"))
        if len(head) == 2:
            stu.at[i,"From tf"] = True
            stu.at[i,"From"] = head[0][0].decode(head[0][1])
            stu.at[i,"addres"] = head[1][0].decode("utf-8")[2:-1]
        else:
            stu.at[i,"addres"] = head[0][0][1:-1]

        #返信先(Reply-To)を反映
        reply = mail.get("Reply-To")
        if reply is not None:
            reply = email.header.decode_header(reply)
            stu.at[i,"Reply-To tf"] = True
            stu.at[i,"Reply-To"] = reply[0][0][1:-1]

        #所属を反映
        org = mail.get("ORGANIZATION")
        if org is not None:
            org = email.header.decode_header(org)
            stu.at[i,"ORGANIZATION tf"] = True
            if org[0][1] is not None:
                stu.at[i,"ORGANIZATION"] = org[0][0].decode(org[0][1])
            else:
                stu.at[i,"ORGANIZATION"] = org[0][0]
        #メーラーの名前を反映
        stu.at[i,"X-MAILER"] = mail.get("X-MAILER")
        #送信時刻を反映
        stu.at[i,"Date"] = int(time.strftime("%Y%m%d%H%M%S", email.utils.parsedate(mail.get("Date"))))
        #本文を反映
        stu.at[i,"Content"] = mail.get_payload(decode=True).decode(mail.get_content_charset())

    #送信時刻でソート
    stu = stu.sort_values("Date")
    print(stu)
    for i, student in stu.iterrows():
        #知りたい条件に合わせて式を書き換え
        if student["From tf"] == False:
            print("******************************************************************")
            print("addres:\t\t\t{}".format(student["addres"]))
            print("From tf:\t\t{}".format(student["From tf"]))
            print("From:\t\t\t{}".format(student["From"]))
            print("Reply-To tf:\t\t{}".format(student["Reply-To tf"]))
            print("Reply-To:\t\t{}".format(student["Reply-To"]))
            print("ORGANIZATION tf:\t{}".format(student["ORGANIZATION tf"]))
            print("ORGANIZATION:\t\t{}".format(student["ORGANIZATION"]))
            print("Content:\n{}".format(student["Content"]))
