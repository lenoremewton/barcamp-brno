module.exports = function(grunt) {
  require('jit-grunt')(grunt);

  grunt.initConfig({
    less: {
      development: {
        options: {
          // compress: true,
          // yuicompress: true,
          // optimization: 2
        },
        files: {
          "static/css/main.css": "static/less/main.less" // destination file and source file
        }
      }
    },
    watch: {
      styles: {
        files: ['static/less/**/*.less'], // which files to watch
        tasks: ['less'],
        options: {
          nospawn: true
        }
      }
    }
  });

  grunt.registerTask('default', ['less']);
};