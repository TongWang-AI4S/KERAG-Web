<template>
  <div class="h-screen flex flex-col bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200 px-4 py-3">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <h1 class="text-xl font-bold text-gray-900">KERAG Web</h1>
          <div class="text-sm text-gray-500">
            {{ rootPath }}
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-600">{{ $t('common.web_lang') }}:</span>
            <select
              v-model="currentLanguage"
              @change="changeLanguage"
              class="px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="zh">中文</option>
              <option value="en">English</option>
            </select>
          </div>
          <SettingsButton />
          <div v-if="appStore.modules.loading" class="text-sm text-gray-500">
            {{ $t('app.loading') }}
          </div>
        </div>
      </div>
    </header>

    <!-- Search Bar -->
    <div class="bg-white border-b border-gray-200 px-4 py-2">
      <SearchBar />
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex overflow-hidden relative" @mousemove="handleMouseMove" @mouseup="stopResizing" @mouseleave="stopResizing">
      <!-- Left Sidebar -->
      <aside :style="{ width: sidebarWidth + 'px' }" class="bg-white border-r border-gray-200 overflow-y-auto shrink-0">
        <ModuleList />
      </aside>

      <!-- Resizer Left -->
      <div
        class="w-1 hover:w-1.5 bg-gray-200 hover:bg-blue-400 cursor-col-resize transition-all duration-150 shrink-0 z-10"
        @mousedown="startResizing('sidebar')"
      ></div>

      <!-- Center Panel Container -->
      <div class="flex-1 flex overflow-hidden">
        <!-- Tree Navigation -->
        <div :style="{ width: treeWidth + 'px' }" class="bg-gray-50 border-r border-gray-200 overflow-y-auto shrink-0">
          <Breadcrumb />
          <NodeTree />
        </div>

        <!-- Resizer Right -->
        <div
          class="w-1 hover:w-1.5 bg-gray-200 hover:bg-blue-400 cursor-col-resize transition-all duration-150 shrink-0 z-10"
          @mousedown="startResizing('tree')"
        ></div>

        <!-- Content Panel -->
        <div class="flex-1 bg-white flex flex-col min-w-0">
          <FormatSelector class="shrink-0" />
          <div class="flex-1 overflow-y-auto">
            <ContentView />
          </div>
        </div>
      </div>
    </div>
  </div>

  <SettingsModal />
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useAppStore } from '@/stores/app';
import { useI18n } from 'vue-i18n';
import { useSettingsStore } from '@/stores/settings';
import SearchBar from '@/components/SearchBar.vue';
import ModuleList from '@/components/ModuleList.vue';
import Breadcrumb from '@/components/Breadcrumb.vue';
import NodeTree from '@/components/NodeTree.vue';
import FormatSelector from '@/components/FormatSelector.vue';
import ContentView from '@/components/ContentView.vue';
import SettingsButton from '@/components/SettingsButton.vue';
import SettingsModal from '@/components/SettingsModal.vue';
import { api } from '@/api/client';

const appStore = useAppStore();
const { locale } = useI18n();

// Language switching
const currentLanguage = ref(locale.value);

const changeLanguage = async () => {
  locale.value = currentLanguage.value;
  // Reinitialize the app to reload modules with new language
  await appStore.initialize();
};

// Resize logic
const sidebarWidth = ref(256);
const treeWidth = ref(320);
const resizing = ref<null | 'sidebar' | 'tree'>(null);

const startResizing = (panel: 'sidebar' | 'tree') => {
  resizing.value = panel;
  document.body.style.cursor = 'col-resize';
  // Prevent text selection while resizing
  document.body.style.userSelect = 'none';
};

const stopResizing = () => {
  resizing.value = null;
  document.body.style.cursor = '';
  document.body.style.userSelect = '';
};

const handleMouseMove = (e: MouseEvent) => {
  if (!resizing.value) return;

  if (resizing.value === 'sidebar') {
    const newWidth = e.clientX;
    if (newWidth > 150 && newWidth < 600) {
      sidebarWidth.value = newWidth;
    }
  } else if (resizing.value === 'tree') {
    // treeWidth is relative to the current sidebarWidth + resizer
    const newWidth = e.clientX - sidebarWidth.value - 4; // 4 is approx resizer width
    if (newWidth > 200 && newWidth < 800) {
      treeWidth.value = newWidth;
    }
  }
};

const rootPath = computed(() => {
  const currentNode = appStore.navigation.currentNode;
  return currentNode?.path || 'Loading...';
});

onMounted(async () => {
  await appStore.initialize();
});
</script>

<style>
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
}
</style>
