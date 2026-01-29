<template>
  <div v-if="settingsStore.isModalOpen" class="modal-overlay" @click="cancel">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2 class="text-lg font-semibold">{{ $t('settings.title') }}</h2>
        <button
          @click="cancel"
          class="p-1 hover:bg-gray-100 rounded transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Warning Message -->
      <div class="warning-banner">
        <div class="warning-icon">⚠️</div>
        <div class="warning-text">
          {{ $t('settings.warning') }}
        </div>
      </div>

      <form @submit.prevent="handleApply" class="modal-body">
        <div class="form-group">
          <label class="form-label">
            {{ $t('settings.keragHome') }}
            <span class="form-hint">{{ $t('settings.keragHomeHint') }}</span>
          </label>
          <input
            v-model="settingsStore.keragHome"
            type="text"
            class="form-input"
            placeholder="/path/to/global/root"
          />
        </div>

        <div class="form-group">
          <label class="form-label">
            {{ $t('settings.keragLocal') }}
            <span class="form-hint">{{ $t('settings.keragLocalHint') }}</span>
          </label>
          <input
            v-model="settingsStore.keragLocal"
            type="text"
            class="form-input"
            placeholder="/path/to/local/root (optional)"
          />
        </div>

        <div class="form-group">
          <label class="form-label">
            {{ $t('settings.keragLang') }}
            <span class="form-hint">{{ $t('settings.keragLangHint') }}</span>
          </label>
          <select v-model="settingsStore.keragLang" class="form-input">
            <option value="">{{ $t('settings.langAuto') }}</option>
            <option value="en">English</option>
            <option value="zh">中文</option>
          </select>
        </div>

        <div class="modal-footer">
          <button
            type="button"
            @click="cancel"
            class="btn btn-secondary"
          >
            {{ $t('common.cancel') }}
          </button>
          <button
            type="submit"
            :disabled="!settingsStore.hasChanges || settingsStore.isApplying"
            class="btn btn-primary"
          >
            {{ settingsStore.isApplying ? $t('common.applying') : $t('settings.apply') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingsStore } from '@/stores/settings'

const settingsStore = useSettingsStore()

const handleApply = async () => {
  await settingsStore.applySettings()
}

const cancel = () => {
  settingsStore.cancel()
}
</script>

<style scoped>
.modal-overlay {
  @apply fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50;
}

.modal-content {
  @apply bg-white rounded-lg shadow-xl w-full max-w-md mx-4 overflow-hidden;
}

.modal-header {
  @apply flex justify-between items-center p-6 border-b border-gray-200;
}

.warning-banner {
  @apply bg-yellow-50 border-b border-yellow-200 p-4 flex items-start gap-3;
}

.warning-icon {
  @apply text-xl mt-0.5;
}

.warning-text {
  @apply text-sm text-yellow-800;
}

.modal-body {
  @apply p-6 space-y-6;
}

.modal-footer {
  @apply flex justify-end gap-3 pt-4 border-t border-gray-100;
}

.form-group {
  @apply space-y-2;
}

.form-label {
  @apply block font-medium text-gray-900;
}

.form-hint {
  @apply block font-normal text-sm text-gray-500 mt-1;
}

.form-input {
  @apply w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500;
}

.btn {
  @apply px-4 py-2 rounded-md font-medium transition-colors;
}

.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed;
}

.btn-secondary {
  @apply bg-gray-200 text-gray-800 hover:bg-gray-300;
}
</style>
