<template>
  <div class="select-none" v-if="node && node.node_id">
    <div
      class="flex items-center py-1 px-2 hover:bg-gray-100 rounded cursor-pointer group"
      :class="{
        'bg-blue-50': isCurrent,
        'pl-0': level === 0
      }"
      :style="{ paddingLeft: `${level * 16 + 8}px` }"
      @click="handleClick"
      @dblclick="handleDblClick"
    >
      <!-- Expand/Collapse Icon -->
      <span
        v-if="hasChildren"
        class="mr-1 w-4 h-4 flex items-center justify-center text-gray-400 hover:text-gray-600"
        @click.stop="toggleExpand"
      >
        <svg
          v-if="!isExpanded"
          class="w-3 h-3 transition-transform"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
        <svg
          v-else
          class="w-3 h-3 transition-transform"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </span>
      <span v-else class="w-4 h-4 mr-1"></span>

      <!-- Node Icon -->
      <span class="mr-2 text-gray-500">
        <svg
          v-if="node.type === 'section'"
          class="w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"
          />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v0" />
        </svg>
        <svg
          v-else-if="node.type === 'content'"
          class="w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <svg
          v-else-if="node.type === 'loading'"
          class="w-4 h-4 animate-spin"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
          />
        </svg>
        <svg
          v-else
          class="w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      </span>

      <!-- Node Label and Title -->
      <div class="flex flex-col min-w-0 overflow-hidden">
        <div class="flex items-baseline gap-2">
          <span
            class="text-sm truncate"
            :class="{
              'font-semibold text-blue-700': isCurrent,
              'font-medium text-gray-900': !isCurrent && node.type === 'section',
              'text-gray-700': !isCurrent && node.type !== 'section'
            }"
          >
            <template v-if="node.type === 'content'">
              {{ $t('node.content_node') }}: {{ node.content_preview?.substring(0, 15) || '...' }}
            </template>
            <template v-else>
              {{ node.title || node.label || 'Untitled' }}
            </template>
          </span>
          <span class="text-[10px] text-gray-400 font-mono truncate shrink-0">
            {{ node.label }}
          </span>
        </div>
      </div>

      <!-- Loading indicator for children -->
      <span v-if="loading" class="ml-2 text-xs text-gray-400">{{ $t('app.loading') }}</span>
    </div>

    <!-- Children Nodes (Recursive) -->
    <div v-if="isExpanded && hasChildren" class="mt-1">
      <TreeNode
        v-for="childId in childIds"
        :key="childId"
        :node="getChildNode(childId)"
        :level="level + 1"
        :is-expanded="appStore.navigation.expandedNodes.has(childId)"
        :is-current="appStore.navigation.currentNode?.node_id === childId"
        @toggle="(id) => $emit('toggle', id)"
        @navigate="(id) => $emit('navigate', id)"
      />
    </div>
  </div>
  <div v-else class="text-xs text-red-500 p-1">Invalid node</div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAppStore } from '@/stores/app';
import type { NodeDetail, NodeInfo } from '@/types';

const props = defineProps<{
  node: NodeDetail | NodeInfo;
  level: number;
  isExpanded: boolean;
  isCurrent: boolean;
}>();

const emit = defineEmits<{
  (e: 'toggle', nodeId: string): void;
  (e: 'navigate', nodeId: string): void;
}>();

const appStore = useAppStore();
const loading = ref(false);

const hasChildren = computed(() => {
  // If we have actual children list in store, use its length
  const childrenIds = appStore.nodeChildren[props.node.node_id!];
  if (childrenIds) return childrenIds.length > 0;

  // Otherwise fallback to metadata
  const node = props.node as any;
  return node.has_children || (node.children_ids && node.children_ids.length > 0);
});

const childIds = computed(() => {
  // Always prefer the ID list from store if available
  const storedIds = appStore.nodeChildren[props.node.node_id!];
  if (storedIds) return storedIds;

  // Fallback to node.children_ids if it's a NodeDetail
  return (props.node as NodeDetail).children_ids || [];
});

const getChildNode = (childId: string): NodeInfo => {
  // 1. Check nodeChildrenInfo (Preview objects)
  const childrenInfo = appStore.nodeChildrenInfo[props.node.node_id!];
  if (childrenInfo) {
    const cached = childrenInfo.find(c => c.node_id === childId);
    if (cached) return cached;
  }

  // 2. Check module roots
  const allRoots = Object.values(appStore.moduleRoots).flat();
  const root = (allRoots as any[]).find(r => r.node_id === childId);
  if (root) return root;

  // 3. Fallback placeholder
  // If we have children IDs but no info yet, it's a loading state
  return {
    node_id: childId,
    label: childId.split('::').pop() || childId,
    type: 'loading', // Special type to indicate we don't know the real type yet
    has_children: true,
  } as any;
};

const toggleExpand = async () => {
  if (!props.node.node_id) return;

  if (!props.isExpanded) {
    loading.value = true;
    try {
      await appStore.loadNodeChildren(props.node.node_id);
    } catch (e) {
      console.error('Failed to load children:', e);
    } finally {
      loading.value = false;
    }
  }

  emit('toggle', props.node.node_id);
};

const navigate = () => {
  if (!props.node.node_id) return;
  emit('navigate', props.node.node_id);
};

const handleClick = () => {
  if (!props.node.node_id) return;
  navigate();
};

const handleDblClick = () => {
  if (!props.node.node_id) return;
  if (hasChildren.value) {
    toggleExpand();
  }
};
</script>
