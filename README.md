# Telemarketing_PeopleAndInterest_Prediction
Flask Web Service ile oluşturulmuş, 'Müşteri' ile 'Ürün satın alma' ilişkisini ortaya koyan ve kalıcı model oluşturmayı sağlayan programım.


# Docker üzerinden ilk çalıştırma	
(image çalıştırmak ve container oluşturmak):
//<tag> olan yere https://hub.docker.com/r/egehaneralp/get-started/tags adresinden en son oluşturulmuş Tag i yaz
$ docker pull egehaneralp/get-started:<tag>       //image'ı kendi bilgisayarına aktar
$ docker run -p 5000:5000 egehaneralp/get-started:<tag>

örn:	
docker pull egehaneralp/get-started:v2
docker run -p 5000:5000 egehaneralp/get-started:v2
----------------
İlk çalıştırma sonrası oluşmuş container'ın ID bilgisine '$ docker container ls --all' komutu ile erişilir,
$ docker start <CONTAINER_ID>
$ docker stop <CONTAINER_ID>
komutları ile uygulama çalıştırılır ve durdurulur.



# /ModelOlustur
-------------------------
- Servise Post Edilecek dosya için KEY == 'file' olmalıdır.
- .xlsx/.xls uzantılı dosyalar ile öğrenim yapabilir.
- 'CINSIYET','SEHIR','SATIS_DURUM','URUN_ADEDI','ARIZA_HIZMET_ADEDI','CAGRI_ADEDI',
  'HIZMET_ADEDI'
  sütunlarını içeriyor olmalıdır.


# /DosyaAnaliz
------------------------
- Kullanım öncesinde MODEL oluşturmak gerekli (/ModelOlustur)
- Servise Post Edilecek dosya içinKEY == 'file' olmalıdır.
- .xlsx/.xls uzantılı dosyalardaki verileri Test edebilir.
- 'CINSIYET','SEHIR','SATIS_DURUM','URUN_ADEDI','ARIZA_HIZMET_ADEDI','CAGRI_ADEDI',
  'HIZMET_ADEDI','CRM_ID'
  sütunlarını içeriyor olmalıdır.


# /BireyAnaliz
------------------------
- Kullanım öncesinde MODEL oluşturmak gerekli (/ModelOlustur)
- Servise Post edilecek JSON formatı aşağıdaki gibi olmak zorundadır.
  {
    "Sehir" : "34",
    "Cinsiyet": "0",
    "Urun_adedi" :0 ,
    "Hizmet_adedi":2 ,
    "Ariza_hizmet_adedi":4,
    "Cagri_adedi":0,
    "CustID":"S00002624750"
   }
