'use strict';

/* Filters */

angular.module('myApp.filters', [])
  .filter('numberToLetter', function() {
    return function(input) {
      return String.fromCharCode(64 + input);
    }
  })
;
