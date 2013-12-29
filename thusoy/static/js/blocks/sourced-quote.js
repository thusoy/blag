/*
* A quote block that also adds a source URL for the quote.
* Data sent is like this:
*
*/

SirTrevor.Blocks.Sourcedquote = (function(){

  var template = _.template([
    '<blockquote class="st-required st-text-block" contenteditable="true"></blockquote>',
    '<label class="st-input-label">Credit</label>',
    '<input maxlength="140" name="author" placeholder="Credit" class="st-input-string st-required js-cite-input" type="text">',
    '<label class="st-input-label">Source</label>',
    '<input name="source" placeholder="Source" class"st-input-string st-required js-cite-input" type="text">',
  ].join("\n"));

  return SirTrevor.Block.extend({

    type: 'sourced_quote',

    icon_name: 'quote',

    editorHTML: function() {
      return template(this);
    },

    loadData: function(data){
      this.getTextBlock().html(SirTrevor.toHTML(data.text, this.type));
      this.$('.js-cite-input').val(data.cite);
    },

  });

})();
