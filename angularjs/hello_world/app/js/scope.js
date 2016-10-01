var model = angular.module("HelloAngular", []);

model.controller("GreetCtrl", ['$scope','$rootScope',
    function($scope, $rootScope) {
        $scope.name = 'World';
        $rootScope.department = 'Angular';
    }
]);

model.controller("ListCtrl", ['$scope',
    function($scope) {
        $scope.names = ['Igor', 'Misko', 'Vojta'];
    }
]);
