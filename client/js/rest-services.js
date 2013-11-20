'use strict';

angular.module('mla.restServices', ['djangoRESTResources'])
    .factory('Annotation', ['djResource', '$filter',
                            function (resource, $filter) {
                                var res = resource('/mla/annotation/:annotationId', {});
                                
                                res.append = function (data, begin, end, category, creator) {
                                    if (end === undefined)
                                        // FIXME: fetch time from server
                                        end = (new Date()).getTime();
                                    if (creator === undefined)
                                        creator = 'Anonymous';
                                    var ann = new res({
                                        data: data,
                                        // Encode timestamps in the appropriate input format for the REST framework
                                        // YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HHMM|-HHMM|Z]"
                                        begin: $filter('date')(begin, "yyyy-MM-ddTHH:mm:ss.sssZ"),
                                        end: $filter('date')(end, "yyyy-MM-ddTHH:mm:ss.sssZ"),
                                        category: category,
                                        creator: creator
                                    });
                                    ann.$save();
                                };
                                return res;
                            }]);
