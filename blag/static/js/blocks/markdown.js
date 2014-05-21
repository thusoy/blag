/* jshint strict: false */

var blockUtils = {
  htmlToMarkdown: function (html) {

    var markdown = html.replace(/([^<>]+)(<div>)/g, "$1\n$2")               // Divitis style line breaks (handle the first line)
      .replace(/<div><div>/g, '\n<div>')                                    // ^ (double opening divs with one close from Chrome)
      .replace(/(?:<div>)([^<>]+)(?:<div>)/g, "$1\n")                       // ^ (handle nested divs that start with content)
      .replace(/(?:<div>)(?:<br>)?([^<>]+)(?:<br>)?(?:<\/div>)/g, "$1\n")   // ^ (handle content inside divs)
      .replace(/<\/p>/g, "\n\n")                                            // P tags as line breaks
      .replace(/<div><br><\/div>/g, "\n")
      .replace(/<(.)?br(.)?>/g, "\n")                                       // Convert normal line breaks
      .replace(/&lt;/g, "<").replace(/&gt;/g, ">");

    return markdown;
  },

  markdownToHtml: function (markdown) {
    var html = markdown.replace(/\r?\n/gm, "<br>");
    return html;
  }
};

SirTrevor.Blocks.Markdown = SirTrevor.Block.extend({

  type: "markdown",

  editorHTML: '<div class="st-required st-text-block" contenteditable="true"></div>',

  icon_name: 'text',

  toData: function () {
    var data = {};
    data.text = blockUtils.htmlToMarkdown(this.getTextBlock().html());
    this.setData(data);
    return data;
  },

  loadData: function (data) {
    this.getTextBlock().html(blockUtils.markdownToHtml(data.text));
  }
});
