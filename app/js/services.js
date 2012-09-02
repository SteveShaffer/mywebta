'use strict';

/* Services */


angular.module('myApp.services', ['ngResource'])
  .factory('Lesson', function($resource) {
    return $resource('/lessons/:lessonId', {lessonId: '@key'})
  })
  .factory('LessonFolder', function($resource) {
    return $resource('/lessonfolders/:key', {key: '@key'})
  })
  .factory('Student', function($resource) {
    return $resource('/periods/:periodId/students/:studentId', {periodId: '@period', studentId: '@key'})
  })
  .factory('RandomStudent', function($resource) {
    return $resource('/periods/:periodId/students/random', {periodId: '@period'})
  })
  .factory('Period', function($resource) {
    return $resource('/periods/:periodId', {periodId: '@key'})
  })
;