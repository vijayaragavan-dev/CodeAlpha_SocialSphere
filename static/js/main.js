document.addEventListener('DOMContentLoaded', function () {
  initDarkMode();
  initLikeButtons();
  initFlashDismiss();
  initFileUploadPreview();
  initOnlineStatus();
});

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

function initDarkMode() {
  const toggle = document.getElementById('darkModeToggle');
  if (!toggle) return;

  const stored = localStorage.getItem('darkMode');
  if (stored === 'true') {
    document.documentElement.setAttribute('data-theme', 'dark');
    toggle.innerHTML = '&#9790;';
  }

  toggle.addEventListener('click', function () {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const newMode = !isDark;

    document.documentElement.setAttribute('data-theme', newMode ? 'dark' : 'light');
    localStorage.setItem('darkMode', newMode);
    toggle.innerHTML = newMode ? '&#9790;' : '&#9788;';

    fetch('/toggle_dark_mode', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrf_token')
      },
      body: JSON.stringify({ dark_mode: newMode })
    }).catch(() => {});
  });
}

function initLikeButtons() {
  document.querySelectorAll('.like-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const postId = this.dataset.postId;
      const countEl = document.getElementById('like-count-' + postId);
      const heartIcon = this.querySelector('.heart-icon');

      fetch('/like/' + postId, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(function (res) {
        if (res.status === 401) {
          window.location.href = '/login?next=' + encodeURIComponent(window.location.pathname);
          throw new Error('Unauthorized');
        }
        return res.json();
      })
      .then(function (data) {
        if (data.liked) {
          btn.classList.add('liked');
        } else {
          btn.classList.remove('liked');
        }
        if (countEl) {
          countEl.textContent = data.count + ' like' + (data.count !== 1 ? 's' : '');
        }
      })
      .catch(function (err) {
        if (err.message !== 'Unauthorized') {
          console.error('Like error:', err);
        }
      });
    });
  });
}

function initFlashDismiss() {
  document.querySelectorAll('.alert-close').forEach(function (btn) {
    btn.addEventListener('click', function () {
      this.parentElement.remove();
    });
  });

  setTimeout(function () {
    document.querySelectorAll('.alert').forEach(function (el) {
      el.style.transition = 'opacity 0.5s ease';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 500);
    });
  }, 5000);
}

function initFileUploadPreview() {
  const fileInput = document.getElementById('imageInput');
  if (!fileInput) return;

  const preview = document.getElementById('imagePreview');
  const fileName = document.getElementById('fileName');

  fileInput.addEventListener('change', function () {
    if (this.files && this.files[0]) {
      const file = this.files[0];
      if (fileName) {
        fileName.textContent = file.name;
      }

      const reader = new FileReader();
      reader.onload = function (e) {
        if (preview) {
          preview.src = e.target.result;
          preview.classList.add('show');
        }
      };
      reader.readAsDataURL(file);
    }
  });
}

function initOnlineStatus() {
  document.querySelectorAll('[data-online-user]').forEach(function (el) {
    const userId = el.dataset.onlineUser;
    const dot = el.querySelector('.online-dot');
    const text = el.querySelector('.online-text');

    if (dot && text) {
      fetch('/online_status/' + userId)
        .then(function (res) { return res.json(); })
        .then(function (data) {
          if (data.is_online) {
            dot.className = 'online-dot online';
            text.textContent = 'Online';
          } else {
            dot.className = 'online-dot offline';
            text.textContent = data.last_seen;
          }
        })
        .catch(function () {});
    }
  });
}
