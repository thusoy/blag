module.exports = function(grunt) {

  // load grunt tasks from package.json
  require('load-grunt-tasks')(grunt);
  var S = require('string');

  function items(obj, callback){
    Object.keys(obj).forEach(function(key, i){
      callback(key, obj[key], i);
    });
  }

  // Project configuration.
  grunt.initConfig({

    bower: {
      install: {
        options: {
          targetDir: 'blag/static/libs',
        }
      }
    },

    clean: {
      dist: [
        '.tmp',
        'dist',
        'blag/**/*.pyc',
        'blag/server-assets',
        'thusoy-blag-0.1.0',
        '*.egg-info',
      ]
    },

    compass: {
      dist: {
        options: {
          sassDir: '.tmp/static/sass/',
          cssDir: '.tmp/static/css/',
          outputStyle: 'compressed',
        }
      }
    },

    concurrent: {
      server: {
        tasks: ['watch', 'shell:server'],
        options: {
          logConcurrentOutput: true,
        }
      }
    },

    copy: {
      bootstrap: {
        files: [{
          expand: true,
          cwd: 'blag/static/libs/sass-bootstrap/lib',
          src: ['_*'],
          dest: '.tmp/static/sass/bootstrap',
        }]
      },
      blagSass: {
        files: [{
          expand: true,
          cwd: 'blag/static/sass',
          src: ['**'],
          dest: '.tmp/static/sass',
        }]
      },
      'fetch-server-assets': {
        files: [{
          src: '.tmp/static/css/core.css',
          dest: 'blag/server-assets/core.css',
        }]
      },
      'js-sources': {
        files: [{
          expand: true,
          cwd: 'blag/static/js',
          src: '**/*.js',
          dest: '.tmp/static/js/',
        }]
      },
      'misc-static': {
        files: [{
          expand: true,
          cwd: 'blag/static',
          src: ['img/favicon.ico'],
          dest: '.tmp/static/',
        }]
      },
    },

    filerev: {
      options: {
        algorithm: 'md5',
        length: 8,
      },
      images: {
        src: '.tmp/static/img/*.jpg',
      },
      styles: {
        src: '.tmp/static/css/*.css',
      },
      js: {
        src: '.tmp/static/js/*.js',
      },
      misc: {
        src: [
          '.tmp/static/img/favicon.ico',
        ]
      },
    },

    imagemin: {
      static: {
        files: [{
          expand: true,
          cwd: 'blag/static/',
          src: 'img/*.{png,jpg}',
          dest: '.tmp/static/',
        }]
      }
    },

    shell: {
      options: {
        stdout: true,
        stderr: true,
      },
      server: {
        command: 'python manage.py devserver',
      },
      'build-python': {
        command: 'python setup.py sdist --formats gztar'
      },
    },

    uglify: {
      options: {
        sourceMap: function (uglifyDest) {
          return uglifyDest.slice(0, -3) + '.map';
        },
        sourceMapPrefix: 3,
        sourceMappingURL: function (uglifyDest) {
          // Strip the first '.tmp' from the destination
          // replace \ with / to work on both windows and *nix
          return S(uglifyDest.slice(4)).replaceAll('\\', '/').slice(0, -2) + 'map';
        },
        //sourceMapRoot: 'blag/static',
      },
      static: {
        files: {
          '.tmp/static/js/main.min.js': [
            'blag/static/js/main.js',
          ],
          '.tmp/static/js/writePost.min.js': [
            'blag/static/libs/underscore/underscore.js',
            'blag/static/libs/Eventable/eventable.js',
            'blag/static/libs/sir-trevor-js/sir-trevor.js',
            'blag/static/js/blocks/code.js',
            'blag/static/js/blocks/sourced-quote.js',
            'blag/static/js/writeEntry.js',
          ],
        }
      },
    },

    cssmin: {
      static: {
        files: {
          '.tmp/static/css/writePost.min.css': [
            'blag/static/libs/sir-trevor-js/sir-trevor.css',
            'blag/static/libs/sir-trevor-js/sir-trevor-icons.css',
          ],
        }
      }
    },

    compress: {
      static: {
        options: {
          archive: 'dist/static.tar.gz',
        },
        files: [
          {expand: true, src: ['**'], cwd: '.tmp/static'},
        ],
      }
    },

    watch: {
      options: {
        livereload: true,
      },
      python: {
        files: ['blag/**/*.py'],
        tasks: []
      },
      sass: {
        files: ['blag/static/sass/*.scss'],
        tasks: ['buildStyles', 'preprocess-html'],
      },
      js: {
        files: ['blag/static/js/*.js', '!**/*.min.js'],
        tasks: ['buildJs']
      },
      templates: {
        files: ['blag/templates/*.html', '!blag/templates/base.html'],
        tasks: ['preprocess-html'],
      },
    },

  });

  grunt.registerTask('dump-revs', 'Dump the changes by filerev to a json file', function(){
    var revs = {};
    items(grunt.filerev.summary, function(key, val){
      var stripLeadingDirs = function (path) {
        return S(path.substring('.tmp/static/'.length)).replaceAll('\\', '/').toString();
      };
      revs[stripLeadingDirs(key)] = stripLeadingDirs(val);
    });
    grunt.file.write('blag/server-assets/filerevs.json', JSON.stringify(revs));
  });

  grunt.registerTask('default', [
    'prep',
    'concurrent:server',
  ]);

  grunt.registerTask('build', [
    'prep',
    'shell:build-python',
    'compress:static',
  ]);

  grunt.registerTask('prep', [
    'clean',
    'buildStyles',
    'buildJs',
    'imagemin',
    'copy:misc-static',
    'server-assets',
    'rev-static',
    'copy:js-sources',
  ]);

  grunt.registerTask('rev-static', [
    'filerev',
    'dump-revs',
  ]);

  grunt.registerTask('buildStyles', [
    'copy:bootstrap',
    'copy:blagSass',
    'compass',
    'cssmin',
  ]);

  grunt.registerTask('server-assets', [
    'copy:fetch-server-assets',
  ]);

  grunt.registerTask('buildJs', [
    'uglify',
  ]);
};
