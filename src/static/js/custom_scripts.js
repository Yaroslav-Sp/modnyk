
  function toggleLike(button) {
    const icon = button.querySelector('i');
    if (icon.style.color === 'red') {
      icon.style.color = 'grey';
    } else {
      icon.style.color = 'red';
    }
  }
