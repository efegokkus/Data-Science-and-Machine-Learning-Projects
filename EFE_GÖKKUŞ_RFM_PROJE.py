import datetime as dt
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option("display.width", 500)
df_ = pd.read_excel(r"C:\Users\efego\PycharmProjects\pythonProject\VERI_BILIMI\datasets\online_retail_II.xlsx",
                    sheet_name="Year 2010-2011")
# GÖREV 1 :
# 1. Online Retail II excelindeki 2010-2011 verisini okuyunuz. Oluşturduğunuz dataframe’in kopyasını oluşturunuz
df = df_.copy()
df.head()

# 2. Veri setinin betimsel istatistiklerini inceleyiniz
df.shape
df.info()

df.describe().T

# 3. Veri setinde eksik gözlem var mı? Varsa hangi değişkende kaç tane eksik gözlem vardır?
df.isnull().sum()

# 4. Eksik gözlemleri veri setinden çıkartınız. Çıkarma işleminde ‘inplace=True’ parametresini kullanınız.
df.dropna(inplace=True)

# 5. Eşsiz ürün sayısı kaçtır?
df.nunique()

# 6. Hangi üründen kaçar tane vardır?
df[ "Description" ].value_counts().head()

# 7. En çok sipariş edilen 5 ürünü çoktan aza doğru sıralayınız
df.groupby("Description").agg({"Quantity": "sum"}).sort_values(by="Quantity", ascending=False)

# 8. Faturalardaki ‘C’ iptal edilen işlemleri göstermektedir.
# İptal edilen işlemleri veri setinden çıkartınız.
df = df[ ~df[ "Invoice" ].str.contains("C", na=False) ]
# Quantity ve Price 0 dan büyük olmalı
df = df[ df[ "Quantity" ] > 0 ]
df = df[ df[ "Price" ] > 0 ]

# 9. Fatura başına elde edilen toplam kazancı ifade eden ‘TotalPrice’ adında bir değişken oluşturunuz.
df[ "Total_Price" ] = df[ "Quantity" ] * df[ "Price" ]

# Görev 2:RFM metriklerinin hesaplanması
df[ "InvoiceDate" ].max()
today = dt.datetime(2011, 12, 11)
# InvoiceDate== RECENCY
# Invoice.nunique() == FREQUENCY
# Total_Price == MONETARY OLACAK

rfm = df.groupby("Customer ID").agg({"InvoiceDate": lambda InvoiceDate: (today - InvoiceDate.max()).days,
                                     "Invoice": lambda Invoice: Invoice.nunique(),
                                     "Total_Price": lambda Total_Price: Total_Price.sum()})
rfm.columns = [ "recency", "frequency", "monetary" ]
rfm = rfm[ rfm[ "monetary" ] > 0 ]

# Görev 3:RFM skorlarının oluşturulması ve tek bir değişkene çevrilmesi
rfm[ "recency_score" ] = pd.qcut(rfm[ "recency" ], 5, labels=[ 5, 4, 3, 2, 1 ])
rfm[ "frequency_score" ] = pd.qcut(rfm[ "frequency" ].rank(method="first"), 5, labels=[ 1, 2, 3, 4, 5 ])
rfm[ "monetary_score" ] = pd.qcut(rfm[ "monetary" ], 5, labels=[ 1, 2, 3, 4, 5 ])
rfm[ "RFM_SCORE" ] = rfm[ "recency_score" ].astype(str) + rfm[ "frequency_score" ].astype(str)

# Görev 4:RFM skorlarının segment olarak tanımlanması
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm[ "segment" ] = rfm[ "RFM_SCORE" ].replace(seg_map, regex=True)

# Görev 5:Aksiyon zamanı!
rfm.head()
rfm[ rfm[ "segment" ] == "champions" ].sort_values(by=[ "recency", "frequency" ], ascending=False)
rfm[ rfm[ "segment" ] == "champions" ].agg("mean")
rfm[ [ "segment", "recency", "frequency", "monetary",] ].groupby("segment").agg([ "mean", "count" ])

rfm[rfm["segment"]=="need_attention"].groupby("segment").agg([ "mean", "count" ])

# Sonuçlar göz önünde bulundurulduğunda champions, at_Risk ve cant_loose segmentlerin de aksiyon gerekmektedir.
#########################################
# 1.Champions
#########################################

# Champions segmenti en sık alışveriş yapan ortalama 6 gün ve en çok para ortalama 6858 Sterlin bırakan sınıftır.
# Bu segmente "premium,gold,diamond" gibi site içinde ayrıcalıklı olduklarını gösterecek üyelikler tanımlanmalı ,
# bu üyeliklere özel indirimler yapılmalıdır.Böylece hem verdikleri paranın karşılığını kat kat aldıklarını düşünecekler
# hem de diğer segmentlerde bulunan üyelerde bu segmente çıkıp ayrıcalıklardan yararlanmak için daha fazla aksiyon
# göstereceklerdir.

##########################################
#2.Cant_loose
##########################################
# cant_loose segmenti ortalama 133 günde bir alışveriş yapan ancak Loyal_customers segmentiyle yarışacak miktarda para
# bırakan ortalama 2797 Sterlin,
# segmenttir.Dolayısıyla kayıp olmamaları için promosyonlu ürünleri ya da haftasonu indirimlerini içeren mail
# veya sms atılmalı ve bizi hatırlamaları sağlanmalıdır.

##########################################
#3.At_Risk
##########################################

# At_Risk segmenti ortalama 154 günde bir ve ortalama 1085 Sterlin para bırakan sınıftır.
# Yeni müşteri eldeki müşteriden daha maliyetlidir prensibi gereği bu segmente özel hafta sonu indirimi,
# bu güne özel kargo ücretsiz gibi mesajlar atılmalıdır.


#"Loyal Customers" sınıfına ait customer ID'leri seçerek excel çıktısını alınız.
new_df=pd.DataFrame()
new_df["loyal_customers_Id"]=rfm[rfm["segment"]=="loyal_customers"].index
new_df.to_csv("loyal_customers.csv")




