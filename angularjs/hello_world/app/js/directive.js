var model = angular.module("HelloAngular", []);

model.directive("hello", function(){
    return {
        restrict : 'E',
        template : '<div>Hi everyone!</div>',
        replace : true
    };
});