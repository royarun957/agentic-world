"""Styling constants for the digital twin Gradio app."""

EXAMPLES = [
    "Tell me about your background and experience.",
    "What kinds of projects are you working on now?",
    "What are your strongest technical skills?",
    "How can I get in touch with you?",
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --twin-accent: #ff6b57;
  --twin-accent-soft: rgba(255, 107, 87, 0.18);
  --twin-accent-hover: #ff8574;
  --twin-user: #ff6b57;
  --twin-user-deep: #e24d3d;
  --twin-mark: #3ecf9f;
  --twin-mark-soft: rgba(62, 207, 159, 0.18);
  --twin-bg: #0b1012;
  --twin-surface: rgba(16, 24, 26, 0.86);
  --twin-surface-solid: #12191b;
  --twin-surface-2: #1a272b;
  --twin-border: rgba(255, 255, 255, 0.08);
  --twin-border-strong: rgba(255, 255, 255, 0.14);
  --twin-text: #eef3f2;
  --twin-muted: #8b9694;
  --twin-radius: 16px;
  --twin-radius-sm: 10px;
  --twin-radius-pill: 999px;
  --twin-shadow: 0 18px 50px rgba(0, 0, 0, 0.38);
  --twin-glow-accent: rgba(255, 107, 87, 0.14);
  --twin-glow-mark: rgba(62, 207, 159, 0.14);
  --twin-glow-mist: rgba(255, 255, 255, 0.04);
}

/* Light mode: Gradio adds `.dark` to <body> when dark; absence = light.
   Neutrals flip; coral and seafoam accents stay the same. */
body:not(.dark) {
  --twin-bg: #f3f6f5;
  --twin-surface: rgba(255, 255, 255, 0.88);
  --twin-surface-solid: #ffffff;
  --twin-surface-2: #e7eeec;
  --twin-border: rgba(16, 28, 26, 0.08);
  --twin-border-strong: rgba(16, 28, 26, 0.14);
  --twin-text: #141c1b;
  --twin-muted: #66716f;
  --twin-shadow: 0 18px 44px rgba(20, 32, 30, 0.08);
  --twin-glow-accent: rgba(255, 107, 87, 0.16);
  --twin-glow-mark: rgba(62, 207, 159, 0.12);
  --twin-glow-mist: rgba(20, 32, 30, 0.04);
}

footer, .built-with, .show-api, .api-docs { display: none !important; }

html, body, gradio-app {
  background: var(--twin-bg) !important;
  color: var(--twin-text) !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  background-image:
    radial-gradient(ellipse 80% 50% at 8% -10%, var(--twin-glow-accent), transparent 55%),
    radial-gradient(ellipse 70% 45% at 96% 0%, var(--twin-glow-mark), transparent 50%),
    radial-gradient(ellipse 60% 40% at 50% 110%, var(--twin-glow-mist), transparent 55%) !important;
  background-attachment: fixed !important;
}

/* ---------- Stable layout ---------- */
.gradio-container {
  background: transparent !important;
  color: var(--twin-text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
  width: 100% !important;
  max-width: 840px !important;
  min-width: 0 !important;
  margin: 0 auto !important;
  padding: 36px 24px 56px !important;
}
.gradio-container .main, .gradio-container .contain, .gradio-container .wrap {
  width: 100% !important;
  max-width: 100% !important;
  min-width: 0 !important;
}
.gradio-container * { min-width: 0; }

/* ---------- Title + description ---------- */
.gradio-container h1 {
  color: var(--twin-text) !important;
  font-size: 30px !important;
  font-weight: 700 !important;
  letter-spacing: -0.04em !important;
  padding-left: 0 !important;
  margin: 8px 0 6px !important;
  text-align: left !important;
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
}
.gradio-container h1::before {
  content: '';
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--twin-mark);
  box-shadow: 0 0 0 4px var(--twin-mark-soft), 0 0 18px var(--twin-mark);
  flex-shrink: 0;
}
.gradio-container .prose p,
.gradio-container p.description,
.gradio-container [class*="description"] p {
  color: var(--twin-muted) !important;
  font-size: 15px !important;
  line-height: 1.55 !important;
  margin: 0 0 18px !important;
  max-width: 36em;
}

