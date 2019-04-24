import tushare as ts
import pandas as pd



def FloatOrZero(value):
    try:
        return float(value)
    except:
        return 0.0
def printGrid():
    stock = ts.get_realtime_quotes('300058')
    bond = ts.get_realtime_quotes('123001')
    df = pd.DataFrame(columns=['b_benefit', 'b_vol', 'b_price','level', 'a_price', 'a_vol', 'a_benefit'])
    stock_price = float(stock.loc[0, 'bid'])*23.2
    for i in range(1, 6):
        bid_price = FloatOrZero(bond.loc[0, 'b'+str(i)+'_p'])
        bid_volume = FloatOrZero(bond.loc[0, 'b'+str(i)+'_v'])*10
        ask_price = FloatOrZero(bond.loc[0, 'a'+str(i)+'_p'])
        ask_volume = FloatOrZero(bond.loc[0, 'a'+str(i)+'_v'])*10
        df.loc[i] = [(stock_price/bid_price -1)*100 ,bid_volume, bid_price, i, ask_price, ask_volume, (stock_price/ask_price -1)*100]
    print df
    print 'stock price:' + str(float(stock.loc[0, 'bid']))
    print '\n\n'
    return df

def send_email(df):
    import smtplib
    from email.mime.text import MIMEText
    _user = "10314731@qq.com"
    _pwd = "liyekxqicqnt"
    _to = "10314731@qq.com"

    msg = MIMEText(df.to_string())
    msg["Subject"] = "300058"
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

import time
while True:
    df = printGrid()
    if df.loc[1, 'a_benefit'] > 0.8:
        send_email(df)
        break
    time.sleep(5)