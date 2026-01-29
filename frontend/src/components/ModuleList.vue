<template>
  <div class="p-4">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-lg font-semibold text-gray-900">{{ $t('modules.title') }}</h2>
      <button
        @click="purgeModules"
        :disabled="appStore.modules.loading"
        class="text-sm text-red-600 hover:text-red-800 disabled:opacity-50"
      >
        {{ $t('modules.purge') }}
      </button>
    </div>
    <div class="space-y-2">
      <div
        v-for="module in appStore.modules.modules"
        :key="module.name"
        class="border border-gray-200 rounded-lg p-3 hover:bg-gray-50 transition-colors"
        :class="{ 'bg-blue-50 border-blue-200': module.loaded }"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <div
              class="h-2 w-2 rounded-full"
              :class="module.loaded ? 'bg-green-500' : 'bg-gray-300'"
            ></div>
            <h3 class="font-medium text-gray-900">{{ module.name }}</h3>
            <span
              v-if="module.loaded"
              class="text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded-full"
            >
              {{ $t('modules.loaded') }}
            </span>
            <span v-else class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
              {{ $t('modules.available') }}
            </span>
          </div>
          <button
            v-if="!module.loaded"
            @click="loadModule(module.name)"
            :disabled="appStore.modules.loading"
            class="text-sm text-blue-600 hover:text-blue-800 disabled:opacity-50"
          >
            {{ $t('modules.load') }}
          </button>
          <button
            v-else
            @click="unloadModule(module.name)"
            :disabled="appStore.modules.loading"
            class="text-sm text-red-600 hover:text-red-800 disabled:opacity-50"
          >
            {{ $t('modules.unload') }}
          </button>
        </div>
        <div class="mt-1 text-sm text-gray-500">
          {{ $t('modules.files', { count: module.file_count }) }}
        </div>
      </div>
    </div>
    <div v-if="appStore.modules.modules.length === 0" class="text-center text-gray-500 py-8">
      {{ $t('app.no_content') }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAppStore } from '@/stores/app';

const appStore = useAppStore();

const loadModule = async (name: string) => {
  await appStore.loadModule(name);
};

const unloadModule = async (name: string) => {
  await appStore.unloadModule(name);
};

const purgeModules = async () => {
  if (confirm($t('modules.purge_confirm'))) {
    await appStore.purgeModules();
  }
};
</script>
