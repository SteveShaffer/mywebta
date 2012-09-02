'use strict';

/* Controllers */


function LessonDetailCtrl($scope, $routeParams, Lesson) {
  $scope.lesson = Lesson.get({ lessonId: $routeParams.lessonId }, function(lesson) {
    $scope.mainDocUrl = lesson.attachments[0].url;
  });
  
  $scope.setDoc = function(docUrl) {
    $scope.mainDocUrl = docUrl;
  };
}

function LessonListCtrl($scope, Lesson, LessonFolder) {
  $scope.lessons = Lesson.query();
  $scope.folders = LessonFolder.query();
}

function StudentRandomCtrl($scope, $routeParams, RandomStudent) {
  $scope.periodId = $routeParams.periodId
  $scope.student = RandomStudent.get({ periodId: $scope.periodId });
}

function PeriodListCtrl($scope, Period) {
  $scope.periods = Period.query();
}

function WeekCtrl($scope, $route, $routeParams) {
  $scope.params = $routeParams;
  $scope.date = $routeParams.month + '/' + $routeParams.day + '/' + $routeParams.year;
  $scope.plans = [
    {
      name: 'Freshmen',
      lessons: [
        'Lesson for day 1',
        'Lesson for day 2',
        'eh... let\'s just relax this day...',
        'oh who cares?'
      ]
    },
    {
      name: 'Juniors',
      lessons: [
        'Lecture them!',
        'Grade them!',
        'Give them a break?  No!',
        'TEST DAY!!!'
      ]
    }
  ];
  $scope.days = [
    {
      title: 'Monday',
      periods: [0,1,2,3,4,5]
    },
    {
      title: 'Tuesday',
      periods: [0,6,1,2,3,4]
    },
    {
      title: 'Wednesday',
      periods: [5,6,1,2]
    },
    {
      title: 'Thursday',
      periods: [0,3,4,5,6,1]
    },
    {
      title: 'Friday',
      periods: [0,2,3,4,5,6]
    }
  ];
  $scope.periods = [
    {
      name: 0,
      plan: 0
    },
    {
      name: 1,
      plan: 0
    },
    {
      name: 2,
      plan: 0
    },
    {
      name: 5,
      plan: 0
    },
    {
      name: 6,
      plan: 1
    }
  ];
  $scope.getLesson = function(day, period) {
    //TODO: Somehow get the schedule to look back at the data (and be bound to it hopefully).
    //Not confident that that would be happening with a function like this.
    //How do we make it figure out which ordinal lesson should be associated with this day and period?
    //Maybe somehow we can go through in order and mark off which ones have already been used?
    //How do we bind to these cross-product data points?  Do we need to give them each their own id of sorts?
  }
}