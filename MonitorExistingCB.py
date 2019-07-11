import pandas as pd
import requests
import time

BOND_INCREASE_RT_THRESHOLD = 3.0

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

jisiluUrl = "https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___t=" + str(time.time())
resp = requests.get(url=jisiluUrl)
data = resp.json()
cbonds=[]
for r in data['rows']:
    cbonds.append(r['cell'])
jdf = pd.DataFrame.from_dict(cbonds)        # jisilu df
jdf.bond_id = jdf.bond_id.astype(str)


with open('trade/existing_bonds.txt') as f:
    exist_bonds = f.readlines()
exist_bonds = set([x.strip() for x in exist_bonds])
rdf = jdf.loc[jdf.bond_id.isin(exist_bonds), ['bond_id','bond_nm', 'increase_rt', 'price', 'sincrease_rt', 'premium_rt']]
# rdf.bond_nm = rdf.bond_nm.str.encode('utf-8')

rdf.increase_rt = rdf.increase_rt.apply(lambda s: s.replace('%', ''))
rdf.increase_rt = rdf.increase_rt.astype('float')
# rdf.sincrease_rt = rdf.sincrease_rt.apply(lambda s: s if '%' in s else '0.0%')
# rdf.sincrease_rt = rdf.sincrease_rt.apply(lambda s: s.replace('%', ''))
# rdf.sincrease_rt = rdf.sincrease_rt.astype('float')

def send_email(content, pwd):
    import smtplib
    from email.mime.text import MIMEText
    _user = "10314731@qq.com"
    _pwd = pwd
    _to = "10314731@qq.com"

    msg = MIMEText(content)
    msg["Subject"] = "monitoring existing bonds"
    msg["From"] = _user
    msg["To"] = _to

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
        print "Success!"
    except smtplib.SMTPException, e:
        print "Falied,%s" % e

alert_rdf = rdf.loc[rdf.increase_rt>BOND_INCREASE_RT_THRESHOLD, :]

if alert_rdf.size>0 :
    alert_rdf.to_csv('temp/monitor.csv', encoding='utf-8')
    with open('temp/monitor.csv') as f:
        s = f.read() + '\n'
    import sys
    send_email(s, sys.argv[1])

