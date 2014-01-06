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
      'fetch-server-assets': {
        files: [{
          src: '.tmp/static/css/core.css',
          dest: 'thusoy/server-assets/core.css',
        }]
      },
      'js-sources': {
        files: [{
          expand: true,
          cwd: 'thusoy/static/js',
          src: '**/*.js',
          dest: '.tmp/static/js/',
        }]
      }
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
      }
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
        command: 'python setup.py sdist --formats gztar'
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
      html: 'thusoy/templates/**/*.html',
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

  grunt.registerTask('dump-revs', 'Dump the changes by filerev to a json file', function(){
    var revs = {};
    items(grunt.filerev.summary, function(key, val){
      var stripLeadingDirs = function (path) {
        return S(path.substring('.tmp/static/'.length)).replaceAll('\\', '/').toString();
      };
      revs[stripLeadingDirs(key)] = stripLeadingDirs(val);
    });
    grunt.file.write('thusoy/server-assets/filerevs.json', JSON.stringify(revs));
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
    'rev-static',
    'copy:js-sources',
    'shell:build-python',
    'shell:package-static',
  ]);

  grunt.registerTask('rev-static', [
    'filerev',
    'dump-revs',
  ]);

  grunt.registerTask('buildStyles', [
    'copy:bootstrap',
    'copy:thusoySass',
    'compass',
  ]);

  grunt.registerTask('server-assets', [
    'copy:fetch-server-assets',
  ]);

  grunt.registerTask('buildJs', [
    'useminPrepare',
    'uglify',
  ]);
};
