/* =============================================================
   codemirror-init.js  —  CodeMirror 6 IDE editor for ML Guide
   Loaded as <script type="module"> so ES imports work fine.
   No build step, no npm — pure CDN via esm.sh
   ============================================================= */

import { EditorState }         from 'https://esm.sh/@codemirror/state@6.4.1';
import { EditorView, keymap, lineNumbers, highlightActiveLine, highlightActiveLineGutter }
                                from 'https://esm.sh/@codemirror/view@6.26.3';
import { defaultKeymap, history, historyKeymap, indentWithTab }
                                from 'https://esm.sh/@codemirror/commands@6.6.0';
import { python }               from 'https://esm.sh/@codemirror/lang-python@6.1.6';
import { bracketMatching, indentOnInput }
                                from 'https://esm.sh/@codemirror/language@6.10.1';
import { autocompletion, closeBrackets }
                                from 'https://esm.sh/@codemirror/autocomplete@6.16.0';

// Map runnerId → EditorView instance so nav.js can read/write them
window.__cmEditors = {};

function mountEditor(runner) {
  const textarea = runner.querySelector('.code-input');
  if (!textarea) return;

  const runnerId = runner.id;
  const initialCode = textarea.value;

  // Store original for reset
  textarea.setAttribute('data-original', initialCode);

  const view = new EditorView({
    state: EditorState.create({
      doc: initialCode,
      extensions: [
        // Language
        python(),
        // Editing comfort
        history(),
        closeBrackets(),
        bracketMatching(),
        indentOnInput(),
        autocompletion({ activateOnTyping: false }),
        // Keymaps
        keymap.of([
          indentWithTab,
          ...defaultKeymap,
          ...historyKeymap,
        ]),
        // Gutter & line highlighting
        lineNumbers(),
        highlightActiveLine(),
        highlightActiveLineGutter(),
        // No internal theme — we style via CSS variables in style.css
        EditorView.theme({
          '&': { height: 'auto' },
          '.cm-scroller': { fontFamily: "'JetBrains Mono', monospace", fontSize: '12px', lineHeight: '1.8' },
          '.cm-content': { padding: '12px 6px 12px 0' },
          '.cm-gutters': { minWidth: '36px' },
          '.cm-lineNumbers .cm-gutterElement': { padding: '0 8px 0 4px', minWidth: '28px', textAlign: 'right' },
        }),
        // Update listener — keep textarea in sync so existing runCode() still works as fallback
        EditorView.updateListener.of(update => {
          if (update.docChanged) {
            textarea.value = view.state.doc.toString();
          }
        }),
      ],
    }),
    parent: runner, // mount inside the runner div, after the textarea
  });

  // Register globally for nav.js access
  window.__cmEditors[runnerId] = view;

  // Hide the raw textarea, show CM
  runner.classList.add('cm-active-runner');

  // Insert CM editor before the output pre, after the textarea
  const output = runner.querySelector('.code-output');
  if (output) runner.insertBefore(view.dom, output);
}

// Mount on all runners already in DOM, and watch for lazily-loaded runners
function mountAll() {
  document.querySelectorAll('.code-runner').forEach(runner => {
    if (!window.__cmEditors[runner.id]) mountAll_one(runner);
  });
}

function mountAll_one(runner) {
  if (!runner.id || window.__cmEditors[runner.id]) return;
  mountEditor(runner);
}

// Initial mount
document.addEventListener('DOMContentLoaded', mountAll);

// Watch for topic HTML injected dynamically via nav.js fetch
const observer = new MutationObserver(mutations => {
  mutations.forEach(m => {
    m.addedNodes.forEach(node => {
      if (node.nodeType !== 1) return;
      // The added node might be a section containing runners, or a runner itself
      node.querySelectorAll && node.querySelectorAll('.code-runner').forEach(r => {
        if (!window.__cmEditors[r.id]) mountEditor(r);
      });
      if (node.classList && node.classList.contains('code-runner') && !window.__cmEditors[node.id]) {
        mountEditor(node);
      }
    });
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('topic-container');
  if (container) observer.observe(container, { childList: true, subtree: true });
});

// Re-sync theme when toggleTheme() fires (CM reads CSS classes, so just force a redraw)
// We expose a helper nav.js can call
window.__cmSyncTheme = () => {
  Object.values(window.__cmEditors).forEach(view => view.requestMeasure());
};
