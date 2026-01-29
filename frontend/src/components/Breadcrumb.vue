<template>
  <div class="bg-white border-b border-gray-200 px-4 py-2">
    <nav class="flex" aria-label="Breadcrumb">
      <ol class="flex items-center space-x-2">
        <li
          v-for="(item, index) in appStore.navigation.breadcrumb"
          :key="item.id"
          class="flex items-center"
        >
          <button
            @click="navigateTo(item.id)"
            class="text-sm hover:text-blue-600"
            :class="{
              'text-gray-500': index < appStore.navigation.breadcrumb.length - 1,
              'text-gray-900 font-medium': index === appStore.navigation.breadcrumb.length - 1
            }"
          >
            {{ item.label || $t('navigation.breadcrumb') }}
          </button>
          <svg
            v-if="index < appStore.navigation.breadcrumb.length - 1"
            class="h-4 w-4 text-gray-400 ml-2"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
              clip-rule="evenodd"
            />
          </svg>
        </li>
      </ol>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { useAppStore } from '@/stores/app';

const appStore = useAppStore();

const navigateTo = async (nodeId: string) => {
  await appStore.navigateTo(nodeId);
};
</script>
