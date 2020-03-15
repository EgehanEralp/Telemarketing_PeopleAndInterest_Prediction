# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 13:59:11 2019

#@author: egehaneralp
"""
#%%
import pandas as pd
from flask import Flask,request,jsonify
import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
#Satıların ne iş yaptığını ve docker ın nasıl hazırlandığını ve çalıştığını anlatan bir döküman(txtdosyası) oluştur
#Ayrı bir docker projesi olarak sadece Öğrenme işlemini gerçekleştirip Modeli döndüren bir uygulama yap


#Flask başlangıcı
app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def girisFonk():
    return "giris sayfası"
################################################################################
                          ##DOSYADAN TAHMİN##
@app.route("/DosyaAnaliz", methods=['POST','GET'])
def islemler():
    
     #model var mı kontrol et!
    try:
        f = open('modelv1.sav','rb')
    except FileNotFoundError:
        return "Olusturulmus bir model bulunmadı"
    
    loaded_model = pickle.load(open('modelv1.sav', 'rb'))

    # checking if the file is present or not.
    if 'file' not in request.files:
        return "Girilen KEY 'file' olmalıdır "
    file = request.files['file']
    
    TestVerileri =  pd.read_excel(file) ##############GÜNCELLENECEK
    STest = TestVerileri[['CINSIYET','SEHIR','SATIS_DURUM']]   ##STRING E CEVİR
    IntTest = TestVerileri[['URUN_ADEDI','ARIZA_HIZMET_ADEDI','CAGRI_ADEDI','HIZMET_ADEDI']]
    idTest = TestVerileri[['CRM_ID']]
    StringTest = STest.astype(str)
    TestVerileriSON = pd.concat([StringTest,IntTest],axis=1)
    
    satirsayi=len(TestVerileri.index)                    #DATA FRAME de KAÇ VERİ VAR ??
    
    
    kaynakTest = TestVerileriSON[['CINSIYET','SEHIR','URUN_ADEDI','ARIZA_HIZMET_ADEDI','CAGRI_ADEDI','HIZMET_ADEDI']]
    
    probs = loaded_model.predict_proba(kaynakTest, check_input=True)
    probsDF = pd.DataFrame(data=probs, index=range(satirsayi), columns=['alma_olasılığı','olasılık2'])
    
    scaler = MinMaxScaler(feature_range=(0.0001, 0.9999))
    scaler = scaler.fit(probsDF)
    normalized = scaler.transform(probsDF)  #float64 tipinde 
    
    normDF = pd.DataFrame(data=normalized, index= range(satirsayi), columns=['hizmet_alma_olasılığı','normalizeOlasılık2'])
    
    tahmin = loaded_model.predict(kaynakTest)
    tahmin = pd.DataFrame(data=tahmin,index=range(satirsayi),columns=['tahmin'])
   
    birlesim= pd.concat([kaynakTest,tahmin],axis=1)
    birlesim2 =pd.concat([birlesim,idTest],axis=1)
    birlesim3 = pd.concat([probsDF,birlesim2],axis=1)
    birlesim4=pd.concat([birlesim3,normDF],axis=1)
    
    filteredSonTablo = birlesim4[['CRM_ID','tahmin','hizmet_alma_olasılığı']]     #sadece id ve tahmin sonucumuz olan tablomuz
    
    #bu tabloyu JSON' casting işlemi yapıp return edicez.
    jsonX = filteredSonTablo.to_json(orient='records')   #orient'in default value 'columns'tur -> Her satırı Json object
                                                         #olarak görüntülemek için orient='records' yaz.    
    return jsonX

################################################################################
                        #BİREYSEL JSON VERİ ANALİZİ#
@app.route('/BireyAnaliz', methods=['POST','GET'])
def MLdeneme():
    
    #model var mı kontrol et!
    try:
        f = open('modelv1.sav','rb')
    except FileNotFoundError:
        return "Olusturulmus bir model bulunmadı"

    #POST edilen Json verilerini alır.#
    
    veriler = request.get_json()
    sehir =veriler['Sehir']
    cinsiyet =veriler['Cinsiyet']
    urunadedi =veriler['Urun_adedi']
    hizmetadedi =veriler['Hizmet_adedi']
    arizahizmetadedi =veriler['Ariza_hizmet_adedi']
    cagriadedi =veriler['Cagri_adedi']
    idx =veriler['CustID']
    
    string = MLcalistir(sehir,cinsiyet,urunadedi,hizmetadedi,arizahizmetadedi,cagriadedi,idx)
    #s2     =  MLcalistir2(sehir,cinsiyet,urunadedi,hizmetadedi,arizahizmetadedi,cagriadedi,idx)
    return jsonify({'CustID':idx,
                    'TahminSonucu':string })

def MLcalistir(sehir,cinsiyet,urunadedi,hizmetadedi,arizahizmetadedi,cagriadedi,idx):
            
    loaded_model = pickle.load(open('modelv1.sav', 'rb'))
      
    # JSON OBJECT == PYTHON DICTIONARY # -> Bu yuzden dictionary kullanıldı
    dict_s = {'Sehir': sehir, 'Cinsiyet': cinsiyet, 'Urun_adedi':urunadedi,'Hizmet_adedi':hizmetadedi,
              'Ariza_hizmet_adedi':arizahizmetadedi, 'Cagri_adedi':cagriadedi}
    
    dict_sd= {'SATIS_DURUM':"x"}
    
    # Python Dictionary'leri Data Frame'e dönüştürmek #
    TahminEdilecekBirey = pd.DataFrame(data=dict_s,index=range(1))   # tek satıra dict_s de belirlediğim sütun ve özelliklerini yazdırdım.   
    tahminsatisdurumu = pd.DataFrame(data=dict_sd, index=range(1))   # tahmin edilecek sütun
    
    # İki Data Frame'i birleştirmek
    idsizTablo= pd.concat([TahminEdilecekBirey,tahminsatisdurumu], axis=1) #HEDEF TABLO (tüm sütunları tamam olan 1 SATIR)
        
    # test süreci
    kaynakTest = idsizTablo[['Sehir','Cinsiyet','Urun_adedi','Hizmet_adedi','Ariza_hizmet_adedi','Cagri_adedi']]
    
    tahmin = loaded_model.predict(kaynakTest)
    
    tahmin = pd.DataFrame(data=tahmin,index=range(1),columns=['tahmin'])
   
    str = tahmin['tahmin'].values[0]
    #tahmin sütununun verisini return et
    return str

################################################################################
                    ###MODEL OLUŞTURMAK##
      #Modeli programı ilk çağırdığında oluşturmak için dosya POST et#
#Eğer mevcut modelin değişmediyse direkt olarak /DosyaAnaliz veya /BireyAnaliz çalıştırabilirsin#
@app.route("/ModelOlustur", methods=['POST','GET'])
def func():
    
    if 'file' not in request.files:
        return "Girilen KEY 'file' olmalıdır"
    file = request.files['file']
    
    TrainVerileri = pd.read_excel(file)
    STrain = TrainVerileri[['CINSIYET','SEHIR','SATIS_DURUM']] #3 sütun
    IntTrain = TrainVerileri[['URUN_ADEDI','ARIZA_HIZMET_ADEDI','CAGRI_ADEDI','HIZMET_ADEDI']]
    StringTrain = STrain.astype(str)
    TrainVerileriSON = pd.concat([StringTrain,IntTrain],axis=1)
    
    DTclf = DecisionTreeClassifier()
    kaynak = TrainVerileriSON[['CINSIYET','SEHIR','URUN_ADEDI','ARIZA_HIZMET_ADEDI','CAGRI_ADEDI','HIZMET_ADEDI']]
    hedef = TrainVerileriSON[['SATIS_DURUM']] 
    DTclf = DTclf.fit(kaynak,hedef)
    
    pickle.dump(DTclf, open('modelv1.sav', 'wb'))
    
    
    
    x_train,x_test,y_train,y_test=train_test_split(kaynak,hedef,test_size=0.125,random_state=0,stratify=hedef)
    
    DTclf2 = DecisionTreeClassifier()
    model = DTclf2.fit(x_train,y_train)  
   
    return ("Model Oluşturma İşlemi Başarılı.<br> Öğrenmenin başarısı: %" +
            (("{0:.2f}".format(model.score(x_test, y_test)*100))))

################################################################################
#Flask sonu

if(__name__ == "__main__"): # bu dosyam terminalden mi çalıştırılmış ?? KONSOLDA bu uygulamamın klasörüne gidip -> 'python RestAndML.py'  komutunu yaz    
    app.run(host='0.0.0.0')