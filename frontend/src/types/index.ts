// API Response Types
export interface BaseResponse<T = any> {
  success: boolean;
  data: T;
  error?: string;
  metadata?: Record<string, any>;
}

export interface ModuleInfo {
  name: string;
  loaded: boolean;
  file_count: number;
}

export interface NodeInfo {
  node_id: string; // Unified to node_id
  label: string;
  type: string;
  title?: string;
  has_children?: boolean;
  content_preview?: string;
}

export interface NodeDetail extends NodeInfo {
  content?: string;
  module?: string;
  path?: string; // API uses 'path'
  line_number?: number;
  parent_id?: string;
  children_ids: string[];
  see_also: Array<{ node_id: string; label: string; description?: string; title?: string }>;
  formatted_content?: FormattedContent;
}

export interface BreadcrumbItem {
  id: string;
  label: string;
}

export interface FormattedContent {
  markdown?: string;
  text?: string;
  tree?: string;
  json_data?: any;
}

export interface NodeView {
  node: NodeDetail;
  formatted_content: FormattedContent;
}

export interface SearchResult {
  node_id: string;
  label: string;
  title?: string;
  type: string;
  file_id?: string;
  excerpt?: string;
}

// Store Types
export interface ModulesState {
  modules: ModuleInfo[];
  availableModules: string[];
  loadedModules: string[];
  loading: boolean;
}

export interface NavigationState {
  currentNode: NodeDetail | null;
  breadcrumb: BreadcrumbItem[];
  expandedNodes: Set<string>;
  loading: boolean;
  history: string[];
  historyCursor: number;
}

export interface SearchState {
  query: string;
  scope: 'all' | 'content' | 'title' | 'label';
  results: SearchResult[];
  loading: boolean;
  caseSensitive: boolean;
  wholeWord: boolean;
  useRegex: boolean;
}

export interface AppState {
  modules: ModulesState;
  navigation: NavigationState;
  search: SearchState;
  contentFormat: 'markdown' | 'text' | 'tree' | 'json';
  viewOptions: {
    depth: number;
    include_content: boolean;
    include_see_also: boolean;
    show_metadata: boolean;
    display_mode: 'none' | 'label' | 'full_id';
  };
}
