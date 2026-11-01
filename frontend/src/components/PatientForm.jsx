import { useState } from 'react'
import DrugSelector from './DrugSelector'
import { calculateDose } from '../services/api'

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
    setErrors((prev) => ({ ...prev, [field]: undefined }))
  }

  const validate = () => {
    const errs = {}
    if (!form.age || form.age < 18 || form.age > 120)
      errs.age = 'Yaş 18 – 120 arasında olmalıdır.'
    if (!form.weight_kg || form.weight_kg < 20 || form.weight_kg > 300)
      errs.weight_kg = 'Kilo 20 – 300 kg arasında olmalıdır.'
    if (form.height_cm && (form.height_cm < 100 || form.height_cm > 250))
      errs.height_cm = 'Boy 100 – 250 cm arasında olmalıdır.'
    if (!form.serum_creatinine || form.serum_creatinine <= 0 || form.serum_creatinine > 15)
      errs.serum_creatinine = 'Serum Kreatinin 0 – 15 mg/dL arasında olmalıdır.'
    if (!form.drug_id) errs.drug_id = 'Lütfen bir ilaç seçiniz.'
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

  const Field = ({ id, label, children }) => (
    <div>
      <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">
        {label}
      </label>
      {children}
      {errors[id] && <p className="mt-1 text-xs text-red-500">{errors[id]}</p>}
    </div>
  )

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* Age */}
      <Field id="age" label="Yaş (yıl) *">
        <input
          id="age"
          type="number"
          min={18}
          max={120}
          value={form.age}
          onChange={(e) => handleChange('age', e.target.value)}
          placeholder="örn: 65"
          className={`${inputBase} ${errors.age ? errorBorder : normalBorder}`}
        />
      </Field>

      {/* Weight */}
      <Field id="weight_kg" label="Gerçek Vücut Ağırlığı (kg) *">
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
      </Field>

      {/* Height */}
      <Field id="height_cm" label="Boy (cm) — Obezite düzeltmesi için">
        <input
          id="height_cm"
          type="number"
          min={100}
          max={250}
          value={form.height_cm}
          onChange={(e) => handleChange('height_cm', e.target.value)}
          placeholder="örn: 170 (isteğe bağlı)"
          className={`${inputBase} ${errors.height_cm ? errorBorder : normalBorder}`}
        />
      </Field>

      {/* Gender */}
      <Field id="gender" label="Cinsiyet *">
        <select
          id="gender"
          value={form.gender}
          onChange={(e) => handleChange('gender', e.target.value)}
          className={`${inputBase} ${normalBorder}`}
        >
          <option value="male">Erkek</option>
          <option value="female">Kadın</option>
        </select>
      </Field>

      {/* Serum Creatinine */}
      <Field id="serum_creatinine" label="Serum Kreatinin (mg/dL) *">
        <input
          id="serum_creatinine"
          type="number"
          step="0.01"
          min={0.01}
          max={15}
          value={form.serum_creatinine}
          onChange={(e) => handleChange('serum_creatinine', e.target.value)}
          placeholder="örn: 1.4"
          className={`${inputBase} ${errors.serum_creatinine ? errorBorder : normalBorder}`}
        />
      </Field>

      {/* Drug Selector */}
      <Field id="drug_id" label="İlaç Seçimi *">
        <DrugSelector
          value={form.drug_id}
          onChange={(val) => handleChange('drug_id', val)}
          error={errors.drug_id}
        />
      </Field>

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
          transition-colors shadow-md"
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
