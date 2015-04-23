(function () {
    'use strict';

    function CalcRestangular(Restangular) {
        console.log(Restangular);
        return Restangular
            .withConfig(function (RestangularConfigurer) {
                RestangularConfigurer
                    .setBaseUrl('/my_calculator/api')
//                    .setDefaultHttpFields({transformRequest: angular.identity});
            });
    };



    angular
        .module('my_calculator', ['restangular', 'ngSanitize'])
        .factory('CalcRestangular', CalcRestangular)
        .controller('calcCtrl', function ($scope, $log, $sanitize, CalcRestangular) {
        $scope.calculation = '';
        $scope.result = '';
        $scope.build_calculation = build_calculation;
        $scope.calculate = calculate;
        $scope.reset_calculation = reset_calculation;

        function calculate() {
            $log.debug($scope.calculation);
            $log.debug($sanitize($scope.calculation));
            return CalcRestangular.one('', $scope.calculation).get().then(function (data) {
                    $log.debug(data);
                    $scope.result = data;
                    return data;
             })
        };

        function reset_calculation() {
            $scope.calculation = '';
            //angular.extend($scope.calculation, '');
        };

        function build_calculation(event) {
            $log.debug(event);
            $scope.calculation += $sanitize(event.target.innerText);
        };

//                $scope.numbers = (0,1,2,3,4,5,6,7,8,9)
//                $scope.user = {};
//                $scope.user_files = [];
//                $scope.new_file = {};
//                $scope.errors = [];
//                $scope.load_user_files = LoadUserData;
//                $scope.load_new_file = LoadNewFile;
//                $scope.remove_file = RemoveFile;
//
//
//                function LoadNewFile(file, user) {
//                    $scope.errors = [];
//                    var uploadUrl = 'files';
//                    RestAngularFileUploader.uploadFile(file, uploadUrl)
//                        .then(
//                            function (response) {
//                                console.log(response)
//                                //todo: через дефер сделать все последовательно
//                                //проверка на ошибки
//                                if (response.hasOwnProperty('error')) {
//                                    var file_error = String(response.error);
//                                    if ($scope.errors.indexOf(file_error) == -1) {
//                                        //проверка на наличие файла у других пользователей
//                                        if ((file_error.indexOf('already') != -1)) {    //костыль с хардкодингом убрать потом
//                                            var pk = file_error.split(' ').splice(-1)
//                                            UserFilesRestangular.one('files', pk).getList('users').then(
//                                                function (users) {
//                                                    console.log(users)
//                                                    users.forEach(
//                                                        function (user) {
//                                                            var user_error = "Another user load you file, it's  " + user.username
//                                                            console.log($scope.errors.indexOf(user_error))
//                                                            if ($scope.errors.indexOf(user_error) == -1) {
//                                                                $scope.errors.push(user_error)
//                                                            }
//                                                        }
//                                                    )
//                                                },
//                                                function (errors) {
//                                                    console.log(errors)
//                                                    $scope.errors.push(errors);
//                                                }
//                                            )
//                                        }
//                                        else {
//                                            $scope.errors.push(error);
//                                        }
//                                    }
//                                }
//                                //создание записи связующей пользователя и файл
//                                if (response.hasOwnProperty('id')) {
//                                    var file_id = response.id;
//                                    var user_file = {'user': $scope.user.id, 'title': file.name, 'file': file_id};
//                                    UserFilesRestangular.all('users_files').post(user_file)
//                                        .then(
//                                        function (response) {
//                                            if (response.hasOwnProperty('error')) {
//                                                var users_error = String(response.error)
//                                                //                                        console.log(response)
//                                                //                                        console.log(users_error)
//                                                if ($scope.errors.indexOf(users_error) == -1) {
//                                                    $scope.errors.push(users_error);
//                                                }
//                                            }
//                                            $scope.load_user_files($scope.user.id)
//                                        },
//                                        function (error) {
//                                            try {
//                                                if (!(error.data.detail in  $scope.errors)) {
//                                                    $scope.errors.push(error.data.detail)
//                                                }
//                                            }
//                                            catch (err) {
//                                                console.log(err);
//                                            }
//                                        }
//                                    );
//                                }
//                                ;
//                            },
//                            function (errors) {
//                                try {
//                                    for (var error in errors.data) {
//                                        if (!(error in  $scope.errors)) {
//                                            $scope.errors.push(errors.data[error])
//                                        }
//                                    }
//                                }
//                                catch (err) {
//                                    console.log(err);
//                                }
//                            }
//                    );
//                };
//
//                function RemoveFile(file) {
//                    $log.debug(file);
//                    file.remove().then(
//                        function () {
//                            $scope.load_user_files($scope.user.id)
//                        }
//                    )
//                };
//
//                function LoadUserData(user_id) {
//                    UserFilesRestangular.one('users', user_id).getList('user_files').then(function (results) {
//                        $log.debug(results);
//						$scope.user_files.lenght = 0;
//                        $scope.user_files = results;
//                        $scope.user.id = user_id;
//                    });
//                };
            })

    }

    ).
    call(this);
