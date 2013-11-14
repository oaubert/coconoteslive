'use strict';

angular.module('mla', [
    'ngRoute',
    'mla.controllers',
    'mla.memoryServices'
]).
config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/annotations', {templateUrl: 'partials/annotation-list.html', controller: 'AnnotationListCtrl'});
    $routeProvider.when('/annotations/:annotationId', {templateUrl: 'partials/annotation-detail.html', controller: 'AnnotationDetailCtrl'});
    $routeProvider.otherwise({redirectTo: '/annotations'});
}]);
