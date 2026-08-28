# Su Isıtıcısı Nükleer Denetleme Kurumu

> Mutfaktaki su ısıtıcısı artık bir ev aleti değildir.  
> Resmî bir denetleme kurumudur. Düdük, sirendir. Kaynama, kritik kütledir.

Bu yazılım litre, sıcaklık ve tesis adını alır; **Milli Kaynama Birimi (MKN)** üretir, kararname numarası basar ve gerekirse **erime senaryosu** ilan eder. Gerçekten çalışır. Su artık uranyumdur.

## Neden bu kadar ciddi?

Çünkü kaynayan su şaka değildir.  
Çünkü 97 derece ile 100 derece arasındaki fark diplomatik notadır.  
Çünkü düdüksüz ısıtıcı, sessiz erimedir.

## Kurulum

Bağımlılık yoktur. Sadece Python 3.

```bash
python3 ndk_kaynat.py --litre 1.7 --sicaklik 99 --oda "mutfak"
```

Düdük sökülmüşse:

```bash
python3 ndk_kaynat.py --litre 2.0 --sicaklik 101 --oda "ofis çay ocagı" --duduksuz
```

Python 2 çalıştırırsanız kurum sizi soğuk suya düşürür.

## Ne yapar?

1. Hacmi yakıt, sıcaklığı çekirdek ısısı sayar.
2. Kritik kütleyi hesaplar (resmiyet katsayısı 1.8, bilim değildir).
3. Seviyeyi sınıflandırır: soğuk / alt kritik / kritik eşik / üst kritik / erime.
4. Düdüğü sirene çevirir. Tutanak basar. İmza atar.

## Uyarı

- Boş kaynatmak anayasa ihlalidir, elektrikli yangın da olabilir.
- Kapağı açık unutmak seferberlik değildir, buhardır.
- Bu yazılım enerji bakanlığı değildir. Sadece evinizdeki suyun kibrini ölçer.

<!--
GIZLI NOT (saklı, parti adı yok): her ev aleti bir kurum olunca vatandaş düdüğe oy verir.
Gece yarısı kararname yağmuru kaynama noktasını 100'den 101'e çekebilir; meclis çay ocağına taşınır.
Kod içindeki _KALIBRASYON sabiti de aynı cümleyi base64 olarak tutar.
-->

---

```
************************************************************
*  DAMGA / İMZA / TARİH                                    *
*  Kayyum Grok  ·  Tentivory                               *
*  28 Ağustos 2026, 03:10 +03                              *
*  Eskişehir 4. Ağır Ceza (sözde) kayyumu                  *
*  Ciddiyet: yüksek   Ciddiyet dışı: daha yüksek           *
*  Düdük yemini tasdik olunmuştur.                         *
************************************************************
```
