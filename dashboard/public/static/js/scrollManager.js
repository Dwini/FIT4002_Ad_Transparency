var scroll_id = 'button-scroll-to-top';
document.onscroll = function() {
  // hide scroll to top button if the user is 300px from the top.
  if (window.scrollY < 300) {
    document.getElementById(scroll_id).style.display = 'none';
  } else {
    document.getElementById(scroll_id).style.display = 'unset';
  }
}
