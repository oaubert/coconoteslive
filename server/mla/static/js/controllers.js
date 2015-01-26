'use strict';

angular.module('mla.controllers', [ 'LocalStorageModule', 'uuid', 'FBAngular' ])
    .controller('AnnotationListCtrl', ['$scope', '$routeParams', '$location', 'Annotation', '$interval', 'localStorageService', 'uuid', 'Fullscreen',
                                       function ($scope, $routeParams, $location, Annotation, $interval, localStorageService, uuid, Fullscreen) {
        var creatoruuid = localStorageService.get('mla-creatoruuid');
        if (creatoruuid === null) {
             creatoruuid = uuid.generate();
             localStorageService.set('mla-creatoruuid', creatoruuid);
        }
        $scope.creatoruuid = creatoruuid;

        // Default value
        var name = localStorageService.get('mla-username');
        if (name === null) {
             name = "Anonyme";
             localStorageService.set('mla-username', name);
        }
        $scope.username = name;
        $scope.$watch('username', function(newValue, oldValue) {
            localStorageService.set('mla-username', newValue);
        });
        $scope.groupname = document.getElementsByTagName('body')[0].dataset.group;
        $scope.shortcut_keys = window.coconotes_shortcutkeys;
        $scope.shortcutid = $routeParams.shortcutId || document.getElementsByTagName('body')[0].dataset.shortcut || "basic";
        $scope.shortcuts = window.coconotes_shortcuts[$scope.shortcutid] || [];

        $scope.annotations = [];
        $scope.buffered_annotations = [];
        $scope.hasFilter = document.location.search.indexOf('filter=') > 0 ? "on" : "off";

        $scope.refresh = function() {
            Annotation.query({},
                             function () { 
                                 $scope.feedback = "";
                                 if ($scope.buffered_annotations.length) {
                                     // There are some unsaved
                                     // annotations. Try to resend them
                                     // now that we know we have some
                                     // connectivity.
                                     var newbuf = [];
                                     $scope.buffered_annotations.map( function (anndata) {
                                         Annotation.append(anndata,
                                                       function (response) { },
                                                           function (reponse) { 
                                                               // Errors again...
                                                               $scope.feedback = "Network trouble";
                                                               newbuf.push(anndata); });
                                     });
                                     $scope.buffered_annotations = newbuf;
                                     // Trigger another refresh
                                     window.setTimeout($scope.refresh, 1000);
                                 }},
                             function () { $scope.feedback = "Network trouble"; }
                            ).$then( function (response) {
                if (response === undefined)
                    return;
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
            var data = $scope.annotation;
            var begin = parseInt(this.begin_timestamp, 10) || (new Date()).getTime();
            var end = (new Date()).getTime();
            var creator = $scope.username;
            $scope.annotation = "";
            $scope.begin_timestamp = null;

            if (! category && data.match(/(\s|^)#\w+/)) {
                var m = data.match(/(\s|^)#(\w+)/);
                category = m[2].trim();
            }
            var anndata = { data: data,
                            begin: begin,
                            end: end,
                            category: category || "",
                            creator: creator,
                            creatoruuid: creatoruuid
                          };
            var ann = Annotation.append(anndata,
                                        function (response) { $scope.feedback = ""; $scope.refresh(); },
                                        function (reponse) { $scope.feedback = "Network trouble";
                                                             $scope.buffered_annotations.push(anndata); });
            // Immediately update displayed list (optimistic view, there should be no error)
            ann.uploading = true;
            $scope.annotations.push(ann);
        };

        $scope.reset_begin_timestamp = function() {
            if (! this.annotation) {
                this.begin_timestamp = (new Date()).getTime();
            }
        };

        $scope.shortcut_nav = function (direction) {
            var index = $scope.shortcut_keys.indexOf($scope.shortcutid);
            if (index == -1 && direction == -1) {
                // Special case: no shortcut yet, we want to go to the last element
                index = -1;
            } else {
                index = index + direction;
            }
            if (index < 0) {
                index = $scope.shortcut_keys.length + index;
            } else if (index > $scope.shortcut_keys.length - 1) {
                index = 0;
            }
            $scope.shortcutid = $scope.shortcut_keys[index];
            $scope.shortcuts = window.coconotes_shortcuts[$scope.shortcutid] || [];
            $scope.refresh();
        };

        $scope.toggle_fullscreen = function () {
            console.log("toggle fullscreen");
            if (Fullscreen.isEnabled())
                Fullscreen.cancel();
            else
                Fullscreen.all();
        };

        $scope.refresh();

        $interval($scope.refresh, 15000);

    }])
    .controller('AnnotationDetailCtrl', ['$scope', '$routeParams', 'Annotation', function ($scope, $routeParams, Annotation) {
        $scope.annotation = Annotation.get($routeParams.annotationId);

        $scope.back = function() {
            window.history.back();
        };
    }]);
