/*
* A quote block that also adds a source URL for the quote.
* Data sent is like this:
*
*/

SirTrevor.Blocks.SourcedQuote = SirTrevor.Block.extend({

  type: 'sourced_quote',

  title: 'Quote with source',

  icon_name: 'quote',

  editorHTML: [
    '<blockquote class="st-required st-text-block" contenteditable="true"></blockquote>',
    '<label class="st-input-label">Credit</label>',
    '<input maxlength="140" name="author" placeholder="Credit" class="st-input-string st-required js-author-input" type="text">',
    '<label class="st-input-label">Source</label>',
    '<input name="source" placeholder="Source" class"st-input-string st-required js-source-input" type="url">',
  ].join("\n"),

  loadData: function (data) {
    this.getTextBlock().html(SirTrevor.toHTML(data.text, this.type));
    this.$('.js-author-input').val(data.author);
    this.$('.js-source-input').val(data.source);
  },

});
