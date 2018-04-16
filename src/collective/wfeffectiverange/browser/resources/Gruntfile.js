module.exports = function (grunt) {
    "use strict";
    grunt.initConfig({
        pkg: grunt.file.readJSON("package.json"),
        // we could just concatenate everything, really
        // but we like to have it the complex way.
        // also, in this way we do not have to worry
        // about putting files in the correct order
        // (the dependency tree is walked by r.js)
        less: {
            dist: {
                options: {
                    paths: [],
                    strictMath: false,
                    sourceMap: true,
                    outputSourceFiles: true,
                    sourceMapFileInline: false,
                    sourceMapURL: "++resource++collective.wfeffectiverange/wfeffectiverange-compiled.less.map",
                    sourceMapFilename: "wfeffectiverange-compiled.less.map",
                    modifyVars: {
                        isPlone: "false"
                    }
                },
                files: {
                    "wfeffectiverange-compiled.css": "wfeffectiverange.less"
                }
            }
        },
        postcss: {
            options: {
                map: false,
                processors: [
                    require("autoprefixer")({
                        browsers: ["last 2 versions"]
                    })
                ]
            },
            dist: {
                src: "*.css"
            }
        },
        watch: {
            scripts: {
                files: [
                    "*.less"
                ],
                tasks: ["less", "postcss"]
            }
        },
        browserSync: {
            html: {
                bsFiles: {
                    src : [
                      "*.less"
                    ]
                },
                options: {
                    watchTask: true,
                    debugInfo: true,
                    online: true,
                    server: {
                        baseDir: "."
                    },
                }
            },
            plone: {
                bsFiles: {
                    src : [
                      "*.less"
                    ]
                },
                options: {
                    watchTask: true,
                    debugInfo: true,
                    proxy: "localhost:8080",
                    reloadDelay: 3000,
                    // reloadDebounce: 2000,
                    browser: ["google chrome"],
                    online: true
                }
            }
        }
    });


    // grunt.loadTasks("tasks");
    grunt.loadNpmTasks("grunt-browser-sync");
    grunt.loadNpmTasks("grunt-contrib-watch");
    grunt.loadNpmTasks("grunt-contrib-less");
    grunt.loadNpmTasks("grunt-postcss");

    // CWD to theme folder
    grunt.file.setBase("./");

    grunt.registerTask("compile", ["less", "postcss"]);
    grunt.registerTask("default", ["compile"]);
    grunt.registerTask("bsync", ["browserSync:html", "watch"]);
    grunt.registerTask("plone-bsync", ["browserSync:plone", "watch"]);
};