/* ---------- Block surfaces ---------- */
.block, .form {
  background: transparent !important;
  box-shadow: none !important;
  border-radius: var(--twin-radius) !important;
}

/* ---------- Hide the Chatbot label / header strip ---------- */
.chatbot > .block-label,
.chatbot > label,
.chatbot .label-wrap,
.chatbot .block-label,
.chatbot > .label-container {
  display: none !important;
}

/* ---------- Chatbot frame ---------- */
.chatbot, .chatbot.block {
  background: var(--twin-surface) !important;
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border: 1px solid var(--twin-border) !important;
  border-radius: var(--twin-radius) !important;
  min-height: 380px !important;
  box-shadow: var(--twin-shadow) !important;
  overflow: hidden !important;
}
.chatbot .placeholder, .chatbot .placeholder * {
  color: var(--twin-muted) !important;
  font-size: 14px !important;
}

/* ---------- Message rows: strip parent backgrounds ---------- */
.message-row,
.message-row > div,
.message-row .role,
.message-wrap, .bubble-wrap {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}

/* ---------- Reset borders on every bubble variant first ---------- */
.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  border: 0 !important;
  box-shadow: none !important;
  padding: 11px 14px !important;
  border-radius: 18px !important;
}

/* ---------- Bubble backgrounds (broad to cover Gradio variants) ---------- */
.message-row.user-row .message,
.message-row.user-row .message-bubble,
.message-row.user-row .bubble,
.message-row[data-role="user"] .message,
.message-row[data-role="user"] .message-bubble {
  background: linear-gradient(160deg, var(--twin-user) 0%, var(--twin-user-deep) 100%) !important;
  color: #ffffff !important;
  border-radius: 18px 18px 6px 18px !important;
}

.message-row.bot-row .message,
.message-row.bot-row .message-bubble,
.message-row.bot-row .bubble,
.message-row[data-role="assistant"] .message,
.message-row[data-role="assistant"] .message-bubble {
  background: var(--twin-surface-2) !important;
  color: var(--twin-text) !important;
  border-radius: 18px 18px 18px 6px !important;
}

/* ---------- Seafoam stripe ----------
   Apply to every common bubble class for assistant rows (we don't know which
   one the running Gradio uses), then suppress on any *nested* instance so the
   stripe lands on the outermost matching element only — exactly one stripe. */
.message-row.bot-row .message,
.message-row.bot-row .bubble,
.message-row.bot-row .message-bubble,
.message-row[data-role="assistant"] .message,
.message-row[data-role="assistant"] .bubble,
.message-row[data-role="assistant"] .message-bubble {
  box-shadow: inset 3px 0 0 var(--twin-mark) !important;
}

.message-row.bot-row .message .message,
.message-row.bot-row .message .bubble,
.message-row.bot-row .message .message-bubble,
.message-row.bot-row .bubble .message,
.message-row.bot-row .bubble .bubble,
.message-row.bot-row .bubble .message-bubble,
.message-row.bot-row .message-bubble .message,
.message-row.bot-row .message-bubble .bubble,
.message-row.bot-row .message-bubble .message-bubble,
.message-row[data-role="assistant"] .message .message,
.message-row[data-role="assistant"] .message .bubble,
.message-row[data-role="assistant"] .message .message-bubble,
.message-row[data-role="assistant"] .bubble .message,
.message-row[data-role="assistant"] .bubble .bubble,
.message-row[data-role="assistant"] .bubble .message-bubble,
.message-row[data-role="assistant"] .message-bubble .message,
.message-row[data-role="assistant"] .message-bubble .bubble,
.message-row[data-role="assistant"] .message-bubble .message-bubble {
  box-shadow: none !important;
  border-radius: 0 !important;
}

