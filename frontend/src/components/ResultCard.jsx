import AlertBadge from './AlertBadge'

/**
 * ResultCard — Displays the pharmacokinetic calculation output.
 *
 * Props:
 *   result {Object} — API response from POST /api/calculate
 */
export default function ResultCard({ result }) {
  if (!result) return null

  const {
    calculated_crcl,
    calculated_dose_mg,
    warning_flag,
    warning_message,
    drug_name,
    renal_category,
  } = result

  return (
    <div className="rounded-2xl border border-gray-200 bg-white shadow-lg p-6 space-y-5">
      {/* Header */}
      <div className="flex items-center gap-2 border-b border-gray-100 pb-3">
        <span className="text-xl">💊</span>
        <h2 className="text-lg font-bold text-gray-800">Hesaplama Sonucu</h2>
      </div>

      {/* Core Metrics */}
      <div className="grid grid-cols-2 gap-4">
        {/* CrCl */}
        <div className="rounded-xl bg-blue-50 border border-blue-100 p-4 text-center">
          <p className="text-xs font-semibold text-blue-500 uppercase tracking-wider">
            Kreatinin Klerensi (CrCl)
          </p>
          <p className="mt-1 text-3xl font-bold text-blue-700">
            {Number(calculated_crcl).toFixed(1)}
          </p>
          <p className="text-xs text-blue-400">mL/min</p>
        </div>

        {/* Calculated Dose */}
        <div className="rounded-xl bg-indigo-50 border border-indigo-100 p-4 text-center">
          <p className="text-xs font-semibold text-indigo-500 uppercase tracking-wider">
            Önerilen Doz
          </p>
          <p className="mt-1 text-3xl font-bold text-indigo-700">
            {Number(calculated_dose_mg).toFixed(2)}
          </p>
          <p className="text-xs text-indigo-400">mg</p>
        </div>
      </div>

      {/* Drug & Renal Category */}
      <div className="flex flex-wrap gap-3 text-sm text-gray-600">
        {drug_name && (
          <span className="inline-flex items-center gap-1 rounded-full bg-gray-100 px-3 py-1">
            💊 <span className="font-medium">{drug_name}</span>
          </span>
        )}
        {renal_category && (
          <span className="inline-flex items-center gap-1 rounded-full bg-gray-100 px-3 py-1">
            🫘 <span className="font-medium">{renal_category}</span>
          </span>
        )}
      </div>

      {/* Clinical Alert */}
      <AlertBadge
        warningFlag={warning_flag}
        warningMessage={warning_message}
        crcl={Number(calculated_crcl)}
      />

      {/* Disclaimer */}
      <p className="text-xs text-gray-400 italic border-t border-gray-100 pt-3">
        ⚠️ Bu hesaplama yalnızca klinik karar destek amacıyla sunulmaktadır. Nihai klinik karar yetkili sağlık profesyoneline aittir.
      </p>
    </div>
  )
}
