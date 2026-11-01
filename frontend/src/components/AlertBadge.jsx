/**
 * AlertBadge — Dynamic clinical warning card.
 *
 * Props:
 *   warningFlag    {boolean} — whether a clinical warning is active
 *   warningMessage {string}  — backend warning detail message
 *   crcl           {number}  — calculated creatinine clearance (mL/min)
 */
export default function AlertBadge({ warningFlag, warningMessage, crcl }) {
  // 🟢 Normal — no warning
  if (!warningFlag) {
    return (
      <div className="flex items-start gap-3 rounded-xl border border-green-300 bg-green-50 p-4 shadow-sm">
        <span className="mt-0.5 text-2xl">🟢</span>
        <div>
          <p className="font-semibold text-green-800">Böbrek Fonksiyonu Normal</p>
          <p className="mt-1 text-sm text-green-700">
            Standart dozaj uygulanabilir. Rutin klinik takip önerilir.
          </p>
        </div>
      </div>
    )
  }

  // 🔴 Critical — CrCl < 10 mL/min (End-Stage Renal Disease)
  if (crcl !== null && crcl < 10) {
    return (
      <div className="flex items-start gap-3 rounded-xl border border-red-400 bg-red-50 p-4 shadow-sm">
        <span className="mt-0.5 text-2xl">🔴</span>
        <div>
          <p className="font-bold text-red-800 uppercase tracking-wide">
            KRİTİK — Son Dönem Böbrek Yetmezliği
          </p>
          <p className="mt-1 text-sm text-red-700">
            Standart dozlamayı <strong>durdurun</strong>. Serum ilaç düzeyi izlemi (TDM) ve klinik eczacı konsültasyonu <strong>zorunludur</strong>.
          </p>
          {warningMessage && (
            <p className="mt-2 text-xs text-red-600 italic border-t border-red-200 pt-2">
              Sistem Mesajı: {warningMessage}
            </p>
          )}
        </div>
      </div>
    )
  }

  // 🟡 Warning — CrCl 10–50 mL/min (Moderate-Severe Renal Impairment)
  return (
    <div className="flex items-start gap-3 rounded-xl border border-yellow-400 bg-yellow-50 p-4 shadow-sm">
      <span className="mt-0.5 text-2xl">🟡</span>
      <div>
        <p className="font-semibold text-yellow-800">Doz Düzeltmesi Gerekli</p>
        <p className="mt-1 text-sm text-yellow-700">
          Orta-ileri böbrek yetmezliği tespit edildi. Doz aralığı uzatılmalı veya idame dozu <strong>%50 azaltılmalıdır</strong>.
        </p>
        {warningMessage && (
          <p className="mt-2 text-xs text-yellow-600 italic border-t border-yellow-200 pt-2">
            Sistem Mesajı: {warningMessage}
          </p>
        )}
      </div>
    </div>
  )
}
