<template>
  <div class="markdown-body custom-markdown" v-html="renderedContent"></div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import MarkdownIt from 'markdown-it';
import 'github-markdown-css/github-markdown-light.css';

const props = defineProps<{
  content: string;
}>();

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
});

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

const renderedContent = computed(() => {
  if (!props.content) return '';
  try {
    return md.render(props.content);
  } catch (error) {
    console.warn('Markdown rendering failed:', error);
    return `<pre class="markdown-error">${escapeHtml(props.content)}</pre>`;
  }
});
</script>

<style scoped>
.custom-markdown {
  padding: 1rem;
  font-size: 15px;
  line-height: 1.6;
  background-color: transparent;
}

.markdown-body {
  box-sizing: border-box;
  min-width: 200px;
  max-width: 100%;
}

:deep(.markdown-error) {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: monospace;
  background-color: #f6f8fa;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
}
</style>
