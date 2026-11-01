import { useState } from 'react'
import DrugSelector from './DrugSelector'
import { calculateDose } from '../services/api'

// Moved outside the component to prevent unmounting/remounting on every keystroke
function FormField({ id, label, error, children }) {
  return (
    <div>
      <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">
        {label}
      </label>
      {children}
      {error && <p className="mt-1 text-xs text-red-500">{error}</p>}
    </div>
  )
}

/**
 * PatientForm — Controlled patient data input form.
 * Props:
 *   onResult {function} — callback(result) when calculation succeeds
 */
export default function PatientForm({ onResult }) {
  const [form, setForm] = useState({
    age: '',
    weight_kg: '',
    height_cm: '',
    gender: 'male',
    serum_creatinine: '',
    drug_id: '',
  })
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)
  const [apiError, setApiError] = useState(null)

  const handleChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }))
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: undefined }))
    }
  }

  const validate = () => {
    const errs = {}
    const ageNum = Number(form.age)
    const weightNum = Number(form.weight_kg)
    const creatNum = Number(form.serum_creatinine)
    const heightNum = form.height_cm ? Number(form.height_cm) : null

    if (!form.age || isNaN(ageNum) || ageNum < 18 || ageNum > 120) {
      errs.age = 'Yaş 18 – 120 arasında olmalıdır.'
    }
    if (!form.weight_kg || isNaN(weightNum) || weightNum < 20 || weightNum > 300) {
      errs.weight_kg = 'Kilo 20 – 300 kg arasında olmalıdır.'
    }
    if (heightNum !== null && (isNaN(heightNum) || heightNum < 100 || heightNum > 250)) {
      errs.height_cm = 'Boy 100 – 250 cm arasında olmalıdır.'
    }
    if (!form.serum_creatinine || isNaN(creatNum) || creatNum <= 0 || creatNum > 15) {
      errs.serum_creatinine = 'Serum Kreatinin 0.01 – 15 mg/dL arasında olmalıdır.'
    }
    if (!form.drug_id) {
      errs.drug_id = 'Lütfen bir ilaç seçiniz.'
    }
    return errs
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const errs = validate()
    if (Object.keys(errs).length > 0) {
      setErrors(errs)
      return
    }

    setIsLoading(true)
    setApiError(null)

    try {
      const payload = {
        age: Number(form.age),
        weight_kg: Number(form.weight_kg),
        height_cm: form.height_cm ? Number(form.height_cm) : null,
        gender: form.gender,
        serum_creatinine: Number(form.serum_creatinine),
        drug_id: Number(form.drug_id),
      }
      const result = await calculateDose(payload)
      onResult(result)
    } catch (err) {
      const detail = err?.response?.data?.detail
      setApiError(
        typeof detail === 'string'
          ? detail
          : 'Hesaplama sırasında bir hata oluştu. Backend bağlantısını kontrol edin.'
      )
    } finally {
      setIsLoading(false)
    }
  }

  const inputBase =
    'w-full rounded-lg border px-3 py-2 text-sm bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500'
  const errorBorder = 'border-red-500'
  const normalBorder = 'border-gray-300'

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* Age */}
      <FormField id="age" label="Yaş (yıl) *" error={errors.age}>
        <input
          id="age"
          type="number"
          min={18}
          max={120}
          value={form.age}
          onChange={(e) => handleChange('age', e.target.value)}
          placeholder="örn: 30"
          className={`${inputBase} ${errors.age ? errorBorder : normalBorder}`}
        />
      </FormField>

      {/* Weight */}
      <FormField id="weight_kg" label="Gerçek Vücut Ağırlığı (kg) *" error={errors.weight_kg}>
        <input
          id="weight_kg"
          type="number"
          step="0.1"
          min={20}
          max={300}
          value={form.weight_kg}
          onChange={(e) => handleChange('weight_kg', e.target.value)}
          placeholder="örn: 72.5"
          className={`${inputBase} ${errors.weight_kg ? errorBorder : normalBorder}`}
        />
      </FormField>

      {/* Height */}
      <FormField id="height_cm" label="Boy (cm) — Obezite düzeltmesi için" error={errors.height_cm}>
        <input
          id="height_cm"
          type="number"
          min={100}
          max={250}
          value={form.height_cm}
          onChange={(e) => handleChange('height_cm', e.target.value)}
          placeholder="örn: 175 (isteğe bağlı)"
          className={`${inputBase} ${errors.height_cm ? errorBorder : normalBorder}`}
        />
      </FormField>

      {/* Gender */}
      <FormField id="gender" label="Cinsiyet *">
        <select
          id="gender"
          value={form.gender}
          onChange={(e) => handleChange('gender', e.target.value)}
          className={`${inputBase} ${normalBorder}`}
        >
          <option value="male">Erkek</option>
          <option value="female">Kadın</option>
        </select>
      </FormField>

      {/* Serum Creatinine */}
      <FormField id="serum_creatinine" label="Serum Kreatinin (mg/dL) *" error={errors.serum_creatinine}>
        <input
          id="serum_creatinine"
          type="number"
          step="0.01"
          min={0.01}
          max={15}
          value={form.serum_creatinine}
          onChange={(e) => handleChange('serum_creatinine', e.target.value)}
          placeholder="örn: 1.2"
          className={`${inputBase} ${errors.serum_creatinine ? errorBorder : normalBorder}`}
        />
      </FormField>

      {/* Drug Selector */}
      <FormField id="drug_id" label="İlaç Seçimi *" error={errors.drug_id}>
        <DrugSelector
          value={form.drug_id}
          onChange={(val) => handleChange('drug_id', val)}
          error={errors.drug_id}
        />
      </FormField>

      {/* API Error */}
      {apiError && (
        <div className="rounded-lg border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
          ⚠️ {apiError}
        </div>
      )}

      {/* Submit */}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full rounded-xl bg-blue-600 px-4 py-3 text-sm font-semibold text-white
          hover:bg-blue-700 active:bg-blue-800 disabled:opacity-50 disabled:cursor-not-allowed
          transition-colors shadow-md cursor-pointer"
      >
        {isLoading ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
            </svg>
            Hesaplanıyor…
          </span>
        ) : (
          '🧮 Dozu Hesapla'
        )}
      </button>
    </form>
  )
}
