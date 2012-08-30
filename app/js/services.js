'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('myApp.services', ['ngResource']).
factory('Lesson', function($resource) {
  return $resource('lessons/:lessonId.json', {}, {
    query: {method:'GET', params:{lessonId:'lessons'}, isArray:true}
  })
});