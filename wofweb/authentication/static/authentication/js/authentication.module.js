(function () {
  'use strict';

  angular
    .module('wof.authentication', [
      'wof.authentication.controllers',
      'wof.authentication.services'
    ]);

  angular
    .module('wof.authentication.controllers', []);

  angular
    .module('wof.authentication.services', ['ngCookies']);
})();