/* ---------- Uniform font size in bubbles ----------
   The "first paragraph different size" was caused by a leaky `.prose p:first-of-type`
   selector. Force every paragraph in a bubble to the same size. */
.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  font-size: 14.5px !important;
  line-height: 1.6 !important;
}
.message-row .message p,
.message-row .message-bubble p,
.message-row .bubble p,
.message-row .prose p {
  font-size: 14.5px !important;
  line-height: 1.6 !important;
  margin: 0 0 8px !important;
  color: inherit !important;
}
.message-row .message p:last-child,
.message-row .message-bubble p:last-child,
.message-row .bubble p:last-child,
.message-row .prose p:last-child { margin-bottom: 0 !important; }

/* Strip stray internal borders/backgrounds from anything inside a bubble */
.message-row .message *,
.message-row .message-bubble *,
.message-row .bubble * {
  background: transparent !important;
  border-color: transparent !important;
  box-shadow: none !important;
  color: inherit !important;
}
.message-row .message a,
.message-row .message-bubble a {
  color: var(--twin-mark) !important;
  text-decoration: none;
  border-bottom: 1px solid color-mix(in srgb, var(--twin-mark) 55%, transparent);
}
.message-row .message a:hover,
.message-row .message-bubble a:hover {
  border-bottom-color: var(--twin-mark);
}

/* ---------- Composer (input + send) ---------- */
.gr-group {
  background: var(--twin-surface) !important;
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border: 1px solid var(--twin-border) !important;
  border-radius: 20px !important;
  box-shadow: var(--twin-shadow) !important;
  padding: 6px !important;
  overflow: hidden;
}
.gr-group:focus-within {
  border-color: color-mix(in srgb, var(--twin-accent) 70%, var(--twin-border)) !important;
  box-shadow: var(--twin-shadow), 0 0 0 3px var(--twin-accent-soft) !important;
}
.styler {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  padding: 0 !important;
}
.row { align-items: stretch !important; gap: 8px !important; }
.block.padded { padding: 0 !important; border: 0 !important; }

.input-row,
.gr-input-row,
.chat-input-row,
form[class*="input"] { align-items: stretch !important; gap: 10px !important; }

