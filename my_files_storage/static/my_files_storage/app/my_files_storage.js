(function () {
    'use strict';

    function UserFilesRestangular(Restangular) {
        return Restangular.withConfig(function (RestangularConfigurer) {
            RestangularConfigurer.setBaseUrl('/my_files_storage/api/');
        });
    };

    angular
        .module('my_files_storage', ['treesApp'])
        .factory('UserFilesRestangular', UserFilesRestangular)
        .directive("fileread", [function () {
            return {
                scope: {
                    fileread: "="
                },
                link: function (scope, element, attributes) {
                    element.bind("change", function (changeEvent) {
                        scope.$apply(function () {
                            scope.fileread = changeEvent.target.files[0];
                            // or all selected files:
                            // scope.fileread = changeEvent.target.files;
                        });
                    });
                }
            }
        }])
        .controller('filesCtrl', function ($scope, $log, UserFilesRestangular) {
            $scope.user = {};
            $scope.user_files = [];
            $scope.new_file = {};
            $scope.errors = [];
            $scope.load_user_files = LoadUserData;
            $scope.load_new_file = LoadNewFile;
            $scope.remove_file = RemoveFile;
            //$scope.uploader = new FileUploader();


            $scope.$watch('user', function () {
                console.log($scope.user) //с init не робит =(((
            });

            $scope.$watch('user_files', function () {
                console.log($scope.user_files) //с init не робит =(((
            });

            function LoadNewFile(file, user) {
                console.log(user)
//                $log.debug(file);
                $log.debug($scope.user);
//                $log.debug($scope.user_files);
                return UserFilesRestangular.all('files').post(file).then(
                    function (response) {
                        //todo: через дефер сделать все последовательно
                        if (response.hasOwnProperty('error')) {
                            var error = String(response.error)
                            if ($scope.errors.indexOf(error) == -1) {
                                console.log(error);
                                console.log(error.indexOf('already'))
                                if ((error.indexOf('already') != -1)) {    //костыль с хардкодингом убрать потом
                                    var pk = (error)[error.length - 1]
                                    console.log(pk);
                                    UserFilesRestangular.one('files', pk).getList('users').then(
                                        function (users) {
                                            console.log(users)
                                            users.forEach(
                                                function (user) {
                                                    var user_error = "Another user load you file, it's  !!!!!!!" + user.username
                                                    if ($scope.errors.indexOf(user_error) == -1) {
                                                        $scope.errors.push(user_error)
                                                    }
                                                }
                                            )
                                        },
                                        function (errors) {
                                            console.log(errors)
                                            $scope.errors.push(errors);
                                        }
                                    )
                                }
                                else {
                                    $scope.errors.push(error);
                                }
                            }
                        }
                        //else if(response.hasOwnProperty('detail')) {$scope.errors = response.detail};
                        if (response.hasOwnProperty('id')) {
                            var file_id = response.id;
                            var user_file = {'user': $scope.user.id, 'title': file.name, 'file': file_id};
                            //var user_file = {'user':$scope.user.id, 'title':file.name, 'file': file_id};
//                            var user_file = {'user':'1', 'title':file.name, 'file': file_id};
                            console.log($scope.user)
                            console.log(user_file)
                            UserFilesRestangular.all('users_files').post(user_file).then(
                                function(){
                                    $scope.load_user_files($scope.user.id) //разобраться почему не изменяется dom с первого раза, с ng-click scope,apply не нужен
                                    $scope.load_user_files($scope.user.id)
                                }
                            );
                        }
                        ;
                    },
                    function (error) {
                        try {
                            if (!(error.data.detail in  $scope.errors)) {
                                $scope.errors.push(error.data.detail)
                            }
                            ;
                        }
                        catch (err) {
                            console.log(err);
                        }

                    }

                );
//                UserFilesRestangular.all('files').post(file);
//                UserFilesRestangular.all('users_files').post(file);
                //$scope.user_files.post();
            };

            function RemoveFile(file) {
                $log.debug(file);
//                var user_id = file.user
//                $scope.user_files = [];
                file.remove().then(
                    function(){
                        $scope.load_user_files($scope.user.id) //разобраться почему не изменяется dom с первого раза, с ng-click scope,apply не нужен
                        $scope.load_user_files($scope.user.id)
                    }
                )

                //$scope.$apply()
//                return UserFilesRestangular.one('users_files',  file.id).get().then(function (results) {
//                    $log.debug(results);
//
//                    return $scope.user_files;
//                });
            };

            function LoadUserData(user_id) {
                UserFilesRestangular.one('users', user_id).getList('user_files').then(function (results) {
                    $log.debug(results);
                    $scope.user_files = results;
                    $scope.user5 = user_id;
                    $scope.user.id = user_id;

//                    return $scope.user_files;
                });
            };

        })


}).call(this);