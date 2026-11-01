import { useEffect, useState, useCallback } from 'react'
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

  const loadDrugs = useCallback(async (isRetry = false) => {
    if (!isRetry) setLoading(true)
    setFetchError(null)

    try {
      const data = await getDrugs()
      setDrugs(data)
      setFetchError(null)
    } catch (err) {
      console.error('Failed to fetch drugs:', err)
      setFetchError('İlaç listesi yüklenemedi. Backend bağlantısını kontrol edin.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadDrugs()

    // Automatic silent retry after 2 seconds if first attempt failed while backend starts
    const timer = setTimeout(() => {
      setDrugs((current) => {
        if (current.length === 0) {
          loadDrugs(true)
        }
        return current
      })
    }, 2000)

    return () => clearTimeout(timer)
  }, [loadDrugs])

  if (loading) {
    return (
      <div className="flex items-center gap-2 text-sm text-gray-400 italic py-2 animate-pulse">
        <svg className="h-4 w-4 animate-spin text-blue-500" viewBox="0 0 24 24" fill="none">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
        </svg>
        İlaç listesi yükleniyor…
      </div>
    )
  }

  if (fetchError && drugs.length === 0) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm">
        <p className="text-red-700 font-medium">{fetchError}</p>
        <button
          type="button"
          onClick={() => loadDrugs()}
          className="mt-2 inline-flex items-center gap-1 rounded bg-red-100 px-2.5 py-1 text-xs font-semibold text-red-800 hover:bg-red-200 transition-colors cursor-pointer"
        >
          🔄 Tekrar Dene
        </button>
      </div>
    )
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
            {drug.name} ({drug.active_ingredient}) — Standart Doz: {drug.standard_dose_mg} mg
          </option>
        ))}
      </select>
      {error && <p className="mt-1 text-xs text-red-500">{error}</p>}
    </div>
  )
}
