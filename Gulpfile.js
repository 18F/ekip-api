var gulp = require('gulp'),
    sass = require('gulp-sass'),
    neat = require('node-neat').includePaths,
    watch = require('gulp-watch'),
    minifycss = require('gulp-minify-css'),
    rename = require('gulp-rename'),
    gzip = require('gulp-gzip');

var gzip_options = {
    threshold: '1kb',
    gzipOptions: {
        level: 9
    }
};

/* Compile Our Sass */
gulp.task('sass', function() {
    return gulp.src('ekip/everykid/static/scss/*.scss')
        .pipe(sass({
          includePaths: ['styles'].concat(neat)
        }))
        .pipe(gulp.dest('ekip/everykid/static/css'))
        .pipe(rename({suffix: '.min'}))
        .pipe(minifycss())
        .pipe(gulp.dest('ekip/everykid/static/css'))
        .pipe(gzip(gzip_options))
        .pipe(gulp.dest('ekip/everykid/static/css'));
});

/* Watch Files For Changes */
gulp.task('watch', function() {
    gulp.watch('ekip/everykid/static/scss/*.scss', ['sass']);
});

gulp.task('default', ['sass', 'watch']);

