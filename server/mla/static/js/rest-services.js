'use strict';

angular.module('mla.restServices', ['djangoRESTResources', 'uuid'])
    .factory('Annotation', ['djResource', '$filter', 'uuid',
                            function (resource, $filter, uuid) {
                                var res = resource('annotation/:annotationId', {});

                                res.append = function (annotation, success, error) {
                                    if (annotation.end === undefined)
                                        // FIXME: fetch time from server
                                        annotation.end = (new Date()).getTime();
                                    if (annotation.creator === undefined)
                                        annotation.creator = 'Anonymous';
                                    annotation.uuid = uuid.generate();
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
