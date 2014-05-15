(function ($, SirTrevor) {
    'use strict';

    SirTrevor.setBlockOptions("Tweet", {
        fetchUrl: function (tweetId) {
            return '/tweets/' + tweetId;
        },
    });

    SirTrevor.setDefaults({
        uploadUrl: '/images',
    });

    new SirTrevor.Editor({
        el: $('[name="raw_content"]'),

        blockTypes: [
            "Code",
            "Heading",
            "Text",
            "Image",
            "Tweet",
            "List",
            "Sourcedquote",
            "Video",
        ],

        defaultType: "Text",
    });
})(jQuery, SirTrevor);
