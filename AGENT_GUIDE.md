# Personalised Drug Dosage Calculation App - Technical Execution & Architecture Plan

## 🕸️ AGENT_GUIDE.md — Ana Proje Mimari, Uygulama ve Hafıza Kılavuzu

> **⚠️ AJAN TALİMATI — HER YENİ SOHBETTE BU DOSYAYI OKU!**
>
> Bu dosya, projenin tüm teknik bağlamını, mimari kararlarını, faz durumlarını ve geçmiş sohbet günlüğünü içerir.
>
> Kullanıcı `/basla`, `/planla`, `/kontrol` veya `/bitir` yazdığında aşağıdaki [10. Ajan Komutları Workflow](#10-ajan-komutları-workflow) bölümüne göre hareket et.
>
> 🛑 **KESİN İŞ AKIŞI KURALI (STRICT 4-STEP PIPELINE — FLASH VE TÜM MODELLER İÇİN):**
>
> `/basla` dendiğinde **KESİNLİKLE KOD YAZMA** ve fazı tek seferde bitirme!
>
> Her faz zorunlu olarak 4 ayrı kullanıcı turunda ilerlemelidir:
>
> 1. **`/basla`**: Sadece git ve faz durumunu kontrol et, branch ayarla, kullanıcıya rapor ver. **KOD YAZMA!** Kullanıcıyı `/planla` yapmaya davet et.
>
> 2. **`/planla`**: Fazda yazılacak sınıfları, metotları ve dosyaları listele. **KULLANICIDAN AÇIK ONAY BEKLE.** Onay gelmeden ASLA kod yazma!
>
> 3. **Kodlama**: Yalnızca plan onayı alındıktan sonra kodları oluştur/düzenle.
>
> 4. **`/kontrol`**: Derleme (`msbuild` / test) ve checklist denetimini yap, kullanıcıya raporla.
>
> 5. **`/bitir`**: Durum tablosunu ve Session Log'u güncelle, git commit/merge komutlarını ver.

## 1. Project Overview & Team Structure

* **Project Title:** Personalised Drug Dosage Calculation App

* **Engineering Team:** Ceyhun Mehmet Keklik, Hamza Karayiğit (Computer Engineering)

* **Multidisciplinary Lead:** Ahsen Özateş (Pharmacy)

## 2. Ekip Görev ve Durum Takip Tablosu (Task & Status Matrix)

| Görev / Modül | Sorumlu | Disiplin | Durum | Faz | 
| ----- | ----- | ----- | ----- | ----- | 
| Klinik Formüller & Terapötik Aralık Seçimi | Ceyhun M. Keklik | Eczacılık | ✅ Tamamlandı | Faz 1 | 
| PostgreSQL Veri Tabanı Şeması & Kurulumu | Ceyhun M. Keklik | Bilgisayar Mühendisliği | ✅ Tamamlandı | Faz 1 | 
* **2026-11-01 (Faz 2):** Hamza ile Faz 2 başarıyla tamamlandı. Cockcroft-Gault eşitliği, Devine IBW ve obez hastalar için ABW algoritmaları (`algorithms/renal.py`), dar terapötik aralıklı ilaçlar (Vankomisin, Digoksin, Lityum) için doz ve aralık uyarlama motoru (`algorithms/dosage.py`), Pydantic v2 veri doğrulama şemaları (`schemas/dosage_schema.py`), POST /api/calculate ve GET /api/drugs rotaları ile audit logging sistemi geliştirildi. 16 klinik sanal hasta profili ve uç değer testleri (`backend/tests/test_phase2.py`) dahil 34/34 test (%100) başarıyla doğrulandı.
* **2026-11-01 (Faz 2):** Hamza ile Faz 2 başarıyla tamamlandı. Cockcroft-Gault eşitliği, Devine IBW ve obez hastalar için ABW algoritmaları (`algorithms/renal.py`), dar terapötik aralıklı ilaçlar (Vankomisin, Digoksin, Lityum) için doz ve aralık uyarlama motoru (`algorithms/dosage.py`), Pydantic v2 veri doğrulama şemaları (`schemas/dosage_schema.py`), POST /api/calculate ve GET /api/drugs rotaları ile audit logging sistemi geliştirildi. 16 klinik sanal hasta profili ve uç değer testleri (`backend/tests/test_phase2.py`) dahil 34/34 test (%100) başarıyla doğrulandı.
* **2026-11-01 (Faz 2):** Hamza ile Faz 2 başarıyla tamamlandı. Cockcroft-Gault eşitliği, Devine IBW ve obez hastalar için ABW algoritmaları (`algorithms/renal.py`), dar terapötik aralıklı ilaçlar (Vankomisin, Digoksin, Lityum) için doz ve aralık uyarlama motoru (`algorithms/dosage.py`), Pydantic v2 veri doğrulama şemaları (`schemas/dosage_schema.py`), POST /api/calculate ve GET /api/drugs rotaları ile audit logging sistemi geliştirildi. 16 klinik sanal hasta profili ve uç değer testleri (`backend/tests/test_phase2.py`) dahil 34/34 test (%100) başarıyla doğrulandı.
* **2026-11-01 (Faz 2):** Hamza ile Faz 2 başarıyla tamamlandı. Cockcroft-Gault eşitliği, Devine IBW ve obez hastalar için ABW algoritmaları (`algorithms/renal.py`), dar terapötik aralıklı ilaçlar (Vankomisin, Digoksin, Lityum) için doz ve aralık uyarlama motoru (`algorithms/dosage.py`), Pydantic v2 veri doğrulama şemaları (`schemas/dosage_schema.py`), POST /api/calculate ve GET /api/drugs rotaları ile audit logging sistemi geliştirildi. 16 klinik sanal hasta profili ve uç değer testleri (`backend/tests/test_phase2.py`) dahil 34/34 test (%100) başarıyla doğrulandı.
| React UI Form Tasarımları & Tailwind Stil | Ceyhun M. Keklik | Bilgisayar Mühendisliği | ⏳ Beklemede | Faz 3 | 
| API Entegrasyonu & Dynamic Alert Badges | Ceyhun M. Keklik | Bilgisayar Mühendisliği | ⏳ Beklemede | Faz 3 | 
| Klinik Uyarı Metinleri & UI Yönergeleri | Ceyhun M. Keklik | Eczacılık | ⏳ Beklemede | Faz 3 | 
| Klinik Validasyon & Doz Doğrulama Testleri | Ceyhun M. Keklik | Eczacılık | ⏳ Beklemede | Faz 3 | 
| Teknik Rapor & Dokümantasyon Hazırlığı | Tüm Ekip | Ortak | ⏳ Beklemede | Faz 4 | 

## 3. Tech Stack Definition

| Component | Technology | Rationale / Purpose | 
| ----- | ----- | ----- | 
| **Frontend** | React.js (Vite) + Tailwind CSS | Fast, responsive UI for clinical settings (tablets, mobile, desktop). | 
| **Backend** | Python (FastAPI) | High-performance calculation engine, automatic OpenAPI docs, native math handling. | 
| **Database** | PostgreSQL | Relational, ACID-compliant database to safely store drug parameters & calculation logs. | 
| **Validation/Schemas** | Pydantic (Python) | Strict input verification (e.g., ensuring physiological values fall in valid ranges). | 
| **Version Control** | Git & GitHub | Distributed version control and collaboration platform. | 

## 4. Detailed Software Architecture & Folder Structure

```
dosage-app/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── database.py          # SQLAlchemy PostgreSQL connection setup
│   │   ├── models/              # Database entities (SQLAlchemy models)
│   │   │   ├── drug.py
│   │   │   └── calculation_log.py
│   │   ├── schemas/             # Request & Response schemas (Pydantic models)
│   │   │   └── dosage_schema.py
│   │   ├── algorithms/          # Pharmacokinetic math logic
│   │   │   ├── renal.py         # Cockcroft-Gault & eGFR formulas
│   │   │   └── dosage.py        # Narrow Therapeutic Index drug formulas
│   │   └── api/                 # API endpoints / routes
│   │       ├── drugs.py
│   │       └── calculate.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/          # Reusable UI components (Inputs, Modals, Alert Cards)
    │   ├── views/               # Pages (Calculator Page, Log History, Drug Info)
    │   ├── services/            # Axios API call services
    │   └── App.jsx
    ├── package.json
    └── tailwind.config.js

```

## 5. Coding & Algorithm Specifications

### A. Pharmacokinetic Formulas to Implement

1. **Creatinine Clearance (**$CrCl$**) via Cockcroft-Gault Equation:**

   $$
   CrCl = \frac{(140 - \text{Age}) \times \text{Weight (kg)}}{72 \times \text{Serum Creatinine (mg/dL)}} \times (0.85 \text{ if Female})
   $$

2. **Adjusted Body Weight (**$ABW$**) for Obese Patients:**

   $$
   IBW (\text{Male}) = 50 + 2.3 \times (\text{Height in inches} - 60)
   $$

   $$
   IBW (\text{Female}) = 45.5 + 2.3 \times (\text{Height in inches} - 60)
   $$

   $$
   ABW = IBW + 0.4 \times (\text{Actual Weight} - IBW)
   $$

3. **Vancomycin / Digoxin Dose Adjustments:**

   * If $CrCl < 50 \text{ mL/min}$: Extend dosing interval or reduce maintenance dose by $50\%$.

   * If $CrCl < 10 \text{ mL/min}$: Trigger high-risk toxicity warning and recommend specialized clinical pharmacy consult.

## 6. PostgreSQL Database Schema

```
-- Table: Drugs (Narrow Therapeutic Index Medications)
CREATE TABLE drugs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    active_ingredient VARCHAR(100) NOT NULL,
    standard_dose_mg NUMERIC(8, 2) NOT NULL,
    therapeutic_range_min NUMERIC(8, 2) NOT NULL,
    therapeutic_range_max NUMERIC(8, 2) NOT NULL,
    renal_clearance_flag BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Calculation Logs (Audit Trail for Clinical Safety)
CREATE TABLE calculation_logs (
    id SERIAL PRIMARY KEY,
    patient_age INT NOT NULL,
    patient_weight_kg NUMERIC(5, 2) NOT NULL,
    patient_gender VARCHAR(10) NOT NULL,
    serum_creatinine NUMERIC(4, 2) NOT NULL,
    calculated_crcl NUMERIC(6, 2) NOT NULL,
    drug_id INT REFERENCES drugs(id),
    calculated_dose_mg NUMERIC(8, 2) NOT NULL,
    warning_flag BOOLEAN DEFAULT FALSE,
    warning_message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```

## 7. Faz Geliştirme Detayları ve Adım Adım Yapılacaklar (Detailed Phase Breakdown)

Projeyi 4 temel faza ayırdık. Her faz, **Strict 4-Step Pipeline (`/basla` ➔ `/planla` ➔ Kodlama ➔ `/kontrol` ➔ `/bitir`)** mantığıyla yürütülür.

### 🔹 FAZ 1: Altyapı, Veri Tabanı Mimarisi ve Tıbbi Çerçeve (Weeks 1-2)

**Odak Noktası:** Projenin omurgasını kurmak, veri tabanını ayağa kaldırmak ve eczacılık formüllerini dokümante etmek.

* **1. Step 1 (`/basla`):** `feature/phase1-setup` branch'i açılır. Ortam kontrolleri yapılır.

* **2. Step 2 (`/planla`):** `backend/app/database.py` ve `models/` dizinindeki SQLAlchemy ORM sınıflarının planı sunulur. Seçilen dar terapötik ilaçların (Vankomisin, Digoksin, Lityum vb.) ve kullanılan formüllerin tıbbi referans dokümanı planlanır.

* **3. Step 3 (Kodlama/Uygulama):**

  * PostgreSQL veritabanı kurulur ve `drugs` ile `calculation_logs` tabloları oluşturulur.

  * FastAPI projesi (`main.py`) başlatılır ve DB bağlantı testi yapılır.

  * `requirements.txt` (FastAPI, SQLAlchemy, psycopg2, pydantic) netleştirilir.

* **4. Step 4 (`/kontrol`):** Veritabanı bağlantısı ve tablo oluşturma migration testleri yapılır.

* **5. Step 5 (`/bitir`):** Faz 1 tamamlandı olarak işaretlenir ve `main` branch'ine merge edilir.

### 🔹 FAZ 2: Çekirdek Backend, Algoritmalar ve Veri Doğrulama (Weeks 3-5)

**Odak Noktası:** Hesaplama motorunu yazmak, Pydantic şemaları ile hatalı veri girişini engellemek ve API uç noktalarını (REST endpoints) yayınlamak.

* **1. Step 1 (`/basla`):** `feature/phase2-backend-algos` branch'i açılır.

* **2. Step 2 (`/planla`):**`algorithms/renal.py` (Cockcroft-Gault, ABW/IBW) ve `algorithms/dosage.py` matematiksel fonksiyonlarının planı sunulur. `schemas/dosage_schema.py` Pydantic model yapısı açıklanır. `api/drugs.py` ve `api/calculate.py` endpoint rotalarının planı sunulur. Algoritmanın doğrulanması için hazırlanacak 15-20 adet "Sanal Hasta Senaryosu" planlanır.

* **3. Step 3 (Kodlama/Uygulama):**

  * Cockcroft-Gault formülü Python fonksiyonlarına dönüştürülür.

  * Yaş (<0 veya >120), Serum Kreatinin (<=0) gibi hatalı verileri engelleyen Pydantic validation mantığı yazılır.

  * POST `/api/calculate` endpoint'i yazılır; hasta verilerini alıp $CrCl$ ve doz hesaplayarak veritabanına log atar.

* **4. Step 4 (`/kontrol`):** PyTest veya Swagger UI üzerinden Sanal Hasta Profilleri ile uç değer (Edge-case) testleri yapılır.

* **5. Step 5 (`/bitir`):** Faz 2 tamamlandı olarak işaretlenir.

### 🔹 FAZ 3: Frontend Geliştirme, Dynamic Alerts & Entegrasyon (Weeks 6-7)

**Odak Noktası:** Kullanıcı dostu klinik web arayüzünü (React + Tailwind) oluşturmak ve Backend API ile entegre etmek.

* **1. Step 1 (`/basla`):** `feature/phase3-frontend-ui` branch'i açılır.

* **2. Step 2 (`/planla`):**Patient Input Form, Drug Selector Dropdown ve Calculation Result Card bileşenlerinin planı sunulur.Axios API istemci katmanı (`services/api.js`) ve Doz Aşımı / Böbrek Yetmezliği için dinamik renkli uyarı kartlarının (Alert Badges) planı sunulur. Kırmızı/Sarı tıbbi uyarı metinlerinin ve öneri mesajlarının taslağı verilir.

* **3. Step 3 (Kodlama/Uygulama):**

  * React Vite projesi kurulur, Tailwind CSS eklenir.

  * Form alanları yazılır: Yaş, Kilo, Boy, Cinsiyet, Serum Kreatinin, İlaç Seçimi.

  * Hesapla butonuna basıldığında FastAPI'ye istek atılır ve dönen $CrCl$ + Doz miktarı ekranda gösterilir.

  * $CrCl < 50$ ise Sarı Uyarı, $CrCl < 10$ veya Doz Aşımı varsa Kırmızı Kritik Uyarı kartı render edilir.

* **4. Step 4 (`/kontrol`):** UI/UX responsive kontrolleri ve E2E (End-to-End) arayüz-backend entegrasyon testleri yapılır.

* **5. Step 5 (`/bitir`):** Faz 3 tamamlandı olarak işaretlenir.

### 🔹 FAZ 4: Klinik Validasyon, Hata Ayıklama ve Dokümantasyon (Week 8)

**Odak Noktası:** Yazılımın klinik doğruluğunu tescillemek, sınır değer hatalarını kapatmak ve teknik raporu teslim etmektir.

* **1. Step 1 (`/basla`):** `feature/phase4-validation-report` branch'i açılır.

* **2. Step 2 (`/planla`):** Manuel klinik hesaplamalar ile sistem çıktılarının çapraz doğrulama tablosu planlanır.  Sistem mimari diyagramı, veritabanı şeması açıklaması ve API dokümantasyon planı sunulur.

* **3. Step 3 (Kodlama/Dokümantasyon):**

  * Eczacı tarafından bulunan uyuşmazlıklar veya yazılımsal bug'lar düzeltilir.

  * FE401 Final Raporu ve Kullanıcı Kılavuzu (User Manual) kaleme alınır.

* **4. Step 4 (`/kontrol`):** Tüm projenin ve final raporunun son kontrolü gerçekleştirilir.

* **5. Step 5 (`/bitir`):** Proje tamamlandı (`Status: COMPLETED`) olarak işaretlenir ve teslim edilir.

## 8. Task Division & Detailed Responsibilities

### **Ceyhun Mehmet Keklik (Computer Engineering)**

1. PostgreSQL Veri Tabanı mimarisi ve SQLAlchemy bağlantı yapılandırması.

2. FastAPI ana uygulama (`main.py`) ve API rota (route) mimarisinin kurulması.

3. React arayüz form bileşenlerinin (UI Forms) tasarlanması ve Tailwind CSS stil entegrasyonu.

### **Hamza Karayiğit (Computer Engineering)**

1. Cockcroft-Gault ve dozaj ayarlama matematiksel fonksiyonlarının yazılması (`algorithms/`).

2. Pydantic şemalarının yazılması ve sınır değer (edge-case) input doğrulamaları.

3. React-FastAPI arasındaki Axios API istemci entegrasyonu ve dinamik durum rozetleri (Alert Badges).

### **Ahsen Özateş (Pharmacy Member - Clinical Domain Lead)**

1. Terapötik aralığı dar ilaç listesinin ve klinik referans formüllerinin tanımlanması.

2. Yazılım doğrulaması için 15-20 adet "Sanal Hasta Profili" (Dummy Data) oluşturulması.

3. Çıkan doz sonuçlarının manuel hesaplamalarla karşılaştırılarak klinik olarak onaylanması.

4. Riskli durumlarda (böbrek yetmezliği, aşırı doz) ekranda çıkacak tıbbi uyarı metinlerinin hazırlanması.

## 9. Session Log (Geçmiş Sohbet Günlüğü)

* **2026-11-01:** Proje planı, teknoloji seçimi, ekip görev dağılım matrisi ve `AGENT_GUIDE.md` iş akışı kuralları dokümana işlendi.

* **2026-11-01:** Detaylı Faz Açıklamaları (Faz 1-4 step-by-step kılavuzu) dokümana entegre edildi. Proje başlangıç durumuna getirildi.

* **2026-11-01 (Faz 1):** Ceyhun ile Faz 1 başarıyla tamamlandı. PostgreSQL/SQLAlchemy ORM modelleri (`drugs`, `calculation_logs`), FastAPI temel mimarisi, DB health check ve initial seed endpoint'leri oluşturuldu. Klinik referans dokümanı (`docs/clinical_reference.md`) hazırlandı. Testler (%100) doğrulandı.

* **2026-11-01 (Faz 2):** Hamza ile Faz 2 başarıyla tamamlandı. Cockcroft-Gault eşitliği, Devine IBW ve obez hastalar için ABW algoritmaları (`algorithms/renal.py`), dar terapötik aralıklı ilaçlar (Vankomisin, Digoksin, Lityum) için doz ve aralık uyarlama motoru (`algorithms/dosage.py`), Pydantic v2 veri doğrulama şemaları (`schemas/dosage_schema.py`), POST /api/calculate ve GET /api/drugs rotaları ile audit logging sistemi geliştirildi. 16 klinik sanal hasta profili ve uç değer testleri (`backend/tests/test_phase2.py`) dahil 34/34 test (%100) başarıyla doğrulandı.

## 10. Ajan Komutları Workflow

Kullanıcı sohbet içerisinde aşağıdaki komutları verdiğinde ilgili adımları kesinlikle sırasıyla uygula:

* **`/basla`**: Bulunduğun fazı belirle, ilgili git branch adını öner, kod yazmadan kullanıcının durumunu ve hedefini onayla. Kullanıcıyı `/planla` komutunu vermeye davet et.

* **`/planla`**: İlgili fazda yapılacak sınıfları, metodları, dosyaları ve mantığı madde madde sırala. Kullanıcıdan açık onay bekle!

* **`/kontrol`**: Kodlanan dosyaların doğruluğunu, syntax kontrolünü ve ekip görev tablosundaki karşılığını denetle, kullanıcıya rapor ver.

* **`/bitir`**: İlgili fazın durumunu `✅ Tamamlandı` olarak güncelle, Session Log'a kayıt düş ve git commit/merge talimatlarını kullanıcıya ilet.