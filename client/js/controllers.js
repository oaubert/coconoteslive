'use strict';

angular.module('mla.controllers', [])
    .controller('AnnotationListCtrl', ['$scope', 'Annotation', '$interval', function ($scope, Annotation, $interval) {
        // Default value
        $scope.username = "Anonyme";

        $scope.refresh = function() {
            Annotation.query().$then( function (response) {
                var data = response.data;

                if ($scope.annotations && $scope.annotations.length && $scope.annotations[$scope.annotations.length - 1].id === undefined) {
                    // We just added locally an annotation, so it has no id. See if we can pick it from returned data.
                    var local = $scope.annotations[$scope.annotations.length - 1];
                    var remote = data[data.length - 1];
                    // FIXME: Wrong comparison here, it depends too
                    // much on datetime str representations. We should
                    // parse the dates.
                    if (local.begin === remote.begin && local.end === remote.end && local.data == remote.data) {
                        // Same annotation. Let's replace the local version with the server-side version
                        $scope.annotations.pop();
                        $scope.annotations.push(remote);
                    }
                }

                // Let's compare loaded data and local data. If they match, no update is necessary
                if ($scope.annotations && data.length == $scope.annotations.length) {
                    var similar = true;
                    for (var i = data.length - 1 ; i >= 0 ; i--) {
                        if (data[i].id !== $scope.annotations[i].id) {
                            similar = false;
                            break;
                        }
                    }
                    if (! similar) {
                        $scope.annotations = data;
                    }
                } else {
                    // Different size. Update the whole list
                    $scope.annotations = data;
                }
            });
        };

        $scope.submit = function(category) {
            var data = this.annotation;
            var begin = parseInt(this.begin_timestamp, 10) || (new Date()).getTime();
            var end = (new Date()).getTime();
            var creator = $scope.username;
            this.annotation = "";
            this.begin_timestamp = null;

            var ann = Annotation.append({ data: data,
                                          begin: begin,
                                          end: end,
                                          category: category || "",
                                          creator: creator
                                        }
                                        ,
                                        function (response) { $scope.refresh() });
            // Immediately update displayed list (optimistic view, there should be no error)
            $scope.annotations.push(ann);
        };

        $scope.reset_begin_timestamp = function() {
            if (! this.annotation) {
                this.begin_timestamp = (new Date()).getTime();
            }
        };

        $scope.refresh();

        $interval($scope.refresh, 30000);

    }])
    .controller('AnnotationDetailCtrl', ['$scope', '$routeParams', 'Annotation', function ($scope, $routeParams, Annotation) {
        $scope.annotation = Annotation.get($routeParams.annotationId);

        $scope.back = function() {
            window.history.back();
        }
    }]);
