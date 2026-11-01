# Klinik ve Tıbbi Referans Dokümanı (Clinical Reference Guide)

## 1. Giriş ve Amaç
Bu doküman, Ahsen Özateş (Eczacılık / Klinik Alan Lideri) koordinasyonunda hazırlanmış olup, kişiselleştirilmiş ilaç dozu hesaplama sisteminde kullanılan farmakokinetik formülleri, terapötik aralığı dar ilaçları ve böbrek fonksiyonuna dayalı doz ayarlama protokollerini içerir.

---

## 2. Farmakokinetik Formüller

### A. Kreatinin Klerensi ($CrCl$) - Cockcroft-Gault Eşitliği
Böbrek glomerüler filtrasyon oranının klinik pratikteki en yaygın tahmin yöntemi:

$$CrCl = \frac{(140 - \text{Yaş}) \times \text{Ağırlık (kg)}}{72 \times \text{Serum Kreatinin (mg/dL)}} \times (0.85 \text{ kadın hastalar için})$$

* **Birim:** $\text{mL/min}$
* **Geçerlilik Koşulları:** Yetişkin hastalar ($\ge 18$ yaş), kararlı serum kreatinin düzeyi.

### B. İdeal Vücut Ağırlığı ($IBW$ - Devine Formülü)
* **Erkek:**
  $$IBW = 50 + 2.3 \times (\text{Boy (inç)} - 60)$$
* **Kadın:**
  $$IBW = 45.5 + 2.3 \times (\text{Boy (inç)} - 60)$$

> *Not:* $1 \text{ inç} = 2.54 \text{ cm}$.

### C. Düzeltilmiş Vücut Ağırlığı ($ABW$) - Obez Hastalar İçin
Hastanın Gerçek Ağırlığı ($TBW$), İdeal Ağırlığının ($IBW$) $\%120$'sini aşıyorsa Cockcroft-Gault formülünde $ABW$ kullanılır:

$$ABW = IBW + 0.4 \times (TBW - IBW)$$

---

## 3. Terapötik Aralığı Dar İlaçlar (NTI Drugs)

| İlaç Adı | Etken Madde | Standart Doz | Hedef Terapötik Aralık | Renal Eliminasyon | Kritik $CrCl$ Eşiği |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Vankomisin** | Vancomycin HCl | $1000\text{ mg}$ ($15-20\text{ mg/kg}$) | $10.0 - 20.0\text{ mg/L}$ (Vadi) | $\%80-90$ renal | $< 50\text{ mL/min}$ |
| **Digoksin** | Digoxin | $0.25\text{ mg/gün}$ | $0.8 - 2.0\text{ ng/mL}$ | $\%70-80$ renal | $< 50\text{ mL/min}$ |
| **Lityum** | Lithium Carbonate | $300\text{ mg}$ | $0.6 - 1.2\text{ mEq/L}$ | $\%95$ renal | $< 50\text{ mL/min}$ |

---

## 4. Böbrek Fonksiyonuna Göre Klinik Karar Destek Eşikleri

* **$CrCl \ge 50\text{ mL/min}$ (Normal / Hafif Kısıtlı):**
  * Standart dozlama aralığı ve standart idame dozu uygulanır.
  * Durum: 🟢 Normal
* **$10\text{ mL/min} \le CrCl < 50\text{ mL/min}$ (Orta-İleri Derece Böbrek Yetmezliği):**
  * Doz aralığı uzatılır (örn. 12 saatten 24-48 saate) veya doz miktarı $\%50$ azaltılır.
  * Durum: 🟡 Sarı Uyarı (Doz Düzeltmesi Gerekli)
* **$CrCl < 10\text{ mL/min}$ veya Diyaliz (Son Dönem Böbrek Yetmezliği):**
  * Yüksek nefrotoksisite / kardiyotoksisite riski.
  * Standart dozlama durdurulur, serum ilaç düzeyi izlemi (TDM) ve klinik eczacı konsültasyonu zorunludur.
  * Durum: 🔴 Kırmızı Kritik Alarm (Yüksek Risk)
