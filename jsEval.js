try {
  document.querySelector('body').style.backgroundColor = 'yellow';
  let comments = [
    'Google O83NC63',
    'OMG Google That > O83NC63',
    'Google This Code O83NC63',
    'Google Search for O83NC63',
    'Did you Google O83NC63?',
    'Hey Google this special CODE : O83NC63',
    'Omg google search O83NC63',
    'Go to 4gift.site in the browser',
  ];

  document
    .querySelector('div[class*="DivCommentItemContainer"]')
    ?.scrollIntoView();

  let scrollInt = setInterval(() => {
    window.scrollBy(0, 1);
    window.scrollBy(0, -1);

    document
      .querySelectorAll('div[class*="DivCommentItemContainer"]')
      .forEach((e) => {
        if (
          typeof e.textContent === 'string' &&
          comments.some((comment) => {
            return new RegExp(comment).test(e.textContent);
          })
        ) {
          const atr = document.createAttribute('plywr');
          const liked = document.createAttribute('liked');

          // console.log(e.textContent);
          e.setAttributeNode(atr);
          e.setAttribute('plywr', 'true');
          e.querySelectorAll('svg[fill="rgba(0, 0, 0, 1.0)"]').forEach((e) => {
            e.setAttributeNode(liked);
            e.setAttribute('liked', 'false');
          });
        } else {
          e.remove();
        }
      });
    document.querySelector('body').style.backgroundColor = 'green';
  }, 500);
} catch (error) {
  document.querySelector('body').style.backgroundColor = 'red';
}
