try {
  document.querySelector('body').style.backgroundColor = 'yellow';
  let comments = [
    '1 New',
    '(1)New Gift',
    'New notification',
    '1 New Surprise!',
    'New surprize',
    'You got a new present',
    'Did you take the Gift?',
    'Did you take a Gift?',
    'Did you take your Gift?',
    'Did you take the present?',
    'Come Get your present!',
    'One new present',
    'Thats Awsome!',
    '1 New Gift',
    'New Gift',
    'You got a new message',
    'New Message',
    'Messages(1)',
    'You have received 1 new present.',
    'Open New Message',
    'Open (1) new gifts!',
    'New (1)',
    'New 1',
  ];

  document
    .querySelector('div[class*="DivCommentItemContainer"]')
    ?.scrollIntoView();

  let scrollInt = setInterval(() => {
    window.scrollBy(0, 2);
    window.scrollBy(0, -2);

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

          console.log(e.textContent);
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
  }, 500);
} catch (error) {
  document.querySelector('body').style.backgroundColor = 'red';
}
