/* jshint strict: false */

SirTrevor.Blocks.Code = SirTrevor.Block.extend({

  type: "code",

  title: 'Code',

  editorHTML: [
    '<textarea class="st-text-block st-code-block"></textarea>',
    '<input type=text class="st-input-string js-language-input" name="language"',
    'placeholder="Language" style="width: 100%; margin-top: 10px; text-align: center">',
  ].join('\n'),

  icon_name: 'quote',

  toData: function () {
    var data = {};
    data.text = this.getTextBlock().val();
    data.language = this.$('.js-language-input').val();
    this.setData(data);
    return data;
  },

  loadData: function (data) {
    this.getTextBlock().val(data.text);
    this.$('.js-language-input').val(data.language);
  }
});
