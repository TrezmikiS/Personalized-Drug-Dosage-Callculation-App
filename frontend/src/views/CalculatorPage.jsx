import { useState } from 'react'
import PatientForm from '../components/PatientForm'
import ResultCard from '../components/ResultCard'

/**
 * CalculatorPage — Main clinical dosage calculator view.
 * Renders the patient form and the result card side-by-side on larger screens.
 */
export default function CalculatorPage() {
  const [result, setResult] = useState(null)

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-10 px-4">
      {/* Page Header */}
      <div className="mx-auto max-w-5xl">
        <div className="mb-8 text-center">
          <div className="inline-flex items-center gap-3 rounded-2xl bg-white border border-blue-100 shadow px-6 py-3 mb-4">
            <span className="text-3xl">🏥</span>
            <div className="text-left">
              <h1 className="text-xl font-bold text-gray-900">
                Kişiselleştirilmiş İlaç Dozu Hesaplama
              </h1>
              <p className="text-xs text-gray-500">
                Dar Terapötik İndeksli İlaçlar — Farmakokinetik Karar Destek Sistemi
              </p>
            </div>
          </div>

          {/* Team Badge */}
          <div className="flex justify-center flex-wrap gap-2 text-xs text-gray-500">
            <span className="rounded-full bg-white border border-gray-200 px-3 py-1 shadow-sm">
              👨‍💻 Ceyhun Mehmet Keklik
            </span>
            <span className="rounded-full bg-white border border-gray-200 px-3 py-1 shadow-sm">
              👨‍💻 Hamza Karayiğit
            </span>
            <span className="rounded-full bg-white border border-gray-200 px-3 py-1 shadow-sm">
              💊 Ahsen Özateş (Klinik Lider)
            </span>
          </div>
        </div>

        {/* Info Banner */}
        <div className="mb-6 rounded-xl border border-blue-200 bg-blue-50 px-5 py-3 text-sm text-blue-700 flex gap-2 items-start">
          <span>ℹ️</span>
          <span>
            Bu sistem Cockcroft-Gault eşitliğini kullanarak kreatinin klirensini (CrCl) hesaplar
            ve böbrek fonksiyonuna göre dar terapötik aralıklı ilaçların dozunu kişiselleştirir.
          </span>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
          {/* Form Panel */}
          <div className="rounded-2xl border border-gray-200 bg-white shadow-lg p-6">
            <div className="flex items-center gap-2 border-b border-gray-100 pb-3 mb-5">
              <span className="text-xl">🩺</span>
              <h2 className="text-base font-bold text-gray-800">Hasta Bilgileri</h2>
            </div>
            <PatientForm onResult={setResult} />
          </div>

          {/* Result Panel */}
          <div className="md:sticky md:top-6">
            {result ? (
              <ResultCard result={result} />
            ) : (
              <div className="rounded-2xl border border-dashed border-gray-300 bg-white p-10 text-center text-gray-400 shadow-sm">
                <span className="block text-4xl mb-3">🧮</span>
                <p className="text-sm font-medium">
                  Hasta bilgilerini doldurun ve hesapla butonuna basın.
                </p>
                <p className="text-xs mt-1">
                  Sonuçlar burada görüntülenecektir.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-10 text-center text-xs text-gray-400">
          Personalised Drug Dosage Calculation App — FE401 Proje · Bilgisayar Mühendisliği & Eczacılık
        </footer>
      </div>
    </div>
  )
}
