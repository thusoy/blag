/* global module, require */

module.exports = function (grunt) {
  'use strict';
  /* jshint maxstatements: false */
  /* jshint camelcase: false */

  // load grunt tasks from package.json
  require('load-grunt-tasks')(grunt);

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

    filerev_assets: {
      dist: {
        options: {
          cwd: '.tmp/static/',
          dest: 'blag/server-assets/filerevs.json',
          prettyPrint: true,
        }
      }
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
        sourceMap: true,
        sourceMapIncludeSources: true,
      },
      static: {
        files: {
          '.tmp/static/js/main.min.js': [
            'blag/static/libs/jquery/dist/jquery.js',
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
        tasks: ['copy:blagSass', 'compass'],
      },
      js: {
        files: ['blag/static/js/**/*.js'],
        tasks: ['buildJs']
      },
      templates: {
        files: ['blag/templates/*.html'],
        tasks: [],
      },
    },
  });

  grunt.registerTask('default', [
    'prep',
    'concurrent:server',
  ]);

  grunt.registerTask('build', [
    'prep',
    'rev-static',
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
  ]);

  grunt.registerTask('rev-static', [
    'filerev',
    'filerev_assets',
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
