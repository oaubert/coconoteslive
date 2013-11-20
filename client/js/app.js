'use strict';

angular.module('mla', [
    'ngRoute',
    'mla.controllers',
    'mla.restServices'
]).
config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/annotations', {templateUrl: '/static/partials/annotation-list.html', controller: 'AnnotationListCtrl'});
    $routeProvider.when('/annotations/:annotationId', {templateUrl: '/static/partials/annotation-detail.html', controller: 'AnnotationDetailCtrl'});
    $routeProvider.otherwise({redirectTo: '/annotations'});
}]);
