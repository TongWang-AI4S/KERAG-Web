<template>
  <div class="h-full flex flex-col">
    <!-- Search Results -->
    <div v-if="appStore.search.results.length > 0" class="flex-1 overflow-y-auto">
      <div class="p-4">
        <h2 class="text-lg font-semibold mb-4">{{ $t('search.results', { count: appStore.search.results.length }) }}</h2>
        <div class="space-y-4">
          <div
            v-for="result in appStore.search.results"
            :key="result.node_id"
            @click="navigateToResult(result.node_id)"
            class="p-4 bg-white border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-sm cursor-pointer transition-all"
          >
            <!-- Large font: Title or Content Preview -->
            <h3 class="text-lg font-bold text-gray-900 mb-1">
              <template v-if="result.type === 'section'">
                {{ result.title || result.label }}
              </template>
              <template v-else>
                {{ result.content_preview || result.label }}
              </template>
            </h3>

            <!-- Small font: Node ID -->
            <div class="text-xs font-mono text-gray-500 mb-2">
              {{ result.node_id }}
            </div>

            <!-- Match Excerpt -->
            <p class="text-sm text-gray-700 bg-gray-50 p-2 rounded border-l-4 border-gray-200 line-clamp-2">
              {{ result.excerpt }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Node Content -->
    <div v-else-if="appStore.navigation.currentNode" class="flex-1 overflow-y-auto">
      <div class="p-6">
        <!-- Node Header -->
        <div class="mb-6">
          <div class="flex items-center space-x-2 mb-2">
            <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
              {{ appStore.navigation.currentNode.type }}
            </span>
            <span v-if="appStore.navigation.currentNode.module" class="text-xs bg-gray-100 text-gray-800 px-2 py-1 rounded">
              {{ appStore.navigation.currentNode.module }}
            </span>
          </div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">
            {{ appStore.navigation.currentNode.title || appStore.navigation.currentNode.label }}
          </h1>
          <div class="text-sm text-gray-500">
            <span>{{ appStore.navigation.currentNode.file_path }}</span>
            <span v-if="appStore.navigation.currentNode.line_number">:{{ appStore.navigation.currentNode.line_number }}</span>
          </div>
        </div>

        <!-- Node Metadata -->
        <div class="mb-6 p-4 bg-gray-50 rounded-lg">
          <h2 class="text-sm font-semibold text-gray-700 mb-2">{{ $t('view.metadata') }}</h2>
          <dl class="grid grid-cols-2 gap-2 text-sm">
            <div>
              <dt class="text-gray-500">ID:</dt>
              <dd class="font-mono text-gray-900">{{ appStore.navigation.currentNode.id }}</dd>
            </div>
            <div>
              <dt class="text-gray-500">{{ $t('search.label') }}:</dt>
              <dd class="text-gray-900">{{ appStore.navigation.currentNode.label }}</dd>
            </div>
            <div>
              <dt class="text-gray-500">{{ $t('node.section_node') }}:</dt>
              <dd class="text-gray-900">{{ appStore.navigation.currentNode.type }}</dd>
            </div>
            <div v-if="appStore.navigation.currentNode.module">
              <dt class="text-gray-500">{{ $t('modules.title') }}:</dt>
              <dd class="text-gray-900">{{ appStore.navigation.currentNode.module }}</dd>
            </div>
          </dl>
        </div>

        <!-- Node Content -->
        <div class="prose max-w-none">
          <div v-if="appStore.contentFormat === 'markdown'">
            <MarkdownRenderer :content="getContent()" />
          </div>
          <div v-else-if="appStore.contentFormat === 'text'">
            <pre class="whitespace-pre-wrap font-sans text-gray-800">{{ getContent() }}</pre>
          </div>
          <div v-else-if="appStore.contentFormat === 'tree'">
            <pre class="whitespace-pre-wrap font-mono text-sm bg-gray-50 p-4 rounded">{{ getTreeView() }}</pre>
          </div>
          <div v-else-if="appStore.contentFormat === 'json'">
            <pre class="whitespace-pre-wrap font-mono text-sm bg-gray-50 p-4 rounded">{{ getJsonView() }}</pre>
          </div>
        </div>

        <!-- Inline Links (类似see also风格) -->
        <div v-if="appStore.navigation.currentNode.type === 'content' && appStore.navigation.currentNode.inline_links && appStore.navigation.currentNode.inline_links.length > 0" class="mt-8">
          <h2 class="text-lg font-semibold mb-3">{{ $t('node.inline_references') }}</h2>
          <div class="space-y-2">
            <div
              v-for="link in appStore.navigation.currentNode.inline_links"
              :key="link.target_id"
              @click="navigateToResult(link.target_id)"
              class="p-2 bg-blue-50 rounded hover:bg-blue-100 cursor-pointer"
            >
              <div class="font-medium text-blue-900">{{ link.target_title || link.target_id }}</div>
              <div class="text-sm text-blue-700">{{ link.link_text }}</div>
            </div>
          </div>
        </div>

        <!-- See Also -->
        <div v-if="appStore.navigation.currentNode.see_also && appStore.navigation.currentNode.see_also.length > 0" class="mt-8">
          <h2 class="text-lg font-semibold mb-3">{{ $t('node.related_links') }}</h2>
          <div class="space-y-2">
            <div
              v-for="link in appStore.navigation.currentNode.see_also"
              :key="link.node_id"
              @click="navigateToResult(link.node_id)"
              class="p-2 bg-blue-50 rounded hover:bg-blue-100 cursor-pointer"
            >
              <div class="font-medium text-blue-900">{{ link.title }}</div>
              <div v-if="link.description" class="text-sm text-blue-700">{{ link.description }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- No Content -->
    <div v-else class="flex-1 flex items-center justify-center text-gray-500">
      <div class="text-center">
        <svg class="h-12 w-12 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <p>{{ $t('node.select_prompt') }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAppStore } from '@/stores/app';
import MarkdownRenderer from './MarkdownRenderer.vue';

const appStore = useAppStore();

const getContent = () => {
  const node = appStore.navigation.currentNode;
  if (!node) return '';

  // 优先使用后端返回的格式化内容
  if (node.formatted_content && node.formatted_content.markdown) {
    return node.formatted_content.markdown;
  }
  if (node.formatted_content && node.formatted_content.text) {
    return node.formatted_content.text;
  }

  return node.content || 'No content available';
};

const getTreeView = () => {
  const node = appStore.navigation.currentNode;
  if (!node) return '';

  // 优先使用后端返回的格式化树
  if (node.formatted_content && node.formatted_content.tree) {
    return node.formatted_content.tree;
  }

  // Fallback (old manual logic)
  let tree = node.label || node.title || 'Untitled';
  if (node.children_ids && node.children_ids.length > 0) {
    tree += `\n${node.children_ids.map((id: string) => `├── ${id}`).join('\n')}`;
  }

  return tree;
};

const getJsonView = () => {
  const node = appStore.navigation.currentNode;
  if (node && node.formatted_content && node.formatted_content.json_data) {
    return JSON.stringify(node.formatted_content.json_data, null, 2);
  }
  return JSON.stringify(node, null, 2);
};

const navigateToResult = async (nodeId: string) => {
  await appStore.navigateTo(nodeId);
  appStore.clearSearch();
};
</script>

<style scoped>
.prose {
  max-width: none;
}

.prose pre {
  @apply bg-gray-50 p-4 rounded;
}
</style>
