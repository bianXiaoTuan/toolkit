var bookStoreDirectives = angular.module('bookStoreDirectives', []);

bookStoreDirectives.directive('bookStoreDirective_1', ['$scope',
    function($scope) {

    }
]);

bookStoreDirectives.directive('bookStoreDirective_2', ['$scope',
    function($scope) {

    }
]);

bookStoreDirectives.directive('hello', ['$scope',
    function($scope) {
		return {
			restrict: 'E',
			template: '<div>HelloWorld</div>',
			replace: true
		};
    }
]);
