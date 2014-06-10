'use strict';

angular.module('mla.restServices', ['djangoRESTResources'])
    .factory('Annotation', ['djResource', '$filter',
                            function (resource, $filter) {
                                var res = resource('annotation/:annotationId', {});
                                
                                res.append = function (annotation, success, error) {
                                    if (annotation.end === undefined)
                                        // FIXME: fetch time from server
                                        end = (new Date()).getTime();
                                    if (annotation.creator === undefined)
                                        creator = 'Anonymous';
                                    // Encode timestamps in the appropriate input format for the REST framework
                                    // YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HHMM|-HHMM|Z]"
                                    annotation.begin = $filter('date')(annotation.begin, "yyyy-MM-ddTHH:mm:ss.sssZ");
                                    annotation.end = $filter('date')(annotation.end, "yyyy-MM-ddTHH:mm:ss.sssZ");
                                    var ann = new res(annotation);
                                    ann.$save({}, success, error);
                                    return annotation;

                                };
                                return res;
                            }]);
