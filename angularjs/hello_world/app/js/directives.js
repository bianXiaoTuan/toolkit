var bookStoreDirectives = angular.module('bookStoreDirectives', []);

bookStoreDirectives.directive('hello',
    function() {
		return {
			restrict: 'E',
			template: '<p>Hello World</p>',
			replace: true
		};
    }
);

bookStoreDirectives.directive('bookStoreDirective_1', ['$scope',
    function($scope) {

    }
]);

bookStoreDirectives.directive('bookStoreDirective_2', ['$scope',
    function($scope) {

    }
]);


