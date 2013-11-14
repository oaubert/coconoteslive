'use strict';

angular.module('mla.restServices', ['djangoRESTResources'])
    .factory('Annotation', ['$resource',
        function ($resource) {
            return $resource('http:/annotation/:annotationId', {});
        }]);
