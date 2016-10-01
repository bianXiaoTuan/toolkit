var model = angular.module("HelloAngular", []);

model.controller("HelloAngular", ['$scope', function($scope) {
        $scope.greeting = {
            'text' : 'Hello'
        };
    }
]);
