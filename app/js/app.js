'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', ['myApp.filters', 'myApp.services', 'myApp.directives']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/week/:year/:month/:day', {
      templateUrl: 'partials/week.html',
      controller: WeekCtrl
    });
    $routeProvider
      .when('/lessons/:lessonId', {
        templateUrl: 'partials/lesson-detail.html',
        controller: LessonDetailCtrl
      })
      .when('/lessons', {
        templateUrl: 'partials/lesson-list.html',
        controller: LessonListCtrl
      })
      .when('/periods/:periodId/students/random' ,{
        templateUrl: 'partials/student-random.html',
        controller: StudentRandomCtrl
      })
      .when('/periods', {
        templateUrl: 'partials/period-list.html',
        controller: PeriodListCtrl
      })
      .otherwise({redirectTo: '/periods'});
  }]);