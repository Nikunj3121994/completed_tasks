(function () {
    'use strict';

angular
    .module('simpleUpload', [])
    .directive('fileModel', ['$parse', function ($parse) {
        return {
            restrict: 'A',
            link: function(scope, element, attrs) {
                var model = $parse(attrs.fileModel);
                var modelSetter = model.assign;

                element.bind('change', function(){
                    scope.$apply(function(){
                        modelSetter(scope, element[0].files[0]);
                    });
                });
            }
        };
    }])
//    .directive("fileread", [function () {
//        return {
//            scope: {
//                fileread: "="
//            },
//            link: function (scope, element, attributes) {
//                element.bind("change", function (changeEvent) {
//                    scope.$apply(function () {
//                        scope.fileread = changeEvent.target.files[0];
//                        // or all selected files:
//                        // scope.fileread = changeEvent.target.files;
//                    });
//                });
//            }
//        }
//    }])
    .service('fileUpload', ['$http', function ($http) {
        this.uploadFileToUrl = function(file, uploadUrl){
            var fd = new FormData();
            fd.append('file', file);
            return $http.post(uploadUrl, fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            })
//            .success(function(){
//                return
//            })
//            .error(function(){
//            });
        }
    }]);

}).call(this);
