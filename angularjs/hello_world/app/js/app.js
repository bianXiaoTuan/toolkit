var bookStoreApp = angular.module('bookStoreApp', [
    'ngRoute',
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
            templateUrl: 'tpls/book_list.html',
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
    ).when('/ngclass', {
            templateUrl: 'tpls/ng_class.html',
            controller: 'NGClass'
        }
    ).when('/ngshow', {
            templateUrl: 'tpls/ng_show.html',
            controller: 'NGClass'
        }
    ).when('/directive_hello', {
            templateUrl: 'tpls/directive_hello.html',
        }
    ).otherwise( {
            redirectTo: '/hello'
        }
    );
});