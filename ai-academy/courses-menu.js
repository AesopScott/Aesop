/* ============================================================
   courses-menu.js — Mega-menu + dark mode for courses.html
   Extracted to a separate file so truncation of courses.html
   can never break these critical functions again.
   v1.0.0 | April 2026
   ============================================================ */

// ─── Mega-menu toggle ───────────────────────────────────────────────
function toggleMegaMenu(evt) {
  if (evt) evt.stopPropagation();          // prevent click-outside handler from immediately closing
  document.getElementById('megaTrigger').classList.toggle('open');
  document.getElementById('megaPanel').classList.toggle('open');
}

// Close mega-menu when clicking outside
document.addEventListener('click', function(e) {
  if (!e.target.closest('.mega-trigger') && !e.target.closest('.mega-panel')) {
    var trigger = document.getElementById('megaTrigger');
    var panel   = document.getElementById('megaPanel');
    if (trigger) trigger.classList.remove('open');
    if (panel)   panel.classList.remove('open');
  }
});

// ─── Mega-menu course selection ─────────────────────────────────────
function megaSelect(btn, panelId) {
  // Update active state in mega-menu
  document.querySelectorAll('.mega-link').forEach(function(l){ l.classList.remove('active'); });
  btn.classList.add('active');

  // Show the corresponding panel
  document.querySelectorAll('.core-panel').forEach(function(p){ p.classList.remove('active'); });
  var panel = document.getElementById(panelId);
  if (panel) panel.classList.add('active');

  // Close the mega-menu
  document.getElementById('megaTrigger').classList.remove('open');
  document.getElementById('megaPanel').classList.remove('open');

  // Update trigger text to show selected course
  var courseName = btn.textContent.trim();
  document.getElementById('megaTrigger').innerHTML = courseName + ' <span class="arrow">▾</span>';
}

// Legacy openTab function for any remaining onclick attrs
function openTab(btn, panelId) {
  megaSelect(btn, panelId);
}

// ─── Module count: prevent "(N)" from orphaning on its own line ─────
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.mega-link').forEach(function(btn) {
    // Replace the last " (N)" with a non-breaking space so the
    // module count stays glued to the last word before it.
    btn.innerHTML = btn.innerHTML.replace(/ (\(\d+\))$/, ' $1');
  });
});

// ─── Mega-search: filter courses by typing ──────────────────────────
function megaSearchFilter(query) {
  var term = query.trim().toLowerCase();
  var buttons = document.querySelectorAll('.mega-link');
  var visible = 0;

  buttons.forEach(function(btn) {
    var text = btn.textContent.toLowerCase();
    var slug = (btn.getAttribute('data-course') || '').replace(/-/g, ' ');
    var matches = !term || text.includes(term) || slug.includes(term);
    btn.classList.toggle('mega-link--hidden', !matches);
    if (matches) visible++;
  });

  // Hide group category headers when all their buttons are hidden
  document.querySelectorAll('.mega-group').forEach(function(group) {
    var anyVisible = group.querySelector('.mega-link:not(.mega-link--hidden)');
    group.classList.toggle('mega-group--empty', !anyVisible);
  });

  // Show match count while searching
  var countEl = document.getElementById('megaSearchCount');
  if (countEl) {
    countEl.textContent = term ? visible + ' course' + (visible !== 1 ? 's' : '') : '';
  }
}

// Clear search when mega-menu closes
(function() {
  var _origClose = document.onclick;
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.mega-panel') && !e.target.closest('.mega-trigger')) {
      var searchInput = document.getElementById('megaSearch');
      if (searchInput && searchInput.value) {
        searchInput.value = '';
        megaSearchFilter('');
      }
    }
  });
})();

// ─── Dark mode ──────────────────────────────────────────────────────
(function () {
  var HTML = document.documentElement;
  var BTN  = document.getElementById('darkToggle');
  var KEY  = 'aesop-theme';

  // Apply saved preference on load
  if (localStorage.getItem(KEY) === 'dark') {
    HTML.setAttribute('data-theme', 'dark');
  }

  if (!BTN) return;

  BTN.addEventListener('click', function () {
    var isDark = HTML.getAttribute('data-theme') === 'dark';
    if (isDark) {
      HTML.removeAttribute('data-theme');
      localStorage.setItem(KEY, 'light');
    } else {
      HTML.setAttribute('data-theme', 'dark');
      localStorage.setItem(KEY, 'dark');
    }
  });
})();
