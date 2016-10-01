var bookStoreCtrls = angular.module('bookStoreCtrls', []);

bookStoreCtrls.controller('HelloCtrl', ['$scope',
    function($scope){
        $scope.greeting = {
            text: 'Hello Angular'
        };
    }
]);

bookStoreCtrls.controller('BookListCtrl', ['$scope',
    function($scope) {
        $scope.books = [
            {title: '<<算法导论>>', auther: '陈欢'},
            {title: '<<机器学习>>', auther: '姜虹'},
            {title: '<<统计学基础>>', auther: '胖乖'}
        ];
    }
]);
