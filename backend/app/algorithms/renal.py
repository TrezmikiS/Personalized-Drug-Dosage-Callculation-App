"""Renal and body weight calculation algorithms.

Implements:
- Devine Formula for Ideal Body Weight (IBW)
- Adjusted Body Weight (ABW) for obese individuals
- Cockcroft-Gault Equation for Creatinine Clearance (CrCl) estimation
"""

from typing import Optional, Dict, Any


def calculate_ibw(height_cm: float, gender: str) -> float:
    """Calculates Ideal Body Weight (IBW) in kg using the Devine formula.

    Formula:
      - Male:   50.0 + 2.3 * (height_in_inches - 60)
      - Female: 45.5 + 2.3 * (height_in_inches - 60)

    Args:
        height_cm: Height in centimeters.
        gender: 'male' or 'female'.

    Returns:
        Ideal body weight in kilograms, rounded to 2 decimal places.
    """
    height_inches = height_cm / 2.54
    inches_over_60 = height_inches - 60.0

    gender_normalized = gender.strip().lower()
    if gender_normalized in ["male", "erkek", "m"]:
        base_weight = 50.0
    else:
        base_weight = 45.5

    # Devine formula is linear above and near 60 inches
    ibw = base_weight + (2.3 * inches_over_60)
    # Floor at 30 kg for clinical safety in unusual extreme height inputs
    return round(max(30.0, ibw), 2)


def calculate_abw(actual_weight_kg: float, ibw: float) -> float:
    """Calculates Adjusted Body Weight (ABW) in kg for obese patients.

    Formula:
      ABW = IBW + 0.4 * (actual_weight - IBW)

    Args:
        actual_weight_kg: Total body weight in kg.
        ibw: Ideal body weight in kg.

    Returns:
        Adjusted body weight in kilograms, rounded to 2 decimal places.
    """
    abw = ibw + 0.4 * (actual_weight_kg - ibw)
    return round(abw, 2)


def determine_weight_for_crcl(
    actual_weight_kg: float,
    height_cm: Optional[float],
    gender: str
) -> Dict[str, Any]:
    """Determines the appropriate weight to use in the Cockcroft-Gault equation.

    Clinical Logic:
    - If height is provided, IBW is calculated.
    - If actual_weight > 1.2 * IBW (obese patient): use ABW.
    - If actual_weight < IBW (underweight patient): use actual weight.
    - Otherwise (normal weight range): use actual weight.
    - If height is not provided: default to actual weight.

    Returns:
        Dict containing weight_used_kg, ibw, and weight_type_used ('ACTUAL', 'ABW').
    """
    if height_cm is None or height_cm <= 0:
        return {
            "weight_used_kg": round(actual_weight_kg, 2),
            "ibw": None,
            "weight_type_used": "ACTUAL",
            "is_obese": False
        }

    ibw = calculate_ibw(height_cm, gender)
    is_obese = actual_weight_kg > (1.2 * ibw)

    if is_obese:
        weight_used = calculate_abw(actual_weight_kg, ibw)
        weight_type = "ABW"
    else:
        weight_used = actual_weight_kg
        weight_type = "ACTUAL"

    return {
        "weight_used_kg": round(weight_used, 2),
        "ibw": ibw,
        "weight_type_used": weight_type,
        "is_obese": is_obese
    }


def calculate_cockcroft_gault(
    age: int,
    actual_weight_kg: float,
    serum_creatinine: float,
    gender: str,
    height_cm: Optional[float] = None
) -> Dict[str, Any]:
    """Calculates Creatinine Clearance (CrCl) via Cockcroft-Gault formula.

    Formula:
      CrCl (mL/min) = [ (140 - Age) * Weight(kg) ] / [ 72 * Serum Creatinine (mg/dL) ]
      * If Female: multiply by 0.85

    Args:
        age: Patient age in years (adults >= 18).
        actual_weight_kg: Total body weight in kg.
        serum_creatinine: Serum creatinine in mg/dL (> 0).
        gender: 'male' or 'female'.
        height_cm: Optional height in cm for IBW/ABW correction.

    Returns:
        Dict with calculated_crcl, weight_used_kg, ibw, weight_type_used, and is_female.
    """
    if serum_creatinine <= 0:
        raise ValueError("Serum creatinine must be strictly positive (> 0 mg/dL).")
    if age < 18:
        raise ValueError("Cockcroft-Gault is clinically validated only for adults (>= 18 years).")

    weight_info = determine_weight_for_crcl(actual_weight_kg, height_cm, gender)
    weight_to_use = weight_info["weight_used_kg"]

    # Basic numerator and denominator
    numerator = (140 - age) * weight_to_use
    denominator = 72.0 * serum_creatinine
    raw_crcl = numerator / denominator

    # Gender coefficient
    gender_normalized = gender.strip().lower()
    is_female = gender_normalized in ["female", "kadin", "kadın", "f"]
    if is_female:
        raw_crcl *= 0.85

    crcl_final = round(max(0.0, raw_crcl), 2)

    return {
        "calculated_crcl": crcl_final,
        "weight_used_kg": weight_to_use,
        "ibw": weight_info["ibw"],
        "weight_type_used": weight_info["weight_type_used"],
        "is_obese": weight_info["is_obese"],
        "is_female": is_female
    }
