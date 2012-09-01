'use strict';

/* Services */


angular.module('myApp.services', ['ngResource'])
.factory('Lesson', function($resource) {
  return $resource('/lessons/:lessonId', {lessonId: '@key'})
})
});