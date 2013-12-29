SirTrevor.setBlockOptions("Tweet", {
    fetchUrl: function (tweetId) {
        return '/tweets/' + tweetId;
    },
});

new SirTrevor.Editor({
    el: $('[name="raw_content"]'),
    uploadUrl: "/images",

    blockTypes: [
        "Text",
        "Sourcedquote",
    ],
});
