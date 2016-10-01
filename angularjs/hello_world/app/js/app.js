var bookStoreApp = angular.module('bookStoreApp', [
    'ngRoute',
    'ngAnimate',
    'bookStoreCtrls',
    'bookStoreServices',
    'bookStoreDirectives'
]);

// 路由
bookStoreApp.config(function($routeProvider){
    $routeProvider.when('/hello', {
            templateUrl: 'tpls/hello.html',
            controller: 'HelloCtrl'
        }
    ).when('/list', {
            templateUrl: 'tpls/bookList.html',
            controller: 'BookListCtrl'
        }
    ).when('/form', {
            templateUrl: 'tpls/form.html',
            controller: 'FormCtrl'
        }
    ).when('/css', {
            templateUrl: 'tpls/css.html',
            controller: 'CSSCtrl'
        }
    ).otherwise( {
            redirectTo: '/hello'
        }
    );
});