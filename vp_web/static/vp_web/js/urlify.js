/*global XRegExp*/
(function() {
    'use strict';

    var LATIN_MAP = {
        '??': 'A', '??': 'A', '??': 'A', '??': 'A', '??': 'A', '??': 'A', '??': 'AE',
        '??': 'C', '??': 'E', '??': 'E', '??': 'E', '??': 'E', '??': 'I', '??': 'I',
        '??': 'I', '??': 'I', '??': 'D', '??': 'N', '??': 'O', '??': 'O', '??': 'O',
        '??': 'O', '??': 'O', '??': 'O', '??': 'O', '??': 'U', '??': 'U', '??': 'U',
        '??': 'U', '?¡ã': 'U', '??': 'Y', '??': 'TH', '??': 'Y', '??': 'ss', '??': 'a',
        '??': 'a', '?¡é': 'a', '?¡ê': 'a', '?¡è': 'a', '?£¤': 'a', '?|': 'ae', '?¡ì': 'c',
        '?¡§': 'e', '??': 'e', '?a': 'e', '??': 'e', '??': 'i', '?-': 'i', '??': 'i',
        '?¡¥': 'i', '?¡ã': 'd', '?¡À': 'n', '?2': 'o', '?3': 'o', '?¡ä': 'o', '?¦Ì': 'o',
        '??': 'o', '??': 'o', '??': 'o', '?1': 'u', '?o': 'u', '??': 'u', '??': 'u',
        '?¡À': 'u', '??': 'y', '??': 'th', '??': 'y'
    };
    var LATIN_SYMBOLS_MAP = {
        '??': '(c)'
    };
    var GREEK_MAP = {
        '?¡À': 'a', '?2': 'b', '?3': 'g', '?¡ä': 'd', '?¦Ì': 'e', '??': 'z', '?¡¤': 'h',
        '??': '8', '?1': 'i', '?o': 'k', '??': 'l', '??': 'm', '??': 'n', '??': '3',
        '??': 'o', '??': 'p', '??': 'r', '??': 's', '??': 't', '??': 'y', '??': 'f',
        '??': 'x', '??': 'ps', '??': 'w', '??': 'a', '?-': 'e', '?¡¥': 'i', '??': 'o',
        '??': 'y', '??': 'h', '??': 'w', '??': 's', '??': 'i', '?¡ã': 'y', '??': 'y',
        '??': 'i', '??': 'A', '??': 'B', '??': 'G', '??': 'D', '??': 'E', '??': 'Z',
        '??': 'H', '??': '8', '??': 'I', '??': 'K', '??': 'L', '??': 'M', '??': 'N',
        '??': '3', '??': 'O', '??': 'P', '??': 'R', '?¡ê': 'S', '?¡è': 'T', '?£¤': 'Y',
        '?|': 'F', '?¡ì': 'X', '?¡§': 'PS', '??': 'W', '??': 'A', '??': 'E', '??': 'I',
        '??': 'O', '??': 'Y', '??': 'H', '??': 'W', '?a': 'I', '??': 'Y'
    };
    var TURKISH_MAP = {
        '??': 's', '??': 'S', '?¡À': 'i', '?¡ã': 'I', '?¡ì': 'c', '??': 'C', '??': 'u',
        '??': 'U', '??': 'o', '??': 'O', '??': 'g', '??': 'G'
    };
    var ROMANIAN_MAP = {
        '??': 'a', '??': 'i', '¨¨?': 's', '¨¨?': 't', '?¡é': 'a',
        '??': 'A', '??': 'I', '¨¨?': 'S', '¨¨?': 'T', '??': 'A'
    };
    var RUSSIAN_MAP = {
        'D¡ã': 'a', 'D¡À': 'b', 'D2': 'v', 'D3': 'g', 'D¡ä': 'd', 'D¦Ì': 'e', '??': 'yo',
        'D?': 'zh', 'D¡¤': 'z', 'D?': 'i', 'D1': 'j', 'Do': 'k', 'D?': 'l', 'D?': 'm',
        'D?': 'n', 'D?': 'o', 'D?': 'p', '??': 'r', '??': 's', '??': 't', '??': 'u',
        '??': 'f', '??': 'h', '??': 'c', '??': 'ch', '??': 'sh', '??': 'sh', '??': '',
        '??': 'y', '??': '', '??': 'e', '??': 'yu', '??': 'ya',
        'D?': 'A', 'D?': 'B', 'D?': 'V', 'D?': 'G', 'D?': 'D', 'D?': 'E', 'D?': 'Yo',
        'D?': 'Zh', 'D?': 'Z', 'D?': 'I', 'D?': 'J', 'D?': 'K', 'D?': 'L', 'D?': 'M',
        'D?': 'N', 'D?': 'O', 'D?': 'P', 'D?': 'R', 'D?': 'S', 'D¡é': 'T', 'D¡ê': 'U',
        'D¡è': 'F', 'D£¤': 'H', 'D|': 'C', 'D¡ì': 'Ch', 'D¡§': 'Sh', 'D?': 'Sh', 'Da': '',
        'D?': 'Y', 'D?': '', 'D-': 'E', 'D?': 'Yu', 'D¡¥': 'Ya'
    };
    var UKRAINIAN_MAP = {
        'D?': 'Ye', 'D?': 'I', 'D?': 'Yi', '¨°?': 'G', '??': 'ye', '??': 'i',
        '??': 'yi', '¨°?': 'g'
    };
    var CZECH_MAP = {
        '??': 'c', '??': 'd', '??': 'e', '??': 'n', '??': 'r', '??': 's', '?£¤': 't',
        '?¡¥': 'u', '??': 'z', '??': 'C', '??': 'D', '??': 'E', '??': 'N', '??': 'R',
        '??': 'S', '?¡è': 'T', '??': 'U', '??': 'Z'
    };
    var POLISH_MAP = {
        '??': 'a', '??': 'c', '??': 'e', '??': 'l', '??': 'n', '?3': 'o', '??': 's',
        '?o': 'z', '??': 'z',
        '??': 'A', '??': 'C', '??': 'E', '??': 'L', '??': 'N', '??': 'O', '??': 'S',
        '?1': 'Z', '??': 'Z'
    };
    var LATVIAN_MAP = {
        '??': 'a', '??': 'c', '??': 'e', '?¡ê': 'g', '??': 'i', '?¡¤': 'k', '??': 'l',
        '??': 'n', '??': 's', '??': 'u', '??': 'z',
        '??': 'A', '??': 'C', '??': 'E', '?¡é': 'G', '?a': 'I', '??': 'K', '??': 'L',
        '??': 'N', '??': 'S', '?a': 'U', '??': 'Z'
    };
    var ARABIC_MAP = {
        '?¡ê': 'a', '?¡§': 'b', '?a': 't', '??': 'th', '??': 'g', '?-': 'h', '??': 'kh', '?¡¥': 'd',
        '?¡ã': 'th', '?¡À': 'r', '?2': 'z', '?3': 's', '?¡ä': 'sh', '?¦Ì': 's', '??': 'd', '?¡¤': 't',
        '??': 'th', '?1': 'aa', '?o': 'gh', '¨´?': 'f', '¨´?': 'k', '¨´?': 'k', '¨´?': 'l', '¨´?': 'm',
        '¨´?': 'n', '¨´?': 'h', '¨´?': 'o', '¨´?': 'y'
    };
    var LITHUANIAN_MAP = {
        '??': 'a', '??': 'c', '??': 'e', '??': 'e', '?¡¥': 'i', '??': 's', '?3': 'u',
        '??': 'u', '??': 'z',
        '??': 'A', '??': 'C', '??': 'E', '??': 'E', '??': 'I', '??': 'S', '?2': 'U',
        '?a': 'U', '??': 'Z'
    };
    var SERBIAN_MAP = {
        '??': 'dj', '??': 'j', '??': 'lj', '??': 'nj', '??': 'c', '??': 'dz',
        '??': 'dj', 'D?': 'Dj', 'D?': 'j', 'D?': 'Lj', 'D?': 'Nj', 'D?': 'C',
        'D?': 'Dz', '??': 'Dj'
    };
    var AZERBAIJANI_MAP = {
        '?¡ì': 'c', '¨¦?': 'e', '??': 'g', '?¡À': 'i', '??': 'o', '??': 's', '??': 'u',
        '??': 'C', '??': 'E', '??': 'G', '?¡ã': 'I', '??': 'O', '??': 'S', '??': 'U'
    };
    var GEORGIAN_MAP = {
        '¨¢??': 'a', '¨¢??': 'b', '¨¢??': 'g', '¨¢??': 'd', '¨¢??': 'e', '¨¢??': 'v', '¨¢??': 'z',
        '¨¢??': 't', '¨¢??': 'i', '¨¢??': 'k', '¨¢??': 'l', '¨¢??': 'm', '¨¢??': 'n', '¨¢??': 'o',
        '¨¢??': 'p', '¨¢??': 'j', '¨¢??': 'r', '¨¢??': 's', '¨¢?¡é': 't', '¨¢?¡ê': 'u', '¨¢?¡è': 'f',
        '¨¢?£¤': 'q', '¨¢?|': 'g', '¨¢?¡ì': 'y', '¨¢?¡§': 'sh', '¨¢??': 'ch', '¨¢?a': 'c', '¨¢??': 'dz',
        '¨¢??': 'w', '¨¢?-': 'ch', '¨¢??': 'x', '¨¢?¡¥': 'j', '¨¢?¡ã': 'h'
    };

    var ALL_DOWNCODE_MAPS = [
        LATIN_MAP,
        LATIN_SYMBOLS_MAP,
        GREEK_MAP,
        TURKISH_MAP,
        ROMANIAN_MAP,
        RUSSIAN_MAP,
        UKRAINIAN_MAP,
        CZECH_MAP,
        POLISH_MAP,
        LATVIAN_MAP,
        ARABIC_MAP,
        LITHUANIAN_MAP,
        SERBIAN_MAP,
        AZERBAIJANI_MAP,
        GEORGIAN_MAP
    ];

    var Downcoder = {
        'Initialize': function() {
            if (Downcoder.map) {  // already made
                return;
            }
            Downcoder.map = {};
            Downcoder.chars = [];
            for (var i = 0; i < ALL_DOWNCODE_MAPS.length; i++) {
                var lookup = ALL_DOWNCODE_MAPS[i];
                for (var c in lookup) {
                    if (lookup.hasOwnProperty(c)) {
                        Downcoder.map[c] = lookup[c];
                    }
                }
            }
            for (var k in Downcoder.map) {
                if (Downcoder.map.hasOwnProperty(k)) {
                    Downcoder.chars.push(k);
                }
            }
            Downcoder.regex = new RegExp(Downcoder.chars.join('|'), 'g');
        }
    };

    function downcode(slug) {
        Downcoder.Initialize();
        return slug.replace(Downcoder.regex, function(m) {
            return Downcoder.map[m];
        });
    }


    function URLify(s, num_chars, allowUnicode) {
        // changes, e.g., "Petty theft" to "petty-theft"
        // remove all these words from the string before urlifying
        if (!allowUnicode) {
            s = downcode(s);
        }
        var removelist = [
            "a", "an", "as", "at", "before", "but", "by", "for", "from", "is",
            "in", "into", "like", "of", "off", "on", "onto", "per", "since",
            "than", "the", "this", "that", "to", "up", "via", "with"
        ];
        var r = new RegExp('\\b(' + removelist.join('|') + ')\\b', 'gi');
        s = s.replace(r, '');
        // if downcode doesn't hit, the char will be stripped here
        if (allowUnicode) {
            // Keep Unicode letters including both lowercase and uppercase
            // characters, whitespace, and dash; remove other characters.
            s = XRegExp.replace(s, XRegExp('[^-_\\p{L}\\p{N}\\s]', 'g'), '');
        } else {
            s = s.replace(/[^-\w\s]/g, '');  // remove unneeded chars
        }
        s = s.replace(/^\s+|\s+$/g, '');   // trim leading/trailing spaces
        s = s.replace(/[-\s]+/g, '-');     // convert spaces to hyphens
        s = s.toLowerCase();               // convert to lowercase
        return s.substring(0, num_chars);  // trim to first num_chars chars
    }
    window.URLify = URLify;
})();
