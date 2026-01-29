import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/api/client'

export const useSettingsStore = defineStore('settings', () => {
  const keragHome = ref('')
  const keragLocal = ref('')
  const keragLang = ref('')
  const isModalOpen = ref(false)
  const isApplying = ref(false)

  const originalSettings = ref({
    keragHome: '',
    keragLocal: '',
    keragLang: ''
  })

  const hasChanges = computed(() => {
    return (
      keragHome.value !== originalSettings.value.keragHome ||
      keragLocal.value !== originalSettings.value.keragLocal ||
      keragLang.value !== originalSettings.value.keragLang
    )
  })

  async function loadSettings() {
    try {
      const response = await api.getSettings()
      if (response.success) {
        keragHome.value = response.data.kerag_home || ''
        keragLocal.value = response.data.kerag_local || ''
        keragLang.value = response.data.kerag_lang || ''

        originalSettings.value = {
          keragHome: keragHome.value,
          keragLocal: keragLocal.value,
          keragLang: keragLang.value
        }
      }
    } catch (error) {
      console.error('Failed to load settings:', error)
    }
  }

  async function applySettings() {
    isApplying.value = true
    try {
      const response = await api.applySettings({
        kerag_home: keragHome.value,
        kerag_local: keragLocal.value,
        kerag_lang: keragLang.value
      })

      if (response.success) {
        isModalOpen.value = false
        window.location.reload()
      } else {
        throw new Error(response.error || 'Failed to apply settings')
      }
    } catch (error) {
      alert(error instanceof Error ? error.message : 'Failed to apply settings')
    } finally {
      isApplying.value = false
    }
  }

  function cancel() {
    isModalOpen.value = false
    // Restore original values
    keragHome.value = originalSettings.value.keragHome
    keragLocal.value = originalSettings.value.keragLocal
    keragLang.value = originalSettings.value.keragLang
  }

  return {
    keragHome,
    keragLocal,
    keragLang,
    isModalOpen,
    isApplying,
    hasChanges,
    loadSettings,
    applySettings,
    cancel
  }
})
