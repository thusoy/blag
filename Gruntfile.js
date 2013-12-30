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
        'dist',
        'thusoy/**/*.pyc',
        'thusoy/server-assets',
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
      },
      python: {
        files: [{
          expand: true,
          cwd: 'thusoy',
          src: ['**', '!static/**'],
          dest: '.tmp/thusoy'
        },
        {
          src: 'setup.py',
          dest: '.tmp/setup.py'
        }]
      },
      'server-assets-dev': {
        files: [{
          src: '.tmp/static/css/core.css',
          dest: 'thusoy/server-assets/core.css',
        }]
      },
      'server-assets-dist': {
        files: [{
          src: '.tmp/static/css/core.css',
          dest: '.tmp/thusoy/server-assets/core.css',
        }]
      },
    },

    imagemin: {
      static: {
        files: [{
          expand: true,
          cwd: 'thusoy/static/',
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
        command: 'python .tmp/setup.py sdist --formats gztar'
      },
      'package-static': {
        command: [
          'cd .tmp/static',
          'tar czf ../../dist/static.tar.gz *',
        ].join('&&')
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
        //sourceMapRoot: 'thusoy/static',
      }
    },

    useminPrepare: {
      options: {
        dest: '.tmp/static',
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
    'build',
    'concurrent:server',
  ]);

  grunt.registerTask('build', [
    'clean',
    'buildStyles',
    'buildJs',
    'imagemin',
    'server-assets',
    'copy:python',
    'shell:build-python',
    'shell:package-static',
  ]);

  grunt.registerTask('buildStyles', [
    'copy:bootstrap',
    'copy:thusoySass',
    'compass',
  ]);

  grunt.registerTask('server-assets', [
    'copy:server-assets-dev',
    'copy:server-assets-dist',
  ]);

  grunt.registerTask('buildJs', [
    'useminPrepare',
    'uglify',
  ]);
};
