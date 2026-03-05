/* theme.js — Coduel theme picker
   Include this script at the end of <body> on every page.
*/
(function () {
    const STORAGE_KEY = 'coduel-theme';

    const THEMES = [
        { id: 'rose', name: 'Rose', c1: '#7d4e57', c2: '#a06070' },
        { id: 'ocean', name: 'Ocean', c1: '#0284c7', c2: '#38bdf8' },
        { id: 'forest', name: 'Forest', c1: '#15803d', c2: '#4ade80' },
        { id: 'violet', name: 'Violet', c1: '#7c3aed', c2: '#a78bfa' },
        { id: 'amber', name: 'Amber', c1: '#b45309', c2: '#fbbf24' },
    ];

    /* Apply theme immediately to avoid flash-of-wrong-theme */
    const saved = localStorage.getItem(STORAGE_KEY) || 'rose';
    document.documentElement.setAttribute('data-theme', saved);

    function applyTheme(id) {
        document.documentElement.setAttribute('data-theme', id);
        localStorage.setItem(STORAGE_KEY, id);
        document.querySelectorAll('.tp-swatch').forEach(sw => {
            const active = sw.dataset.theme === id;
            sw.classList.toggle('tp-active', active);
            sw.setAttribute('aria-pressed', String(active));
        });
        /* Also update logo gradient if it's a CSS-var-based element */
        const logoEl = document.querySelector('.logo-title');
        if (logoEl) {
            /* Force repaint so gradient var picks up */
            logoEl.style.display = 'none';
            void logoEl.offsetHeight;
            logoEl.style.display = '';
        }
    }

    function buildPicker() {
        /* ── Styles ── */
        const style = document.createElement('style');
        style.textContent = `
      #tp-btn {
        position: fixed;
        bottom: 74px; right: 22px;
        z-index: 9999;
        width: 44px; height: 44px;
        border-radius: 50%;
        border: 1px solid rgba(255,255,255,0.1);
        background: rgba(13,16,23,0.85);
        color: #fff;
        font-size: 1.15rem;
        cursor: pointer;
        display: flex; align-items: center; justify-content: center;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 6px 24px rgba(0,0,0,0.45);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        outline: none;
      }
      #tp-btn:hover { transform: scale(1.1); box-shadow: 0 10px 32px rgba(0,0,0,0.55); }
      #tp-btn:focus-visible { outline: 2px solid var(--accent, #7d4e57); outline-offset: 3px; }

      #tp-panel {
        position: fixed;
        bottom: 126px; right: 22px;
        z-index: 9999;
        background: rgba(10,13,20,0.92);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 14px 14px 12px;
        display: none;
        flex-direction: column;
        gap: 11px;
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.55);
        min-width: 170px;
      }
      #tp-panel.tp-open {
        display: flex;
        animation: tpIn 0.2s cubic-bezier(0.25,0.46,0.45,0.94) both;
      }
      @keyframes tpIn {
        from { opacity: 0; transform: translateY(12px) scale(0.97); }
        to   { opacity: 1; transform: translateY(0)    scale(1); }
      }

      .tp-label {
        font-size: 0.62rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.25);
        user-select: none;
        padding: 0 2px;
      }

      .tp-swatches {
        display: flex;
        gap: 8px;
        align-items: center;
      }

      .tp-swatch {
        width: 28px; height: 28px;
        border-radius: 50%;
        border: 2px solid transparent;
        cursor: pointer;
        transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
        position: relative;
        outline: none;
        flex-shrink: 0;
      }
      .tp-swatch:hover { transform: scale(1.18); }
      .tp-swatch:focus-visible { outline: 2px solid #fff; outline-offset: 2px; }
      .tp-swatch.tp-active {
        border-color: rgba(255,255,255,0.9);
        box-shadow: 0 0 0 3px rgba(255,255,255,0.12);
        transform: scale(1.08);
      }
      /* Checkmark on active */
      .tp-swatch.tp-active::after {
        content: '✓';
        position: absolute;
        inset: 0;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.65rem;
        font-weight: 900;
        color: #fff;
        text-shadow: 0 1px 3px rgba(0,0,0,0.6);
        /* pseudo flex trick */
        display: grid; place-items: center;
        line-height: 1;
      }

      .tp-names {
        display: flex;
        gap: 8px;
        align-items: center;
      }
      .tp-name-item {
        flex: 0 0 28px;
        text-align: center;
        font-size: 0.55rem;
        font-weight: 600;
        color: rgba(255,255,255,0.3);
        letter-spacing: 0.04em;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        transition: color 0.15s;
      }
      .tp-name-item.tp-active { color: rgba(255,255,255,0.7); }
    `;
        document.head.appendChild(style);

        /* ── Button ── */
        const btn = document.createElement('button');
        btn.id = 'tp-btn';
        btn.title = 'Change theme';
        btn.setAttribute('aria-label', 'Open theme picker');
        btn.innerHTML = '🎨';

        /* ── Panel ── */
        const panel = document.createElement('div');
        panel.id = 'tp-panel';
        panel.setAttribute('role', 'dialog');
        panel.setAttribute('aria-label', 'Theme picker');

        const label = document.createElement('div');
        label.className = 'tp-label';
        label.textContent = 'Theme';

        const swatchRow = document.createElement('div');
        swatchRow.className = 'tp-swatches';

        const nameRow = document.createElement('div');
        nameRow.className = 'tp-names';

        const current = localStorage.getItem(STORAGE_KEY) || 'rose';

        THEMES.forEach(t => {
            const sw = document.createElement('button');
            sw.className = 'tp-swatch' + (t.id === current ? ' tp-active' : '');
            sw.dataset.theme = t.id;
            sw.title = t.name;
            sw.setAttribute('aria-pressed', String(t.id === current));
            sw.style.background = `linear-gradient(135deg, ${t.c1}, ${t.c2})`;
            sw.addEventListener('click', () => applyTheme(t.id));
            swatchRow.appendChild(sw);

            const nm = document.createElement('div');
            nm.className = 'tp-name-item' + (t.id === current ? ' tp-active' : '');
            nm.dataset.themeLabel = t.id;
            nm.textContent = t.name;
            nameRow.appendChild(nm);
        });

        panel.appendChild(label);
        panel.appendChild(swatchRow);
        panel.appendChild(nameRow);

        document.body.appendChild(btn);
        document.body.appendChild(panel);

        /* Toggle panel */
        btn.addEventListener('click', e => {
            e.stopPropagation();
            panel.classList.toggle('tp-open');
        });

        /* Close when clicking outside */
        document.addEventListener('click', e => {
            if (!panel.contains(e.target) && e.target !== btn) {
                panel.classList.remove('tp-open');
            }
        });

        /* Keyboard: Escape */
        document.addEventListener('keydown', e => {
            if (e.key === 'Escape') panel.classList.remove('tp-open');
        });

        /* Sync name labels when theme changes */
        const origApply = applyTheme;
        window._applyTheme = id => {
            origApply(id);
            document.querySelectorAll('.tp-name-item').forEach(nm => {
                nm.classList.toggle('tp-active', nm.dataset.themeLabel === id);
            });
        };
        swatchRow.querySelectorAll('.tp-swatch').forEach(sw => {
            sw.addEventListener('click', () => {
                document.querySelectorAll('.tp-name-item').forEach(nm => {
                    nm.classList.toggle('tp-active', nm.dataset.themeLabel === sw.dataset.theme);
                });
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', buildPicker);
    } else {
        buildPicker();
    }
})();
