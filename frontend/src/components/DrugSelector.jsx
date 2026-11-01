import { useEffect, useState } from 'react'
import { getDrugs } from '../services/api'

/**
 * DrugSelector — Fetches drug list from backend and renders a select dropdown.
 * Props:
 *   value    {number|string} — currently selected drug_id
 *   onChange {function}     — callback(drug_id) on selection change
 *   error    {string}       — optional validation error message
 */
export default function DrugSelector({ value, onChange, error }) {
  const [drugs, setDrugs] = useState([])
  const [loading, setLoading] = useState(true)
  const [fetchError, setFetchError] = useState(null)

  useEffect(() => {
    getDrugs()
      .then((data) => setDrugs(data))
      .catch(() => setFetchError('İlaç listesi yüklenemedi. Backend bağlantısını kontrol edin.'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="text-sm text-gray-400 italic animate-pulse">
        İlaç listesi yükleniyor…
      </div>
    )
  }

  if (fetchError) {
    return <p className="text-sm text-red-500">{fetchError}</p>
  }

  return (
    <div>
      <select
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className={`w-full rounded-lg border px-3 py-2 text-sm bg-white shadow-sm
          focus:outline-none focus:ring-2 focus:ring-blue-500
          ${error ? 'border-red-500' : 'border-gray-300'}`}
      >
        <option value="">— İlaç Seçiniz —</option>
        {drugs.map((drug) => (
          <option key={drug.id} value={drug.id}>
            {drug.name} ({drug.active_ingredient})
          </option>
        ))}
      </select>
      {error && <p className="mt-1 text-xs text-red-500">{error}</p>}
    </div>
  )
}
