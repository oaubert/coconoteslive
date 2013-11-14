'use strict';

(function () {

    /**
     * Generates a GUID string, according to RFC4122 standards.
     * @returns {String} The generated GUID.
     * @example af8a8416-6e18-a307-bd9c-f2c947bbb3aa
     * @author Slavik Meltser (slavik@meltser.info).
     * @link http://slavik.meltser.info/?p=142
     */
    function guid() {
        function _p8(s) {
            var p = (Math.random().toString(16)+"000000000").substr(2,8);
            return s ? "-" + p.substr(0,4) + "-" + p.substr(4,4) : p ;
        }
        return _p8() + _p8(true) + _p8(true) + _p8();
    };

    var annotations = [
        {"id": 1, "data": "Test",   "begin": 1383918010000, "end": 1383918020000, "creator": "foobar", "category": "question" },
        {"id": 2, "data": "A",      "begin": 1383918110000, "end": 1383918120000, "creator": "foobar", "category": "agree" },
        {"id": 3, "data": "Long",   "begin": 1383918210000, "end": 1383918220000, "creator": "foobar", "category": "disagree" },
        {"id": 4, "data": "time",   "begin": 1383918310000, "end": 1383918320000, "creator": "foobar", "category": "" },
        {"id": 5, "data": "ago",    "begin": 1383918410000, "end": 1383918420000, "creator": "foobar", "category": "reference" },
        {"id": 6, "data": "came",   "begin": 1383918510000, "end": 1383918520000, "creator": "foobar", "category": "question" },
        {"id": 7, "data": "a",      "begin": 1383918610000, "end": 1383918620000, "creator": "foobar", "category": "" },
        {"id": 8, "data": "man",    "begin": 1383918710000, "end": 1383918720000, "creator": "foobar", "category": "" },
        {"id": 9, "data": "on",     "begin": 1383918810000, "end": 1383918820000, "creator": "foobar", "category": "question" },
        {"id": 10, "data": "a",     "begin": 1383918910000, "end": 1383918920000, "creator": "foobar", "category": "question" },
        {"id": 11, "data": "track", "begin": 1383918990000, "end": 1383918999000, "creator": "foobar", "category": "agree" }
        ],

        findById = function (id) {
            var annotation = null,
                l = annotations.length,
                i;
            for (i = 0; i < l; i = i + 1) {
                if (annotations[i].id === id) {
                    annotation = annotations[i];
                    break;
                }
            }
            return annotation;
        },

        findByCreator = function (creatorId) {
            var results = annotations.filter(function (element) {
                return creatorId === element.creator;
            });
            return results;
        };


    angular.module('mla.memoryServices', [])
        .factory('Annotation', [
            function () {
                return {
                    query: function () {
                        return annotations;
                    },
                    get: function (annotation) {
                        return findById(parseInt(annotation.id));
                    },
                    append: function (data, begin, end, category, creator) {
                        if (end === undefined)
                            end = (new Date()).getTime();
                        if (creator === undefined)
                            creator = 'Anonymous';
                        annotations.push({
                            id: guid(),
                            data: data,
                            begin: begin,
                            end: end,
                            category: category,
                            creator: creator});
                    }
                }

            }]);

}());