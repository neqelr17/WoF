(function () {
  'use strict';

  angular
    .module('wof', [
      'wof.routes',
      'wof.authentication',
      'wof.config'
    ]);

  angular
    .module('wof.config', []);

  angular
    .module('wof.routes', ['ngRoute']);

  run.$inject = ['$http'];

  /**
  * @name run
  * @ desc Update xsrf $http headers to align with Django's defaults
  */
  function run($http) {
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';
  }

})();
