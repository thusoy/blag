(function ($, SirTrevor, _) {
  'use strict';

  var uploadFileWithData = function (block, file, extraData, onSuccess, onError) {
    var uid = [block.blockID, (new Date()).getTime(), 'raw'].join('-');
    var data = new FormData();

    data.append('attachment[name]', file.name);
    data.append('attachment[file]', file);
    data.append('attachment[uid]', uid);
    data.append('data', JSON.stringify(extraData));

    block.resetMessages();

    var callbackSuccess = function () {
      SirTrevor.log('Upload callback called');

      if (_.isFunction(onSuccess)) {
        onSuccess.apply(block, arguments);
      }
    };

    var callbackError = function () {
      SirTrevor.log('Upload callback error called');

      if (_.isFunction(onError)) {
        onError.apply(block, arguments);
      }
    };

    var xhr = $.ajax({
      url: SirTrevor.DEFAULTS.uploadUrl,
      data: data,
      cache: false,
      contentType: false,
      processData: false,
      dataType: 'json',
      type: 'POST'
    });

    block.addQueuedItem(uid, xhr);

    xhr.done(callbackSuccess)
       .fail(callbackError)
       .always(_.bind(block.removeQueuedItem, block, uid));

    return xhr;
  };


  SirTrevor.Blocks.AltImage = SirTrevor.Block.extend({
    type: 'alt_image',
    title: 'Image',

    /*droppable: true,*/
    uploadable: true,
    editorHTML: '<label>Description: </label><input type="text" placeholder="Short description" ' +
      'class="st-input-string">',

    icon_name: 'image',

    loadData: function (data) {
      // Create our image tag
      this.$editor.html($('<img>', {src: data.imageUrl}));
    },

    toData: function () {
      var data = {
        'altText': this.$('input[type="text"]').val(),
      };
      this.setData(data);
    },

    onBlockRender: function () {
      /* Setup the upload button */
      this.$inputs.find('button').bind('click', function (ev) { ev.preventDefault(); });
      this.$inputs.find('input').on('change', _.bind(function (ev) {
        this.onDrop(ev.currentTarget);
      }, this));
    },

    onUploadSuccess: function (data) {
      this.setData(data);
      this.ready();
    },

    onUploadError: function () {
      this.addMessage(i18n.t('blocks:image:upload_error'));
      this.ready();
    },

    onDrop: function (transferData) {
      var file = transferData.files[0],
          urlAPI = (typeof URL !== "undefined") ? URL :
            (typeof webkitURL !== "undefined") ? webkitURL : null;

      // Handle one upload at a time
      if (/image/.test(file.type)) {
        this.loading();
        // Show this image on here
        this.$inputs.hide();
        this.$editor.html($('<img>', { src: urlAPI.createObjectURL(file) })).show();
        this.toData();

        uploadFileWithData(this, file, this.blockStorage.data, this.onUploadSuccess,
          this.onUploadError);
      }
    }
  });
})(jQuery, SirTrevor, _);
