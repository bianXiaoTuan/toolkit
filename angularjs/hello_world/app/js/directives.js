var bookStoreDirectives = angular.module('bookStoreDirectives', []);

/**
 * restrict
 * E: 元素
 * A: 属性
 * C: 样式类
 * M: 注释
 */
bookStoreDirectives.directive('hello',
    function() {
		return {
			restrict: 'AEMC',
			template: '<p>Hello World</p>',
			replace: true
		};
    }
);
