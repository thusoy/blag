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
          copy: false,
        }
      }
    },

    /* Needed since sass/compass doesn't have any decent way to include plain CSS files yet */
    rename: {
      sirTrevor: {
        files: [
          {src: 'bower_components/sir-trevor-js/sir-trevor.css', dest: 'bower_components/sir-trevor-js/_sir-trevor.scss'},
          {src: 'bower_components/sir-trevor-js/sir-trevor-icons.css', dest: 'bower_components/sir-trevor-js/_sir-trevor-icons.scss'}
        ]
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
        'cover',
        '.coverage',
      ]
    },

    compass: {
      dist: {
        options: {
          sassDir: 'blag/static/sass/',
          cssDir: '.tmp/static/css/',
          outputStyle: 'compressed',
          importPath: ["bower_components"],
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
      'fetch-server-assets': {
        files: [{
          src: '.tmp/static/css/core.css',
          dest: 'blag/server-assets/core.css',
        },
        {
          src: '.tmp/static/js/inline.min.js',
          dest: 'blag/server-assets/inline.js',
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
      'build-static': {
        command: [
          'mkdir -p dist',
          'cd .tmp/static',
          'tar czf ../../dist/static.tar.gz *',
          'sha256sum ../../dist/static.tar.gz | cut -d" " -f1 > ../../dist/static.tar.gz.sha256',
        ].join(' && '),
      }
    },

    uglify: {
      options: {
        sourceMap: true,
        sourceMapIncludeSources: true,
      },
      static: {
        files: {
          '.tmp/static/js/main.min.js': [
            'blag/static/js/main.js',
          ],
          '.tmp/static/js/writePost.min.js': [
            'bower_components/jquery/dist/jquery.js',
            'bower_components/underscore/underscore.js',
            'bower_components/Eventable/eventable.js',
            'bower_components/sir-trevor-js/sir-trevor.js',
            'blag/static/js/blocks/code.js',
            'blag/static/js/blocks/markdown.js',
            'blag/static/js/blocks/sourced-quote.js',
            'blag/static/js/writeEntry.js',
          ],
        },
      },
      inline: {
        options: {
          sourceMap: false,
        },
        files: {
          '.tmp/static/js/inline.min.js': [
            'blag/static/js/inline.js',
          ],
        }
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
        tasks: ['buildStyles'],
      },
      js: {
        files: ['blag/static/js/**/*.js'],
        tasks: ['uglify']
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
    'clean',
    'prep',
    'rev-static',
    'shell:build-python',
    'shell:build-static',
  ]);

  grunt.registerTask('prep', [
    'clean',
    'compass',
    'uglify',
    'copy:fetch-server-assets',
    'imagemin',
    'copy:misc-static',
  ]);

  grunt.registerTask('rev-static', [
    'filerev',
    'filerev_assets',
  ]);

  grunt.registerTask('init-deps', [
    'bower',
    'rename:sirTrevor',
  ]);
};
