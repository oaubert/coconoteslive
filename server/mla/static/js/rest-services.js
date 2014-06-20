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
        return {
            data: { 'basic': [ { id: 'comment', label: 'Envoyer', tooltip: 'Envoyer le commentaire' },
                               { id: 'question', label: 'Question', tooltip: 'Poser une question' },
                               { id: 'chapitre', label: 'Chapitre', tooltip: 'Changement de chapitre' },
                               { id: 'slide', label: 'Slide', tooltip: 'Changement de slide' } ],
                    'concept': [ { id: 'concept', label: 'Concept', tooltip: 'Introduction de concept' },
                                 { id: 'exemple', label: 'Exemple', tooltip: 'Présentation d\'un exemple' },
                                 { id: 'exercice', label: 'Exercice', tooltip: 'Exercice pratique' } ],
                    'amelioration': [ { id: 'pepite', label: 'Pépite', color: '#2b0' },
                                      { id: 'confusion', label: 'Confusion', color: '#b20' },
                                      { id: 'refaire', label: 'Slide à refaire', color: '#b20' },
                                      { id: 'typo', label: 'Typo' } ],
                    'scenario': [ { id: 'faire_exercice', label: 'Faire un exercice' },
                                  { id: 'ajouter_animation', label: 'Ajouter une animation' },
                                  { id: 'proposer_activite', label: 'Proposer une activité' } ]
                  },
            'keys': function () { return Object.keys(this.data); }
        };
    });
