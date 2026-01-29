import axios, { AxiosInstance } from 'axios';
import type {
  BaseResponse,
  ModuleInfo,
  NodeDetail,
  NodeView,
  BreadcrumbItem,
  SearchResult,
  NodeInfo
} from '@/types';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
      timeout: 10000,
    });
  }

  // Modules
  async getModules(): Promise<BaseResponse<{
    modules: ModuleInfo[];
    available_modules: string[];
    loaded_modules: string[];
  }>> {
    const response = await this.client.get('/modules/');
    return response.data;
  }

  async loadModule(name: string): Promise<BaseResponse<any>> {
    const response = await this.client.post('/modules/load', null, {
      params: { module_name: name }
    });
    return response.data;
  }

  async unloadModule(name: string): Promise<BaseResponse<any>> {
    const response = await this.client.delete('/modules/unload', {
      params: { module_name: name }
    });
    return response.data;
  }

  async purgeModules(): Promise<BaseResponse<any>> {
    const response = await this.client.post('/modules/purge');
    return response.data;
  }

  async getLoadedModuleRoots(): Promise<BaseResponse<NodeDetail[]>> {
    const response = await this.client.get('/modules/roots');
    return response.data;
  }

  // Nodes
  async getCurrentNode(): Promise<BaseResponse<NodeDetail>> {
    const response = await this.client.get('/nodes/current/');
    return response.data;
  }

  async navigateTo(target: string): Promise<BaseResponse<NodeDetail>> {
    const response = await this.client.post(`/nodes/navigate?target=${encodeURIComponent(target)}`);
    return response.data;
  }

  async navigateBack(steps: number = 1): Promise<BaseResponse<NodeDetail>> {
    const response = await this.client.post('/nodes/back', null, {
      params: { steps }
    });
    return response.data;
  }

  async navigateForward(steps: number = 1): Promise<BaseResponse<NodeDetail>> {
    const response = await this.client.post('/nodes/forward', null, {
      params: { steps }
    });
    return response.data;
  }

  async navigateUp(levels: number = 1): Promise<BaseResponse<NodeDetail>> {
    const response = await this.client.post('/nodes/up', null, {
      params: { levels }
    });
    return response.data;
  }

  async resolveNodeId(target: string): Promise<BaseResponse<{ id?: string, node_id?: string, candidates?: any[] }>> {
    const response = await this.client.get('/nodes/resolve', {
      params: { target }
    });
    return response.data;
  }

  async getNodeDetail(
    id: string,
    depth: number = 1,
    format: string = 'text',
    options: any = {}
  ): Promise<BaseResponse<NodeView>> {
    const response = await this.client.get('/nodes/detail', {
      params: {
        node_id: id,
        depth,
        format,
        include_content: options.include_content,
        include_see_also: options.include_see_also,
        show_metadata: options.show_metadata,
        display_mode: options.display_mode
      }
    });
    return response.data;
  }

  async getChildren(id: string): Promise<BaseResponse<string[]>> {
    const response = await this.client.get('/nodes/children', {
      params: {
        node_id: id
      }
    });
    return response.data;
  }

  async previewChildren(
    id: string,
    nodeType: string = 'all',
    sortBy: string = 'order'
  ): Promise<BaseResponse<NodeInfo[]>> {
    const response = await this.client.get('/nodes/preview_children', {
      params: {
        node_id: id,
        node_type: nodeType,
        sort_by: sortBy
      }
    });
    return response.data;
  }

  // Search
  async search(
    q: string,
    scope: 'all' | 'content' | 'title' | 'label' = 'all',
    maxResults: number = 50,
    wholeWord: boolean = false,
    caseSensitive: boolean = false,
    useRegex: boolean = false
  ): Promise<BaseResponse<SearchResult[]>> {
    const response = await this.client.get('/search', {
      params: {
        q,
        scope,
        max_results: maxResults,
        whole_word: wholeWord,
        case_sensitive: caseSensitive,
        use_regex: useRegex
      }
    });
    return response.data;
  }

  // Status
  async getStatus(): Promise<BaseResponse<any>> {
    const response = await this.client.get('/status');
    return response.data;
  }

  async getHistory(): Promise<BaseResponse<{
    items: string[];
    cursor: number;
    size: number;
  }>> {
    const response = await this.client.get('/nodes/history');
    return response.data;
  }

  async getSettings(): Promise<BaseResponse<{
    kerag_home: string
    kerag_local: string
    kerag_lang: string
  }>> {
    const response = await this.client.get('/settings/')
    return response.data
  }

  async applySettings(settings: {
    kerag_home: string
    kerag_local: string
    kerag_lang: string
  }): Promise<BaseResponse<any>> {
    const response = await this.client.post('/settings/apply', settings)
    return response.data
  }
}

export const api = new APIClient();
