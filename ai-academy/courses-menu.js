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

// ─── Mega-search: live typeahead results list ────────────────────────
function megaSearchFilter(query) {
  var term      = query.trim().toLowerCase();
  var panel     = document.getElementById('megaPanel');
  var resultsEl = document.getElementById('megaSearchResults');
  var countEl   = document.getElementById('megaSearchCount');

  if (!term) {
    // No query — restore the normal grid view
    if (panel)     panel.classList.remove('mega-panel--searching');
    if (resultsEl) resultsEl.innerHTML = '';
    if (countEl)   countEl.textContent = '';
    return;
  }

  // Switch to search mode: grid hides, results list shows
  if (panel) panel.classList.add('mega-panel--searching');

  // Collect matching buttons with their category label and live status
  var results = [];
  document.querySelectorAll('.mega-link').forEach(function(btn) {
    var text = btn.textContent.toLowerCase();
    var slug = (btn.getAttribute('data-course') || '').replace(/-/g, ' ');
    if (text.includes(term) || slug.includes(term)) {
      var group = btn.closest('.mega-group');
      var catEl = group ? group.querySelector('.mega-cat') : null;
      var cat   = catEl ? catEl.textContent.trim() : '';
      results.push({
        btn:   btn,
        label: btn.textContent.trim(),
        cat:   cat,
        live:  btn.classList.contains('mega-link--live')
      });
    }
  });

  // Render results list
  if (!resultsEl) return;

  if (results.length === 0) {
    resultsEl.innerHTML =
      '<div class="mega-no-results">No courses match "' +
      query.trim().replace(/</g, '&lt;') + '"</div>';
  } else {
    resultsEl.innerHTML = results.map(function(r, i) {
      return (
        '<div class="mega-result-item" data-idx="' + i + '">' +
          '<span class="mega-result-cat">' + r.cat + '</span>' +
          '<span class="mega-result-name">' + r.label + '</span>' +
          '<span class="mega-result-badge mega-result-badge--' +
            (r.live ? 'live' : 'soon') + '">' +
            (r.live ? 'Live' : 'Soon') +
          '</span>' +
        '</div>'
      );
    }).join('');

    // Wire up click handlers after rendering
    resultsEl.querySelectorAll('.mega-result-item').forEach(function(el, i) {
      el.addEventListener('click', function() {
        var r = results[i];
        megaSelect(r.btn, r.btn.getAttribute('data-panel'));
        // Clear search state
        var inp = document.getElementById('megaSearch');
        if (inp) { inp.value = ''; megaSearchFilter(''); }
      });
    });
  }

  if (countEl) {
    countEl.textContent =
      results.length + ' course' + (results.length !== 1 ? 's' : '');
  }
}

// Clear search when mega-menu closes (click outside)
document.addEventListener('click', function(e) {
  if (!e.target.closest('.mega-panel') && !e.target.closest('.mega-trigger')) {
    var inp = document.getElementById('megaSearch');
    if (inp && inp.value) { inp.value = ''; megaSearchFilter(''); }
  }
});

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
