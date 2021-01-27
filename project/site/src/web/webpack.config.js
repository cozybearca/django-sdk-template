const path = require("path")

module.exports = {
    entry: {
        base: "base/webpack",
        home: "home/webpack",
    },
    devtool: "inline-source-map",
    output: {
        library: "[name]",
        libraryTarget: "var",
        filename: "[name].js",
        path: path.resolve(process.env.COLLECT_STATIC_DIR, "webpack"),
    },
    resolveLoader: {
        modules: ["./node_modules"],
    },
    resolve: {
        modules: [".", "./node_modules"],
        extensions: [".ts", ".js"],
    },
    mode: "development",
    module: {
        rules: [
            {
                test: /\.tsx?$/i,
                use: {
                    loader: "ts-loader",
                    options: {
                        configFile: "tsconfig.webpack.json",
                        onlyCompileBundledFiles: true,
                        compilerOptions: {
                            target: "es5",
                            moduleResolution: "node",
                            sourceMap: true,
                            allowJs: true,
                            strict: true,
                            noImplicitAny: true,
                            downlevelIteration: true,
                            baseUrl: ".",
                            typeRoots: [path.resolve(__dirname, "node_modules/@types")],
                            paths: {
                                "*": [
                                    "*",
                                    "base/*",
                                    path.resolve(__dirname, "node_modules/*"),
                                ],
                            },
                        },
                    },
                },
            },
            {
                test: /\.css$/i,
                use: ["style-loader", "css-loader"],
            },
            {
                test: /\.less$/i,
                use: [
                    "style-loader",
                    "css-loader",
                    {
                        loader: "less-loader",
                        options: {
                            paths: [__dirname],
                        },
                    },
                ],
            },
            {
                test: /\.scss$/i,
                use: ["style-loader", "css-loader", "sass-loader"],
            },
            {
                test: /\.(woff(2)?|ttf|eot|svg|gif)(\?v=\d+\.\d+\.\d+)?$/,
                use: [
                    {
                        loader: "file-loader",
                        options: {
                            name: "[name].[ext]",
                            outputPath: "assets",
                            publicPath: "static/assets",
                        },
                    },
                ],
            },
        ],
    },
}
