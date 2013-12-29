module.exports = function(grunt) {

  // load grunt tasks from package.json
  require('load-grunt-tasks')(grunt);
  var S = require('string');

  // Project configuration.
  grunt.initConfig({

    bower: {
      install: {
        options: {
          targetDir: 'thusoy/static/libs',
        }
      }
    },

    clean: {
      dist: [
        '.tmp',
        'thusoy/static/css',
        'thusoy/**/*.pyc',
      ]
    },

    compass: {
      dist: {
        options: {
          sassDir: '.tmp/static/sass/',
          cssDir: 'thusoy/static/css/',
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
          cwd: 'thusoy/static/libs/sass-bootstrap/lib',
          src: ['_*'],
          dest: '.tmp/static/sass/bootstrap',
        }]
      },
      thusoySass: {
        files: [{
          expand: true,
          cwd: 'thusoy/static/sass',
          src: ['**'],
          dest: '.tmp/static/sass',
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
      }

    },

    'string-replace': {
      html: {
        files: {
          'thusoy/templates/base.html': 'thusoy/templates/_base.html',
        },
        options: {
          replacements: [{
            pattern: /{# import (.*?) #}/ig,
            replacement: function (match, p1) {
              return grunt.file.read(p1);
            }
          }]
        }
      },
    },

    uglify: {
      options: {
        sourceMap: function (uglifyDest) {
          return uglifyDest.slice(0, -3) + '.map';
        },
        sourceMapPrefix: 3,
        sourceMappingURL: function (uglifyDest) {
          // Strip the first 'thusoy' from the destination
          // replace \ wiht / to work on both windows and *nix
          return S(uglifyDest.slice(6)).replaceAll('\\', '/').slice(0, -2) + 'map';
        },
        //sourceMapRoot: 'thusoy/static',
      }
    },

    useminPrepare: {
      options: {
        dest: 'thusoy/static',
        root: 'thusoy/',
        flow: {
          html: {
            steps: {'js': ['uglifyjs']},
            post: {}
          }
        }
      },
      html: 'thusoy/**/templates/**/*.html',
    },

    watch: {
      options: {
        livereload: true,
      },
      python: {
        files: ['thusoy/**/*.py'],
        tasks: []
      },
      sass: {
        files: ['thusoy/static/sass/*.scss'],
        tasks: ['buildStyles', 'preprocess-html'],
      },
      js: {
        files: ['thusoy/static/js/*.js', '!**/*.min.js'],
        tasks: ['buildJs']
      },
      templates: {
        files: ['thusoy/templates/*.html', '!thusoy/templates/base.html'],
        tasks: ['preprocess-html'],
      },
    },

  });

  grunt.registerTask('default', [
    'clean',
    'build',
    'concurrent:server',
  ]);

  grunt.registerTask('preprocess-html', [
    'string-replace:html',
  ]);

  grunt.registerTask('build', [
    'buildStyles',
    'buildJs',
    'preprocess-html',
  ]);

  grunt.registerTask('buildStyles', [
    'copy',
    'compass',
  ]);

  grunt.registerTask('buildJs', [
    'useminPrepare',
    'uglify',
  ]);
};
