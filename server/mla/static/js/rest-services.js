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
                            }])
    .factory('ShortcutService', function () {
        return { 'basic': [ { id: 'comment', label: 'Envoyer', tooltip: 'Envoyer le commentaire' },
                            { id: 'question', label: 'Question', tooltip: 'Poser une question' },
                            { id: 'chapitre', label: 'Chapitre', tooltip: 'Changement de chapitre' } ],
                 'test': [ { id: 'test1', label: 'Test 1', color: '#abc' },
                           { id: 'test2', label: 'Test 2', color: '#def' },
                           { id: 'test3', label: 'Test 3', color: '#fac' },
                           { id: 'test4', label: 'Test 4', color: '#bab' },
                           { id: 'test5', label: 'Test 5', color: '#fac' },
                           { id: 'test6', label: 'Test 6', color: '#cba' } ]
               };
    });
