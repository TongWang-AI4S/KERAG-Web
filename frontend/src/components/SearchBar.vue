<template>
  <div class="flex items-center space-x-4">
    <div class="flex-1 max-w-md">
      <div class="relative">
        <input
          v-model="appStore.search.query"
          @keyup.enter="performSearch"
          type="text"
          :placeholder="$t('search.placeholder')"
          class="w-full px-4 py-2 pl-10 pr-4 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <svg
          class="absolute left-3 top-2.5 h-4 w-4 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
        <button
          v-if="appStore.search.query"
          @click="clearSearch"
          class="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
        >
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>
    <select
      v-model="appStore.search.scope"
      class="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <option value="all">{{ $t('search.all') }}</option>
      <option value="content">{{ $t('search.content') }}</option>
      <option value="title">{{ $t('search.title') }}</option>
      <option value="label">{{ $t('search.label') }}</option>
    </select>

    <!-- New Search Options -->
    <div class="flex items-center space-x-2">
      <button
        @click="appStore.search.caseSensitive = !appStore.search.caseSensitive"
        :class="appStore.search.caseSensitive ? 'bg-blue-100 text-blue-700 border-blue-300' : 'bg-gray-50 text-gray-600 border-gray-200'"
        class="px-2 py-1 text-xs border rounded transition-colors whitespace-nowrap"
      >
        {{ $t('search.case_sensitive') }}
      </button>
      <button
        @click="appStore.search.wholeWord = !appStore.search.wholeWord"
        :class="appStore.search.wholeWord ? 'bg-blue-100 text-blue-700 border-blue-300' : 'bg-gray-50 text-gray-600 border-gray-200'"
        class="px-2 py-1 text-xs border rounded transition-colors whitespace-nowrap"
      >
        {{ $t('search.whole_word') }}
      </button>
      <button
        @click="appStore.search.useRegex = !appStore.search.useRegex"
        :class="appStore.search.useRegex ? 'bg-blue-100 text-blue-700 border-blue-300' : 'bg-gray-50 text-gray-600 border-gray-200'"
        class="px-2 py-1 text-xs border rounded transition-colors whitespace-nowrap"
      >
        {{ $t('search.regex') }}
      </button>
    </div>

    <button
      @click="performSearch"
      :disabled="appStore.search.loading"
      class="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {{ appStore.search.loading ? $t('app.loading') : $t('search.button') }}
    </button>
    <span v-if="appStore.search.results.length > 0" class="text-sm text-gray-500">
      {{ $t('search.results', { count: appStore.search.results.length }) }}
    </span>
    <button
      v-if="appStore.search.results.length > 0"
      @click="clearSearch"
      class="text-sm text-blue-600 hover:text-blue-800"
    >
      {{ $t('search.clear') }}
    </button>

    <!-- Navigation Buttons -->
    <div class="flex-1"></div>
    <div class="flex items-center space-x-1 border-l border-gray-200 pl-4">
      <!-- Jump to Node ID -->
      <div class="flex items-center space-x-1 mr-2">
        <input
          v-model="jumpId"
          @keyup.enter="handleJump"
          type="text"
          :placeholder="$t('search.jump_placeholder')"
          class="w-32 px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
        />
        <button
          @click="handleJump"
          class="px-2 py-1 text-xs bg-gray-100 text-gray-600 border border-gray-300 rounded hover:bg-blue-50 hover:text-blue-600 hover:border-blue-300 transition-colors whitespace-nowrap"
        >
          {{ $t('search.jump') }}
        </button>
      </div>

      <button
        @click="appStore.navigateBack()"
        class="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
        :title="$t('search.back')"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
      </button>
      <button
        @click="appStore.navigateForward()"
        class="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
        :title="$t('search.forward')"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
        </svg>
      </button>
      <button
        @click="appStore.navigateUp()"
        class="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
        :title="$t('search.up')"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
        </svg>
      </button>

      <!-- History Dropdown -->
      <div class="relative">
        <button
          @click="toggleHistory"
          class="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
          :title="$t('search.history')"
          ref="historyBtn"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </button>

        <div
          v-if="showHistory"
          class="absolute right-0 mt-1 w-80 bg-white border border-gray-200 rounded-lg shadow-xl z-50 overflow-hidden flex flex-col max-h-[400px]"
        >
          <div class="p-2 border-b border-gray-100 bg-gray-50 text-xs font-semibold text-gray-500 uppercase tracking-wider">
            {{ $t('search.browse_history') }}
          </div>
          <div class="overflow-y-auto flex-1">
            <div
              v-for="(nodeId, index) in appStore.navigation.history"
              :key="`${nodeId}-${index}`"
              @click="jumpToHistory(index)"
              class="px-4 py-2 hover:bg-blue-50 cursor-pointer border-b border-gray-50 last:border-0 group"
              :class="{ 'bg-blue-50': index === appStore.navigation.historyCursor }"
            >
              <div class="flex flex-col">
                <span
                  class="text-sm truncate"
                  :class="index === appStore.navigation.historyCursor ? 'font-bold text-blue-700' : 'text-gray-900'"
                >
                  {{ getHistoryTitle(nodeId) }}
                </span>
                <span class="text-[10px] text-gray-400 font-mono truncate">
                  {{ nodeId }}
                </span>
              </div>
            </div>
          </div>
          <div v-if="appStore.navigation.history.length === 0" class="p-4 text-center text-sm text-gray-400">
            {{ $t('search.no_history') }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useAppStore } from '@/stores/app';

const appStore = useAppStore();
const showHistory = ref(false);
const jumpId = ref('');
const historyBtn = ref<HTMLElement | null>(null);

const handleJump = async () => {
  if (!jumpId.value.trim()) return;
  await appStore.navigateTo(jumpId.value.trim());
  jumpId.value = '';
};

const toggleHistory = () => {
  showHistory.value = !showHistory.value;
};

const closeHistory = (e: MouseEvent) => {
  if (historyBtn.value && !historyBtn.value.contains(e.target as Node)) {
    showHistory.value = false;
  }
};

onMounted(() => {
  window.addEventListener('click', closeHistory);
});

onUnmounted(() => {
  window.removeEventListener('click', closeHistory);
});

const getHistoryTitle = (nodeId: string) => {
  const cached = appStore.nodeCache[nodeId];
  if (cached && cached.node) {
    if (cached.node.type === 'section') {
       return cached.node.title || cached.node.label;
    } else {
       return cached.node.content_preview || cached.node.label;
    }
  }
  return nodeId.split('::').pop() || nodeId;
};

const jumpToHistory = async (targetIndex: number) => {
  const currentIndex = appStore.navigation.historyCursor;
  if (targetIndex === currentIndex) return;

  const steps = Math.abs(targetIndex - currentIndex);
  if (targetIndex < currentIndex) {
    await appStore.navigateBack(steps);
  } else {
    await appStore.navigateForward(steps);
  }
  showHistory.value = false;
};

const performSearch = async () => {
  if (!appStore.search.query.trim()) {
    clearSearch();
    return;
  }
  await appStore.performSearch(appStore.search.query, appStore.search.scope);
};

const clearSearch = () => {
  appStore.clearSearch();
};
</script>
