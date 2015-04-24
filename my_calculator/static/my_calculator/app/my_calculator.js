(function () {
    'use strict';

    function CalcRestangular(Restangular) {
        //console.log(Restangular);
        return Restangular
            .withConfig(function (RestangularConfigurer) {
                RestangularConfigurer
                    .setBaseUrl('/my_calculator/api');
            });
    };

    function NumRestangular(Restangular) {
        //console.log(Restangular);
        return Restangular
            .withConfig(function (RestangularConfigurer) {
                RestangularConfigurer
                    .setBaseUrl('/my_calculator/api/numbers');
            });
    };

    function LexRestangular(Restangular) {
        //console.log(Restangular);
        return Restangular
            .withConfig(function (RestangularConfigurer) {
                RestangularConfigurer
                    .setBaseUrl('/my_calculator/api/lexemes');
            });
    };





    angular
        .module('my_calculator', ['restangular', 'ngSanitize'])
        .factory('CalcRestangular', CalcRestangular)
        .factory('NumRestangular', NumRestangular)
        .factory('LexRestangular', LexRestangular)
        .controller('calcCtrl', function ($scope, $log, $sanitize, NumRestangular, LexRestangular, CalcRestangular) {
            $scope.numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
            $scope.lexems = ['.', '/', '*', '+', '-'];
            $scope.calculation = '';
            $scope.savedcalculation = '';
            $scope.result = '';
            $scope.build_calculation = build_calculation;
            $scope.calculate = calculate;
            $scope.reset_calculation = reset_calculation;
            $scope.save_calculation = save_calculation;
            $scope.load_calculation = load_calculation;

            function reset_calculation() {
                $scope.calculation = '';
                //angular.extend($scope.calculation, '');
            };

            function build_calculation(event) {
                $log.debug(event);
                $scope.calculation += $sanitize(event.target.innerText);
            };

            function calculate() {
                $log.debug($scope.calculation);
                $log.debug($sanitize($scope.calculation));
                return CalcRestangular.one('results', $scope.calculation).get().then(function (data) {
                        $log.debug(data);
                        $scope.result = data;
                        reset_calculation();
                        return data;
                 });
            };

            function save_calculation(){
                $scope.savedcalculation = $scope.calculation;
            };

            function load_calculation(){
                $scope.calculation = $scope.savedcalculation;
                 $scope.savedcalculation = '';
            };

            function LoadData(user_id) {
                console.log(CalcRestangular.all('numbers').getList());
                CalcRestangular.all('numbers').getList().then(function (data) {
                    //angular.extend($scope.numbers, []);
                    //$scope.numbers.lenght = 0;
                    $scope.numbers = [];
                    data.forEach(function (item) {
                        $scope.numbers =  $scope.numbers.concat(item.number);
                        //console.log(item);
                    });
                });
                CalcRestangular.all('lexemes').getList().then(function (data) {
                    $scope.lexems = [];
                    data.forEach(function (item) {
                         $scope.lexems =  $scope.lexems.concat(item.operation);
                    });
                });
            };
            LoadData();
        })

    }

    ).
    call(this);
