var bookStoreCtrls = angular.module('bookStoreCtrls', []);

bookStoreCtrls.controller('HelloCtrl', ['$scope',
    function($scope){
        $scope.greeting = {
            text: 'Hello'
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

bookStoreCtrls.controller('FormCtrl', ['$scope',
    function($scope) {
        $scope.userInfo = {
            email: 'chenhuan0102@126.com',
            password: '123456',
            autoLogin: true
        };

        $scope.getFormData = function() {
            console.log($scope.userInfo);
        };

        $scope.setFormData = function() {
            $scope.userInfo = {
                email: 'jianghong@126.com',
                password: '654321',
                autoLogin: false
            };
        };

        $scope.resetFormData = function() {
            $scope.userInfo = {
                email: 'chenhuan0102@126.com',
                password: '123456',
                autoLogin: true
            };
        };
    }
]);

bookStoreCtrls.controller('CSSCtrl', ['$scope',
    function($scope) {
        $scope.setGreen = function() {
            $scope.color = 'green';
        };

        $scope.setRed = function() {
            $scope.color = 'red';
        };
    }
]);

bookStoreCtrls.controller('NGClass', ['$scope',
    function($scope) {
        $scope.showError = function() {
            $scope.isError = true;
            $scope.isWarning = false;
            $scope.messageText = 'showError';
        };

        $scope.showWarning = function() {
            $scope.isError = false;
            $scope.isWarning = true;
            $scope.messageText = 'showWarning';
        };
    }
]);

bookStoreCtrls.controller('NGShow', ['$scope',
    function($scope) {
        $scope.menuState = {show : false};
        $scope.toggleMenu = function() {
            $scope.menuState.show = !$scope.menuState.show;
        };
    }
]);
