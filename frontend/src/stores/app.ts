import { defineStore } from 'pinia';
import type {
  AppState,
  NodeDetail,
  NodeInfo,
} from '@/types';
import { api } from '@/api/client';

// Extended state
interface ExtendedAppState extends AppState {
  moduleRoots: Record<string, NodeDetail | NodeDetail[]>;
  nodeChildren: Record<string, string[]>; // IDs
  nodeChildrenInfo: Record<string, NodeInfo[]>; // Detailed objects for tree rendering
  nodeCache: Record<string, { node: NodeDetail, breadcrumb: any[] }>;
}

export const useAppStore = defineStore('app', {
  state: (): ExtendedAppState => ({
    modules: {
      modules: [],
      availableModules: [],
      loadedModules: [],
      loading: false
    },
    navigation: {
      currentNode: null,
      breadcrumb: [],
      expandedNodes: new Set<string>(['::ROOT']),
      loading: false,
      history: [],
      historyCursor: -1
    },
    search: {
      query: '',
      scope: 'all',
      results: [],
      loading: false,
      caseSensitive: false,
      wholeWord: false,
      useRegex: false
    },
    contentFormat: 'markdown',
    viewOptions: {
      depth: 1,
      include_content: true,
      include_see_also: true,
      show_metadata: false,
      display_mode: 'none'
    },
    moduleRoots: {},
    nodeChildren: {},
    nodeChildrenInfo: {},
    nodeCache: {}
  }),

  actions: {
    // Initialize app
    async initialize() {
      await this.loadModules();
      await this.loadCurrentNode();
    },

    // Module actions
    async loadModules() {
      this.modules.loading = true;
      try {
        const response = await api.getModules();
        if (response.success) {
          this.modules.modules = response.data.modules;
          this.modules.availableModules = response.data.available_modules;
          this.modules.loadedModules = response.data.loaded_modules;

          // Load root nodes for all loaded modules
          await this.loadLoadedModuleRoots();
        }
      } catch (error) {
        console.error('Failed to load modules:', error);
      } finally {
        this.modules.loading = false;
      }
    },

    async loadLoadedModuleRoots() {
      try {
        const response = await api.getLoadedModuleRoots();
        if (response.success) {
          // Clear old roots and store new ones
          this.moduleRoots = {};
          response.data.forEach(root => {
            if (root.module) {
              if (this.moduleRoots[root.module]) {
                if (!Array.isArray(this.moduleRoots[root.module])) {
                  this.moduleRoots[root.module] = [this.moduleRoots[root.module] as NodeDetail];
                }
                (this.moduleRoots[root.module] as NodeDetail[]).push(root);
              } else {
                this.moduleRoots[root.module] = root;
              }
            }
          });
        }
      } catch (e) {
        console.warn('Failed to load loaded module roots:', e);
      }
    },

    async loadModule(name: string) {
      this.modules.loading = true;
      try {
        const response = await api.loadModule(name);
        if (response.success) {
          await this.loadModules();
          await this.loadCurrentNode();
        }
      } catch (error) {
        console.error('Failed to load module:', error);
      } finally {
        this.modules.loading = false;
      }
    },

    async unloadModule(name: string) {
      this.modules.loading = true;
      try {
        const response = await api.unloadModule(name);
        if (response.success) {
          delete this.moduleRoots[name];
          await this.loadModules();
          await this.loadCurrentNode();
        }
      } catch (error) {
        console.error('Failed to unload module:', error);
      } finally {
        this.modules.loading = false;
      }
    },

    async purgeModules() {
      this.modules.loading = true;
      try {
        const response = await api.purgeModules();
        if (response.success) {
          this.moduleRoots = {};
          await this.loadModules();
          await this.loadCurrentNode();
        }
      } catch (error) {
        console.error('Failed to purge modules:', error);
      } finally {
        this.modules.loading = false;
      }
    },

    // Navigation actions
    async loadCurrentNode() {
      this.navigation.loading = true;
      try {
        const response = await api.getCurrentNode();
        if (response.success) {
          this.navigation.currentNode = response.data;
          this.navigation.breadcrumb = response.metadata?.breadcrumb || [];

          // Fetch full history metadata
          const histRes = await api.getHistory();
          if (histRes.success) {
            this.navigation.history = histRes.data.items;
            this.navigation.historyCursor = histRes.data.cursor;

            // Pre-fetch titles for history items if not in cache
            for (const id of this.navigation.history) {
               if (!this.nodeCache[id]) {
                 // Non-blocking fetch to populate cache
                 api.getNodeDetail(id, 0).then(res => {
                    if (res.success) {
                      this.nodeCache[id] = { node: res.data.node, breadcrumb: [] };
                    }
                 });
               }
            }
          }

          // Also fetch full view with current options
          await this.fetchNodeView();
        }
      } catch (error) {
        console.error('Failed to load current node:', error);
      } finally {
        this.navigation.loading = false;
      }
    },

    async fetchNodeView() {
      if (!this.navigation.currentNode) return;
      try {
        const response = await api.getNodeDetail(
          this.navigation.currentNode.node_id,
          this.viewOptions.depth,
          this.contentFormat,
          this.viewOptions
        );
        if (response.success) {
          // Merge formatted content into the current node
          this.navigation.currentNode = {
            ...response.data.node,
            formatted_content: response.data.formatted_content
          };
        }
      } catch (error) {
        console.error('Failed to fetch node view:', error);
      }
    },

    async loadNodeChildren(nodeId: string) {
      console.log(`[Store] Loading children for: ${nodeId}`);
      try {
        // 1. Get raw ID list
        const idResponse = await api.getChildren(nodeId);
        if (idResponse.success) {
          console.log(`[Store] IDs received for ${nodeId}:`, idResponse.data);
          this.nodeChildren = {
            ...this.nodeChildren,
            [nodeId]: idResponse.data
          };
        }

        // 2. Get detailed preview for tree rendering
        const previewResponse = await api.previewChildren(nodeId);
        if (previewResponse.success) {
          console.log(`[Store] Previews received for ${nodeId}:`, previewResponse.data);
          this.nodeChildrenInfo = {
            ...this.nodeChildrenInfo,
            [nodeId]: previewResponse.data
          };
        }
      } catch (error) {
        console.error('Failed to load node children:', error);
      }
    },

    async navigateTo(target: string) {
      if (!target || target === 'undefined') return;

      this.navigation.loading = true;
      try {
        // 1. Resolve target to full node ID first
        const resolveRes = await api.resolveNodeId(target);
        if (!resolveRes.success) {
          throw new Error(resolveRes.error || 'Failed to resolve ID');
        }

        if (resolveRes.data.candidates && resolveRes.data.candidates.length > 1) {
          throw new Error(`Ambiguous ID: ${target}. Found ${resolveRes.data.candidates.length} candidates.`);
        }

        const targetId = resolveRes.data.node_id || resolveRes.data.id;
        if (!targetId) {
          throw new Error(`Could not resolve ID: ${target}`);
        }

        // Use resolved ID for cache lookup
        if (this.nodeCache[targetId]) {
          const cached = this.nodeCache[targetId];
          this.navigation.currentNode = cached.node;
          this.navigation.breadcrumb = cached.breadcrumb;
        }

        const response = await api.getNodeDetail(
          targetId,
          this.viewOptions.depth,
          this.contentFormat,
          this.viewOptions
        );

        if (response.success) {
          const updatedNode = {
            ...response.data.node,
            formatted_content: response.data.formatted_content
          };

          this.navigation.currentNode = updatedNode;

          const navResponse = await api.navigateTo(targetId);
          if (navResponse.success) {
            // Only update breadcrumb and history if not already at target
            if (!navResponse.data.already_at_target) {
              this.navigation.breadcrumb = navResponse.metadata?.breadcrumb || [];

              // Refresh modules list as navigation might have triggered lazy loading
              await this.loadModules();

              // Refresh history
              const histRes = await api.getHistory();
              if (histRes.success) {
                this.navigation.history = histRes.data.items;
                this.navigation.historyCursor = histRes.data.cursor;
              }
            }
          }

          // Always cache using the resolved targetId
          this.nodeCache = {
            ...this.nodeCache,
            [targetId]: {
              node: updatedNode,
              breadcrumb: this.navigation.breadcrumb
            }
          };

          if (updatedNode.type === 'section' && updatedNode.has_children) {
            await this.loadNodeChildren(updatedNode.node_id);
          }
        }
      } catch (error: any) {
        console.error('Failed to navigate:', error);
        // Optional: show a user-friendly error message if you have a notification system
      } finally {
        this.navigation.loading = false;
      }
    },

    async navigateBack(steps: number = 1) {
      this.navigation.loading = true;
      try {
        const response = await api.navigateBack(steps);
        if (response.success) {
          this.navigation.currentNode = response.data;
          this.navigation.breadcrumb = response.metadata?.breadcrumb || [];
          // Refresh history state
          const histRes = await api.getHistory();
          if (histRes.success) {
            this.navigation.historyCursor = histRes.data.cursor;
          }
        }
      } catch (error) {
        console.error('Failed to navigate back:', error);
      } finally {
        this.navigation.loading = false;
      }
    },

    async navigateForward(steps: number = 1) {
      this.navigation.loading = true;
      try {
        const response = await api.navigateForward(steps);
        if (response.success) {
          this.navigation.currentNode = response.data;
          this.navigation.breadcrumb = response.metadata?.breadcrumb || [];
          // Refresh history state
          const histRes = await api.getHistory();
          if (histRes.success) {
            this.navigation.historyCursor = histRes.data.cursor;
          }
        }
      } catch (error) {
        console.error('Failed to navigate forward:', error);
      } finally {
        this.navigation.loading = false;
      }
    },

    async navigateUp(levels: number = 1) {
      this.navigation.loading = true;
      try {
        const response = await api.navigateUp(levels);
        if (response.success) {
          this.navigation.currentNode = response.data;
          this.navigation.breadcrumb = response.metadata?.breadcrumb || [];
        }
      } catch (error) {
        console.error('Failed to navigate up:', error);
      } finally {
        this.navigation.loading = false;
      }
    },

    toggleNodeExpansion(nodeId: string) {
      if (!nodeId || nodeId === 'undefined') return;
      const newExpandedNodes = new Set(this.navigation.expandedNodes);
      if (newExpandedNodes.has(nodeId)) {
        newExpandedNodes.delete(nodeId);
      } else {
        newExpandedNodes.add(nodeId);
      }
      this.navigation.expandedNodes = newExpandedNodes;
    },

    async performSearch(query: string, scope: 'all' | 'content' | 'title' | 'label' = 'all') {
      this.search.query = query;
      this.search.scope = scope;
      this.search.loading = true;
      try {
        // Pass all search options from the store state
        const response = await api.search(
          query,
          scope,
          50, // maxResults
          this.search.wholeWord,
          this.search.caseSensitive,
          this.search.useRegex
        );
        if (response.success) {
          this.search.results = response.data;
        }
      } catch (error) {
        console.error('Search failed:', error);
        this.search.results = [];
      } finally {
        this.search.loading = false;
      }
    },

    clearSearch() {
      this.search.query = '';
      this.search.results = [];
    }
  }
});
