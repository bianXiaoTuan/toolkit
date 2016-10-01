var module = angular.module("HelloAngular", []);

module.controller('CommonController', ['$scope', function($scope){
    $scope.common = function() {
        alert('通用功能');
    }
}]);

module.controller('Controller1', ['$scope', function($scope){
    $scope.greeting = {
        'text1' : 'Hello'
    };

    $scope.test1 = function() {
        alert('test1');
    };
}]);

module.controller('Controller2', ['$scope', function($scope){
    $scope.greeting = {
        'text2' : 'Hello'
    };

    $scope.test2 = function() {
        alert('test2');
    }
}]);
