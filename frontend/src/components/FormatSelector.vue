<template>
  <div class="bg-white border-b border-gray-200 px-4 py-2 flex flex-wrap items-center gap-4">
    <!-- Format Selector -->
    <div class="flex items-center space-x-2">
      <span class="text-sm font-medium text-gray-700 whitespace-nowrap">{{ $t('view.format') }}：</span>
      <div class="flex items-center bg-gray-100 rounded-lg p-0.5">
        <button
          v-for="format in formats"
          :key="format.value"
          @click="selectFormat(format.value)"
          :class="{
            'bg-white text-blue-600 shadow-sm': appStore.contentFormat === format.value,
            'text-gray-600 hover:text-gray-900': appStore.contentFormat !== format.value
          }"
          class="px-2.5 py-1 text-xs rounded-md transition-colors whitespace-nowrap"
        >
          {{ format.label }}
        </button>
      </div>
    </div>

    <!-- View Options -->
    <div class="flex items-center space-x-4 border-l border-gray-200 pl-4">
      <!-- Depth -->
      <div class="flex items-center space-x-1.5">
        <label class="text-sm font-medium text-gray-700 whitespace-nowrap">{{ $t('view.depth') }}：</label>
        <input
          type="number"
          v-model.number="appStore.viewOptions.depth"
          min="0"
          max="5"
          @change="updateView"
          class="w-12 px-1.5 py-1 text-xs border border-gray-300 rounded focus:ring-1 focus:ring-blue-500 outline-none"
        />
      </div>

      <!-- Include Content -->
      <div class="flex items-center space-x-1.5">
        <input
          type="checkbox"
          id="include-content"
          v-model="appStore.viewOptions.include_content"
          @change="updateView"
          class="w-3.5 h-3.5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
        />
        <label for="include-content" class="text-sm font-medium text-gray-700 cursor-pointer select-none">{{ $t('view.include_content') }}</label>
      </div>

      <!-- Include See Also -->
      <div class="flex items-center space-x-1.5">
        <input
          type="checkbox"
          id="include-see-also"
          v-model="appStore.viewOptions.include_see_also"
          @change="updateView"
          class="w-3.5 h-3.5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
        />
        <label for="include-see-also" class="text-sm font-medium text-gray-700 cursor-pointer select-none">{{ $t('view.include_see_also') }}</label>
      </div>

      <!-- Show Metadata (Tree only) -->
      <div v-if="appStore.contentFormat === 'tree'" class="flex items-center space-x-1.5">
        <input
          type="checkbox"
          id="show-metadata"
          v-model="appStore.viewOptions.show_metadata"
          @change="updateView"
          class="w-3.5 h-3.5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
        />
        <label for="show-metadata" class="text-sm font-medium text-gray-700 cursor-pointer select-none">{{ $t('view.metadata') }}</label>
      </div>

      <!-- Display Mode (Markdown only) -->
      <div v-if="appStore.contentFormat === 'markdown'" class="flex items-center space-x-1.5">
        <label class="text-sm font-medium text-gray-700 whitespace-nowrap">{{ $t('view.display_mode') }}：</label>
        <select
          v-model="appStore.viewOptions.display_mode"
          @change="updateView"
          class="px-1.5 py-1 text-xs border border-gray-300 rounded focus:ring-1 focus:ring-blue-500 outline-none bg-white"
        >
          <option value="none">{{ $t('view.mode.none') }}</option>
          <option value="label">{{ $t('view.mode.label') }}</option>
          <option value="full_id">{{ $t('view.full_id') }}</option>
        </select>
      </div>

      <!-- Refresh Button -->
      <button
        @click="updateView"
        class="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-colors"
        :title="$t('view.refresh_view')"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAppStore } from '@/stores/app'
import { useI18n } from 'vue-i18n'

const appStore = useAppStore()
const { t } = useI18n()

const formats = [
  { value: 'markdown', label: 'Markdown' },
  { value: 'text', label: t('view.text_format') },
  { value: 'tree', label: t('view.tree_format') },
  { value: 'json', label: 'JSON' }
];

const selectFormat = (format: string) => {
  appStore.contentFormat = format as any;
  updateView();
};

const updateView = () => {
  appStore.fetchNodeView();
};
</script>
