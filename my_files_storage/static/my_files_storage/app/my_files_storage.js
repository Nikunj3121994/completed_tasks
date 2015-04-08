(function () {
    'use strict';

    function UserFilesRestangular(Restangular) {
        return Restangular.withConfig(function (RestangularConfigurer) {
            RestangularConfigurer.setBaseUrl('/my_files_storage/api/');
        });
    };

    angular
        .module('my_files_storage', ['treesApp', 'ui.tree', 'ui.bootstrap', 'restangular'])
        .factory('UserFilesRestangular', UserFilesRestangular)
        .controller('filesCtrl', function ($scope, $log, $http, UserFilesRestangular) {
//            $scope.user
//            $scope.user_files
            console.log($scope.user)
        })


}).call(this);