var gulp = require('gulp'),
    sass = require('gulp-sass'),
    neat = require('node-neat').includePaths,
    watch = require('gulp-watch'),
    minifycss = require('gulp-minify-css'),
    uglify = require('gulp-uglifyjs'),
    rename = require('gulp-rename');

// compile all sass files into css folder and create minified file
gulp.task('sass', function() {
  return gulp.src('ekip/everykid/static/scss/*.scss')
    .pipe(sass({
      includePaths: ['styles'].concat(neat)
    }))
    .pipe(gulp.dest('ekip/everykid/static/css'))
    .pipe(rename({suffix: '.min'}))
    .pipe(minifycss())
    .pipe(gulp.dest('ekip/everykid/static/css'));
});

gulp.task('uglify', function() {
  gulp.src('ekip/everykid/static/js/script.js')
    .pipe(uglify())
    .pipe(gulp.dest('ekip/everykid/static/js/min'));

  gulp.src('ekip/everykid/static/js/voucher.js')
    .pipe(uglify())
    .pipe(gulp.dest('ekip/everykid/static/js/min'));

});

// change watcher
gulp.task('watch', function() {
  gulp.watch('ekip/everykid/static/scss/*.scss', ['sass']);
  gulp.watch('ekip/everykid/static/js/*.js', ['uglify']);
});

gulp.task('default', ['sass', 'uglify', 'watch']);

