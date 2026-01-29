<template>
  <div class="p-2 relative">
    <!-- Loading overlay (less intrusive) -->
    <div v-if="appStore.navigation.loading" class="absolute top-0 right-2">
      <div class="text-[10px] text-blue-500 animate-pulse">{{ $t('navigation.syncing') }}</div>
    </div>

    <div v-if="nodes.length > 0" class="space-y-1">
      <TreeNode
        v-for="(node, index) in nodes"
        :key="node.node_id || `node-${index}`"
        :node="node"
        :level="0"
        :is-expanded="appStore.navigation.expandedNodes.has(node.node_id)"
        :is-current="appStore.navigation.currentNode?.node_id === node.node_id"
        @toggle="toggleNode"
        @navigate="navigateToNode"
      />
    </div>
    <div v-else class="text-center text-gray-500 py-8">
      {{ $t('navigation.no_nodes') }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useAppStore } from '@/stores/app';
import TreeNode from './TreeNode.vue';
import type { NodeDetail, NodeInfo } from '@/types';

const appStore = useAppStore();

const nodes = computed<(NodeDetail | NodeInfo)[]>(() => {
  const nodeList: (NodeDetail | NodeInfo)[] = [];

  // 1. 添加所有已加载模块的根节点（可能有多个）
  const allRoots = Object.values(appStore.moduleRoots);

  for (const root of allRoots) {
    if (root) {
      if (Array.isArray(root)) {
        for (const r of root) {
          if (r && r.node_id) {
            nodeList.push(r);
          }
        }
      } else if (root.node_id) {
        nodeList.push(root);
      }
    }
  }

  // 去重 (以防重复)
  const seen = new Set();
  const finalNodes = nodeList.filter(node => {
    if (seen.has(node.node_id)) return false;
    seen.add(node.node_id);
    return true;
  });

  return finalNodes;
});

const toggleNode = async (nodeId: string) => {
  if (!nodeId || nodeId === 'undefined' || nodeId === 'null') {
    console.error('Invalid nodeId for toggle:', nodeId);
    return;
  }
  appStore.toggleNodeExpansion(nodeId);
};

const navigateToNode = async (nodeId: string) => {
  if (!nodeId || nodeId === 'undefined' || nodeId === 'null') {
    console.error('Invalid nodeId for navigation:', nodeId);
    return;
  }
  await appStore.navigateTo(nodeId);
};

onMounted(async () => {
  await appStore.initialize();
});
</script>
