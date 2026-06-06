import time
import yfinance as yf
import pandas as pd
# AAPL yerine bist değerleri yazılıp aralık ve peryot değerleri değiştirilebilinir.
data = yf.download("IMUX", period="1mo", interval="1h")
print(data.tail())
global mal
mal = 0
global para
para = 1                    #Burak Şahin Tarafından Kodlandı
#indikatörler (göstergeler)
def get_rsi():
    window = 14
    delta = data["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))
    r=data['RSI']
    return r.iloc[-1]
def get_sma():
    data["SMA_20"] = data["Close"].rolling(window=20).mean()
    data["SMA_50"] = data["Close"].rolling(window=50).mean()
    x=data['SMA_20'][-1:]
    y=data['SMA_50'][-1:]
    return x.iloc[-1],y.iloc[-1]
def get_macd():
    exp1 = data["Close"].ewm(span=12, adjust=False).mean()
    exp2 = data["Close"].ewm(span=26, adjust=False).mean()

    data["MACD"] = exp1 - exp2
    data["Signal_Line"] = data["MACD"].ewm(span=9, adjust=False).mean()
    cd=data['Signal_Line']
    return cd.iloc[-1]
    #Burada basit bir mal alımı ve nakit dönüşümünü sürekli kılan bir döngü mantığı ortaya konulmuştur.
    #yukardaki indikatörler üzerine basit bir olabilirlik mantığı ortaya konulmuştur.
def generate_signal(p,m):
    xx,yy=get_sma()
    rr=get_rsi()
    zz=get_macd()
    if zz<0.001 and p==0:
        print('acil çıkış satışı verildi ')
        print('nakite geçildi')
        print('1')
        global para
        para = 1
        global mal
        mal = 0
    else:
        if (xx> yy or rr<20 )and p>0 and m==0:
            print( "BUY")
            print('mal alındı')
            print('2')
            mal = 1
            para = 0
        elif (xx<80)and m>0 and p==0:
            print( "SELL")
            print('3')
            para = 1
            mal=0
        else:
            print('HOLD')
            print('4')
            print(rr)
def renklendir(datam):
    delta2 = data["Close"].diff()
    delta=delta2.iloc[-1]
    ss=delta.astype(float)
    if ss.any() < 0:
        print('yeşil')
    else:
        print('kırmızı')
renklendir(data)                #BURAK ŞAHİN TARAFINDAN KODLANDI


# Canlıya alma .....sinyal üretimine dikkat para-mal ???
while True:
    if para > 0:
        data["Signal"] = generate_signal(para, mal)
        print('-------')
        time.sleep(5)
        print('-------')
    elif mal > 0:
        data["Signal"] = generate_signal(para, mal)
        print('-------')
        time.sleep(5)
        print('-------')
    else:
        print('paydos')


