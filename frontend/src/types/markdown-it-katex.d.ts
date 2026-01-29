declare module 'markdown-it-katex' {
  import MarkdownIt from 'markdown-it';

  interface KatexOptions {
    throwOnError?: boolean;
    strict?: boolean | string | (errorCode: string) => boolean;
    trust?: boolean;
    macros?: { [key: string]: string };
    displayMode?: boolean;
  }

  function markdownItKatex(md: MarkdownIt, options?: KatexOptions): void;

  export default markdownItKatex;
}
