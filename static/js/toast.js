(function () {
  'use strict';

  var ICONS = {
    success: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" fill="#4caf50"/><path d="M8 12.5l2.5 2.5L16 9.5" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    error: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" fill="#dc3545"/><path d="M9 9l6 6M15 9l-6 6" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/></svg>',
    danger: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" fill="#dc3545"/><path d="M9 9l6 6M15 9l-6 6" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/></svg>',
    warning: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" fill="#f59e0b"/><path d="M12 8v4.5M12 15.5h.01" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/></svg>',
    info: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" fill="#0d6efd"/><path d="M12 11v5M12 8h.01" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/></svg>'
  };

  function getStack() {
    var stack = document.querySelector('.toast-stack');
    if (!stack) {
      stack = document.createElement('div');
      stack.className = 'toast-stack';
      document.body.appendChild(stack);
    }
    return stack;
  }

  window.showToast = function (message, type) {
    type = (type || 'success').toLowerCase();
    if (!ICONS[type]) {
      type = 'success';
    }

    var toast = document.createElement('div');
    toast.className = 'toast-item toast-' + type;
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');

    var icon = document.createElement('span');
    icon.className = 'toast-icon';
    icon.innerHTML = ICONS[type];

    var text = document.createElement('span');
    text.className = 'toast-msg';
    text.textContent = message;

    toast.appendChild(icon);
    toast.appendChild(text);
    getStack().appendChild(toast);

    setTimeout(function () {
      toast.classList.add('hide');
      setTimeout(function () {
        if (toast.parentNode) {
          toast.parentNode.removeChild(toast);
        }
      }, 350);
    }, 4000);
  };

  document.addEventListener('DOMContentLoaded', function () {
    var items = document.querySelectorAll('[data-toast-message]');
    [].forEach.call(items, function (el) {
      window.showToast(
        el.getAttribute('data-toast-message'),
        el.getAttribute('data-toast-type') || 'success'
      );
    });
  });
})();