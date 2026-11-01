"""Dosage adjustment algorithm for Narrow Therapeutic Index (NTI) medications.

Implements clinical dosing guidelines according to renal clearance thresholds (CrCl):
- Vancomycin (Vankomisin)
- Digoxin (Digoksin)
- Lithium (Lityum)
- Generic NTI fallback
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DosageAdjustmentResult:
    calculated_dose_mg: float
    dosing_interval_hours: Optional[int]
    warning_level: str  # "NORMAL", "WARNING", "CRITICAL"
    warning_flag: bool
    warning_message: str


def adjust_dosage(
    drug_name: str,
    standard_dose_mg: float,
    crcl: float,
    weight_kg: float
) -> DosageAdjustmentResult:
    """Calculates adjusted dose, dosing interval, and clinical warning flags.

    Args:
        drug_name: Name of the drug (e.g. 'Vankomisin', 'Digoksin', 'Lityum').
        standard_dose_mg: Standard baseline dose from DB in milligrams.
        crcl: Calculated Creatinine Clearance in mL/min.
        weight_kg: Patient weight used for calculation.

    Returns:
        DosageAdjustmentResult with calculated dose, interval, and risk level.
    """
    drug_lower = drug_name.strip().lower()

    # 1. VANCOMYCIN (Vankomisin)
    if "vankomisin" in drug_lower or "vancomycin" in drug_lower:
        # Standard maintenance: 1000 mg (or ~15-20 mg/kg) every 12 hours
        if crcl >= 50.0:
            return DosageAdjustmentResult(
                calculated_dose_mg=standard_dose_mg,
                dosing_interval_hours=12,
                warning_level="NORMAL",
                warning_flag=False,
                warning_message="Böbrek fonksiyonu yeterli (CrCl >= 50 mL/min). Standart doz (12 saatte bir 1000 mg) uygundur."
            )
        elif 30.0 <= crcl < 50.0:
            return DosageAdjustmentResult(
                calculated_dose_mg=standard_dose_mg,
                dosing_interval_hours=24,
                warning_level="WARNING",
                warning_flag=True,
                warning_message="Hafif-orta derece böbrek yetmezliği (CrCl 30-49 mL/min). Eliminasyon yavaşladığından doz aralığı 24 saate uzatılmıştır. Serum vadi düzeyi (TDM) izlenmelidir."
            )
        elif 10.0 <= crcl < 30.0:
            return DosageAdjustmentResult(
                calculated_dose_mg=round(standard_dose_mg * 0.5, 2),
                dosing_interval_hours=24,
                warning_level="WARNING",
                warning_flag=True,
                warning_message="Orta-ileri derece böbrek yetmezliği (CrCl 10-29 mL/min). Doz %50 azaltılarak 24 saatte bir 500 mg olarak ayarlandı. TDM takibi zorunludur."
            )
        else:  # crcl < 10.0 (Severe renal impairment / Dialysis)
            return DosageAdjustmentResult(
                calculated_dose_mg=0.0,
                dosing_interval_hours=48,
                warning_level="CRITICAL",
                warning_flag=True,
                warning_message="Kritik Uyarı: Son dönem böbrek yetmezliği (CrCl < 10 mL/min)! Standart dozlama kontrendikedir. Nefrotoksisite riski aşırı yüksektir. İlaç bekletilmeli, klinik eczacı konsültasyonu ve kan düzeyi takibiyle bireysel yükleme dozu verilmelidir."
            )

    # 2. DIGOXIN (Digoksin)
    elif "digoksin" in drug_lower or "digoxin" in drug_lower:
        # Standard dose: 0.25 mg daily
        if crcl >= 50.0:
            return DosageAdjustmentResult(
                calculated_dose_mg=standard_dose_mg,
                dosing_interval_hours=24,
                warning_level="NORMAL",
                warning_flag=False,
                warning_message="Böbrek eliminasyonu normal. Standart günlük idame dozu (0.25 mg/gün) uygundur."
            )
        elif 10.0 <= crcl < 50.0:
            # 50% dose reduction
            reduced_dose = round(standard_dose_mg * 0.5, 4)
            return DosageAdjustmentResult(
                calculated_dose_mg=reduced_dose,
                dosing_interval_hours=24,
                warning_level="WARNING",
                warning_flag=True,
                warning_message="Orta derece böbrek yetmezliği. Toksisite (aritmi, görme bozukluğu) riskini engellemek için doz %50 azaltıldı (0.125 mg/gün)."
            )
        else:  # crcl < 10.0
            critical_dose = round(standard_dose_mg * 0.25, 4)
            return DosageAdjustmentResult(
                calculated_dose_mg=critical_dose,
                dosing_interval_hours=48,
                warning_level="CRITICAL",
                warning_flag=True,
                warning_message="Kritik Uyarı: Şiddetli böbrek yetmezliği (CrCl < 10 mL/min)! Digoksin birikimi ve ölümcül kardiyotoksisite riski. Gün aşırı 0.0625 mg önerilir, serum elektrolitleri (K, Mg) ve EKG sıkı izlenmelidir."
            )

    # 3. LITHIUM (Lityum)
    elif "lityum" in drug_lower or "lithium" in drug_lower:
        # Standard dose: 300 mg (often BID)
        if crcl >= 50.0:
            return DosageAdjustmentResult(
                calculated_dose_mg=standard_dose_mg,
                dosing_interval_hours=12,
                warning_level="NORMAL",
                warning_flag=False,
                warning_message="Böbrek fonksiyonu yeterli. Standart dozlama protokolü uygundur."
            )
        elif 10.0 <= crcl < 50.0:
            reduced_dose = round(standard_dose_mg * 0.5, 2)
            return DosageAdjustmentResult(
                calculated_dose_mg=reduced_dose,
                dosing_interval_hours=24,
                warning_level="WARNING",
                warning_flag=True,
                warning_message="Böbrek klerensi belirgin azalmış. Lityum %95 böbrekten atıldığı için intoksikasyon riski mevcuttur. Doz %50 azaltıldı (150 mg/gün) ve serum lityum takibi gereklidir."
            )
        else:  # crcl < 10.0
            return DosageAdjustmentResult(
                calculated_dose_mg=0.0,
                dosing_interval_hours=None,
                warning_level="CRITICAL",
                warning_flag=True,
                warning_message="Kritik Alarm: Son dönem böbrek yetmezliğinde Lityum KONTRENDİKEDİR! Şiddetli nörotoksisite ve kalıcı hasar riski nedeniyle tedavi durdurulmalı ve alternatif psikotrop ajanlar düşünülmelidir."
            )

    # 4. GENERIC / FALLBACK FOR OTHER NTI DRUGS
    else:
        if crcl >= 50.0:
            return DosageAdjustmentResult(
                calculated_dose_mg=standard_dose_mg,
                dosing_interval_hours=24,
                warning_level="NORMAL",
                warning_flag=False,
                warning_message="Renal fonksiyon normal sınırlarda. Standart etiket dozu uygundur."
            )
        elif 10.0 <= crcl < 50.0:
            return DosageAdjustmentResult(
                calculated_dose_mg=round(standard_dose_mg * 0.5, 2),
                dosing_interval_hours=24,
                warning_level="WARNING",
                warning_flag=True,
                warning_message="Böbrek klerensi kısıtlı. Standart doz %50 azaltılarak uygulanmalıdır."
            )
        else:
            return DosageAdjustmentResult(
                calculated_dose_mg=0.0,
                dosing_interval_hours=None,
                warning_level="CRITICAL",
                warning_flag=True,
                warning_message="Ağır renal yetmezlik (CrCl < 10 mL/min). Standart dozlama önerilmez, nefrolog konsültasyonu gereklidir."
            )
