(function () {
  'use strict';

  angular
    .module('wof', [
      'wof.routes',
      'wof.authentication'
    ]);

  angular
    .module('wof.routes', ['ngRoute']);
})();