textarea, input[type="text"] {
  background: transparent !important;
  border: 0 !important;
  border-radius: 14px !important;
  color: var(--twin-text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 14.5px !important;
  padding: 12px 14px !important;
  line-height: 1.45 !important;
  min-height: 44px !important;
  box-shadow: none !important;
  transition: border-color 0.16s ease, box-shadow 0.16s ease;
}
textarea:focus, input[type="text"]:focus {
  border-color: transparent !important;
  outline: none !important;
  box-shadow: none !important;
}
textarea:disabled, input[type="text"]:disabled { opacity: 0.72; }
textarea::placeholder, input::placeholder { color: var(--twin-muted) !important; }

/* ---------- Buttons ---------- */
button {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  letter-spacing: 0.01em !important;
  text-transform: none !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: var(--twin-radius-sm) !important;
  background: var(--twin-surface) !important;
  color: var(--twin-text) !important;
  padding: 0 16px !important;
  min-height: 44px !important;
  align-self: stretch !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer;
  transition: background 0.16s ease, color 0.16s ease, border-color 0.16s ease, transform 0.16s ease, box-shadow 0.16s ease;
}
button:hover {
  border-color: var(--twin-border-strong) !important;
  color: var(--twin-accent) !important;
  transform: translateY(-1px);
}

button.primary,
button[variant="primary"],
button.submit,
button.submit-button,
.submit-button,
button.lg.primary {
  background: var(--twin-accent) !important;
  border: 1px solid var(--twin-accent) !important;
  color: #ffffff !important;
  min-height: 44px !important;
  min-width: 44px !important;
  height: 44px !important;
  align-self: center !important;
  padding: 0 14px !important;
  border-radius: 14px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  box-shadow: 0 8px 22px rgba(255, 107, 87, 0.32) !important;
}
button.primary:hover,
button.submit:hover,
.submit-button:hover,
button.lg.primary:hover {
  background: var(--twin-accent-hover) !important;
  border-color: var(--twin-accent-hover) !important;
  color: #ffffff !important;
  transform: translateY(-1px);
}

/* ---------- Submit-button icon: center vertically and size correctly ---------- */
button.submit svg,
button.submit-button svg,
.submit-button svg,
button.primary svg,
button[variant="primary"] svg {
  width: 18px !important;
  height: 18px !important;
  margin: 0 auto !important;
  display: block !important;
  align-self: center !important;
  color: #ffffff !important;
  fill: currentColor !important;
  stroke: currentColor !important;
}

/* ---------- Examples ---------- */
.examples, .examples-holder, [data-testid="examples"] {
  background: transparent !important;
  padding: 0 !important;
  margin-top: 16px !important;
}
.examples table, .examples-table { background: transparent !important; border: 0 !important; }
.examples button, .example, .examples td button, [data-testid="examples"] button {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: var(--twin-radius-pill) !important;
  color: var(--twin-text) !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  padding: 9px 14px !important;
  text-align: left !important;
  min-height: 0 !important;
  align-self: auto !important;
  display: inline-block !important;
  box-shadow: none !important;
  backdrop-filter: blur(12px);
}
.examples button:hover, .example:hover, [data-testid="examples"] button:hover {
  border-color: color-mix(in srgb, var(--twin-mark) 55%, var(--twin-border)) !important;
  color: var(--twin-mark) !important;
  background: color-mix(in srgb, var(--twin-mark) 8%, var(--twin-surface)) !important;
  transform: translateY(-1px);
}

/* ---------- Icon buttons (clear, retry, copy) ---------- */
.icon-button, .chatbot .icon-button {
  color: var(--twin-muted) !important;
  background: transparent !important;
  border: 0 !important;
  border-radius: 8px !important;
  min-height: 0 !important;
  align-self: auto !important;
  padding: 6px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  box-shadow: none !important;
  transform: none !important;
}
.icon-button:hover, .chatbot .icon-button:hover {
  color: var(--twin-accent) !important;
  background: var(--twin-accent-soft) !important;
}

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: var(--twin-border-strong);
  border-radius: var(--twin-radius-pill);
}
::-webkit-scrollbar-thumb:hover { background: var(--twin-mark); }

/* ---------- Selection ---------- */
::selection { background: var(--twin-accent); color: #ffffff; }

/* ---------- Mobile ---------- */
@media (max-width: 640px) {
  .gradio-container { padding: 22px 14px 40px !important; }
  .gradio-container h1 { font-size: 24px !important; }
  .chatbot, .chatbot.block { min-height: 320px !important; border-radius: 14px !important; }
  textarea, input[type="text"], button.primary, button.submit, .submit-button {
    min-height: 44px !important;
  }
}
"""

JS = """
() => {
  document.title = 'Digital Twin';

  if (!document.getElementById('twin-fonts')) {
    const link = document.createElement('link');
    link.id = 'twin-fonts';
    link.rel = 'stylesheet';
    link.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap';
    document.head.appendChild(link);
  }

  const focusInput = () => {
    const areas = document.querySelectorAll('textarea');
    if (areas.length) areas[areas.length - 1].focus();
  };
  setTimeout(focusInput, 300);

  // Re-focus the message field whenever Gradio re-enables it
  // (i.e. after the assistant finishes responding).
  const watchTextarea = (area) => {
    if (area.dataset.twinWatched) return;
    area.dataset.twinWatched = '1';
    let wasDisabled = area.disabled || area.readOnly;
    new MutationObserver(() => {
      const isDisabled = area.disabled || area.readOnly;
      if (wasDisabled && !isDisabled) area.focus();
      wasDisabled = isDisabled;
    }).observe(area, { attributes: true, attributeFilter: ['disabled', 'readonly'] });
  };

  const scan = () => document.querySelectorAll('textarea').forEach(watchTextarea);
  setTimeout(scan, 500);
  new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
}
"""
