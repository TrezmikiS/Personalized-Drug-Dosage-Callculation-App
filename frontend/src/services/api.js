import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Fetch available Narrow Therapeutic Index drugs from backend.
 * @returns {Promise<Array>} List of drugs
 */
export const getDrugs = async () => {
  const response = await apiClient.get('/api/drugs')
  return response.data
}

/**
 * Submit patient data to the calculation engine.
 * @param {Object} patientData - Patient vitals and drug selection
 * @returns {Promise<Object>} Calculation result with CrCl, dose and warning info
 */
export const calculateDose = async (patientData) => {
  const response = await apiClient.post('/api/calculate', patientData)
  return response.data
}
