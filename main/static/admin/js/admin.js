function modifyDateTimeWidgets() {
  // Get nodeList of all p.datetime nodes
  const dateTimeWidgets = document.querySelectorAll('p.datetime');

  // Loop through dateTimeWidgets
  for (const dateTimeWidget of dateTimeWidgets) {

    // If screen is wider than 1024, remove br and add margin to end of first shortcuts
    if (window.screen.width >= 1024) {
      // Remove br
      const br = dateTimeWidget.querySelector('br');
      br.parentNode.removeChild(br);

      // Add some margin after first shortcuts
      const shortcuts = dateTimeWidget.querySelector('.datetimeshortcuts');
      shortcuts.style.marginRight = '1rem';
    }

    // Add max-width to inputs (mostly for mobile)
    const inputs = dateTimeWidget.querySelectorAll('input');
    for (const input of inputs) {
      input.style.maxWidth = '10rem';
    }

    // Get <a> node with "Now" text
    const nowLinkXPath = document.evaluate('.//a[contains(., "Now")]', dateTimeWidget, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
    const nowLink = nowLinkXPath.singleNodeValue;

    // Get <a> node with "Today" text
    const todayLinkXPath = document.evaluate('.//a[contains(., "Today")]', dateTimeWidget, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
    const todayLink = todayLinkXPath.singleNodeValue;

    // Add event listeners to the links that find the input, change its style, and that fade out the change
    nowLink.addEventListener('click', (e) => {

      // Force click todayLink when nowLink is clicked, so date gets updated too
      todayLink.click();

      // Flash green background
      const nowInput = nowLink.closest('p').querySelector('input.vTimeField');
      nowInput.style.backgroundColor = 'green';
      nowInput.style.color = 'white';
      setTimeout(function() {
        nowInput.style.backgroundColor='transparent';
        nowInput.style.transition='background-color .75s';
        nowInput.style.color = 'black';
      }, 500);
    });

    todayLink.addEventListener('click', (e) => {
      // Flash green background
      const todayInput = nowLink.closest('p').querySelector('input.vDateField');
      todayInput.style.backgroundColor = 'green';
      todayInput.style.color = 'white';
      setTimeout(function() {
        todayInput.style.backgroundColor='transparent';
        todayInput.style.transition='background-color .75s';
        todayInput.style.color = 'black';
      }, 500);
    });
  }
}

window.addEventListener('load', modifyDateTimeWidgets);