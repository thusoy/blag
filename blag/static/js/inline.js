/*!
Modified for brevity from https://github.com/filamentgroup/loadCSS
loadCSS: load a CSS file asynchronously.
[c]2014 @scottjehl, Filament Group, Inc.
Licensed MIT
*/
function loadCSS(href){
  'use strict';
  var ss = window.document.createElement('link'),
      ref = window.document.getElementsByTagName('head')[0];

  ss.rel = 'stylesheet';
  ss.href = href;

  // temporarily, set media to something non-matching to ensure it'll
  // fetch without blocking render
  ss.media = 'only x';

  ref.parentNode.insertBefore(ss, ref);

  setTimeout(function() {
    // set media back to `all` so that the stylesheet applies once it loads
    ss.media = 'all';
  }, 0);
}
