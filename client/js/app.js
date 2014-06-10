'use strict';

angular.module('mla', [
    'ngRoute',
    'mla.controllers',
    'mla.restServices'
]).
config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/shortcut/:shortcutId', { templateUrl: '../static/partials/annotation-list.html', controller: 'AnnotationListCtrl'});
    $routeProvider.when('/annotations/:annotationId', { templateUrl: '../static/partials/annotation-detail.html', controller: 'AnnotationDetailCtrl'});
    $routeProvider.otherwise({ templateUrl: '../static/partials/annotation-list.html', controller: 'AnnotationListCtrl'});
}])
.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';    
}]);
