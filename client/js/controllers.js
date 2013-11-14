'use strict';

angular.module('mla.controllers', [])
    .controller('AnnotationListCtrl', ['$scope', 'Annotation', function ($scope, Annotation) {
        $scope.annotations = Annotation.query();
        
        $scope.submit = function(category) {
            var data = this.annotation;
            var begin = parseInt(this.begin_timestamp, 10) || (new Date()).getTime();
            var end = (new Date()).getTime();
            var creator = "Anonymous";
            
            Annotation.append(data, begin, end, category, creator);
            this.annotation = "";
            this.begin_timestamp = null;
        };

        $scope.reset_begin_timestamp = function() {
            if (! this.annotation) {
                this.begin_timestamp = (new Date()).getTime();
            }
        };
    }])
    .controller('AnnotationDetailCtrl', ['$scope', '$routeParams', 'Annotation', function ($scope, $routeParams, Annotation) {
        $scope.annotation = Annotation.get($routeParams.annotationId);

        $scope.back = function() {
            window.history.back();
        }
    }]);
