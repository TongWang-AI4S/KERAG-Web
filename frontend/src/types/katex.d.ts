declare module 'katex' {
  interface KatexOptions {
    throwOnError?: boolean;
    strict?: boolean | string | ((errorCode: string) => boolean);
    trust?: boolean;
    macros?: { [key: string]: string };
    displayMode?: boolean;
    output?: 'html' | 'mathml' | 'htmlAndMathml';
    leqno?: boolean;
    fleqn?: boolean;
    errorColor?: string;
    minRuleThickness?: number;
    maxSize?: number;
    maxExpand?: number;
  }

  function renderToString(tex: string, options?: KatexOptions): string;

  export { renderToString };
  export default { renderToString };
}
