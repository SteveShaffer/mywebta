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

function StudentRandomCtrl($scope, $routeParams, Period, RandomStudent) {
  $scope.periodId = $routeParams.periodId;
  $scope.period = Period.get({ periodId: $scope.periodId });
  $scope.student = RandomStudent.get({ periodId: $scope.periodId });
}

function StudentBatchCtrl($scope, $routeParams, Period) {
  $scope.period = Period.get({ periodId: $routeParams.periodId });
}

function PeriodListCtrl($scope, Period) {
  $scope.periods = Period.query();
  $scope.reloadPeriods = function() {
    $scope.periods = Period.query(); //TODO: this is terrible!
  }
}

function PeriodDetailCtrl($scope, $routeParams, Period, Student) {
  $scope.periodId = $routeParams.periodId;
  $scope.period = Period.get({ periodId: $scope.periodId });
  $scope.students = Student.query({ periodId: $scope.periodId });
  $scope.reloadStudents = function() {
    $scope.students = Student.query({ periodId: $scope.periodId}); //TODO: this is terrible!
  }
}

function PeriodNewCtrl($scope, Period) {
  $scope.period = new Period();
  $scope.period.addNew = function() {
    this.$save();
    $('#add-alert').text(this.name + ' added.').removeClass('hide');
  }
}

function HotpotatoCtrl($scope, $log) {
  $scope.averageTime = 40;
  $scope.imageId = 0;
  var maxImage = 4; //ID of max image.  So if you have 5 images numbered 0-4, this would be 4.
  
  function incrementImage() {
    $scope.imageId += 1;
    $('#potato-pic').attr('src','img/potato/' + $scope.imageId + '.jpg'); //TODO: Why am I even using angular if this can't be dynamic?
    $log.log('Incrementing image to ' + $scope.imageId + '.  Setting timer for ' + $scope.changeTimes[$scope.imageId]);
    if ($scope.imageId == maxImage) {
      document.getElementById('explosion-sound').play();
      $('#song-video').attr('src','');
      
    } else {
      setTimeout(function(){incrementImage()},$scope.changeTimes[$scope.imageId]); //TODO: should be using $scope.changeTimes.pop() probably.
    }
  }
  
  $scope.timerGo = function() {
    $scope.imageId = 0;
    $scope.changeTimes = [];
    $('#song-video').attr('src','http://www.youtube.com/embed/FV6nJxg7mM0?autoplay=1');
    for (var i=0; i<maxImage; i++) {
      $scope.changeTimes.push( (0.5+(1*Math.random())) * $scope.averageTime*1000 / maxImage )
    }
    $scope.timerRef = setTimeout(function(){incrementImage()}, $scope.changeTimes[0]);
    $log.log('Kicked off timer.');
  };
  
  $scope.toggleOptions = function() { //TODO: There's some angular thing with ng-show I should be doing instead
    $('#optShowButton').toggle();
    $('#options').toggle();
  }
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