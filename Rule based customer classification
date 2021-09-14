import numpy as np
import pandas as pd

# GÖREV 1
# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.

df = pd.read_csv(r"C:\Users\efego\PycharmProjects\pythonProject\VERI_BILIMI\2_HAFTA_ODEV\persona.csv")
df.head()
df.tail()
df.shape
df.info()
df.columns
df.index
df.describe().T
df.isnull().values.any()
df.isnull().sum()

# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
df[ "SOURCE" ].unique()
df[ "SOURCE" ].nunique()
df[ "SOURCE" ].value_counts()

#Soru 3: Kaç unique PRICE vardır?
df["PRICE"].nunique()

# Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df[ "PRICE" ].value_counts()

# Soru 5: Hangi ülkeden kaçar tane satış olmuş?
df["COUNTRY"].value_counts()

#Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY").agg({"PRICE": "sum"})

#Soru 7: SOURCE türlerine göre satış sayıları nedir?
df.groupby(["SOURCE"]).agg({"PRICE": "count"})

#Soru 8: Ülkelere göre PRICE ortalamaları nedir? ( PRICE COLUMN A MEAN NASIL YAZDIRILIR????)
df.groupby("COUNTRY").agg({"PRICE": "mean"})

#Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE").agg({"PRICE": "mean"})

#Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY","SOURCE"]).agg({"PRICE": "mean"})
#&&&&&
df.groupby(["COUNTRY","SOURCE"]).agg({"PRICE": "mean"}).unstack()#ilk=index,2.=sütun olur
#&&&&&&
df.pivot_table("PRICE","SOURCE","COUNTRY")

#Görev 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE": "mean"})

#Görev 3: Çıktıyı PRICE’a göre sıralayınız
agg_df=df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE",ascending=False)
agg_df

#Görev 4:Index’te yer alan isimleri değişken ismine çeviriniz.
agg_df.reset_index(inplace=True)



#Görev 5:Age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.(‘0_18', ‘19_23', '24_30', '31_40', '41_70')
#agg_df["AGE_CUT"] = pd.cut(agg_df["AGE"], [0, 18, 19, 23, 24, 30,31,40,41,70],right=False) agg_df
bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]

mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())]

agg_df["age_cat"] = pd.cut(agg_df["AGE"], bins, labels=mylabels)
agg_df.head()

#Görev 6 : Yeni seviye tabanlı müşterileri (persona) tanımlayınız.

for row in agg_df.values:
    print(row)

[row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]

agg_df["customers_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]
agg_df.head()

agg_df = agg_df[["customers_level_based", "PRICE"]]
agg_df.head()

agg_df["customers_level_based"].value_counts()


agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})


agg_df = agg_df.reset_index()
agg_df.head()


# Görev 7 : Yeni müşterileri (personaları) segmentlere ayırınız.

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])

agg_df.groupby("SEGMENT").agg({"PRICE": ["mean", "max", "sum"]})
agg_df[agg_df["SEGMENT"] == "C"]

#TAHMİN????????????????????????????????????????????????????????????????

# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?
new_user = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]
