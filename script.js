'use strict'

window.addEventListener('DOMContentLoaded', function() {
  const contact_buttons = document.getElementsByClassName('contact_via_email')
  for (let button of contact_buttons) {
    const location = button.dataset.location.replace(/ /g, '-').toLowerCase();
    const mailto = `mailto:${location}@tzm.one`
    button.setAttribute('href', mailto)
  }
});
