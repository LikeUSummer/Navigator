const path = require('path')

function resolve(dir) {
  return path.join(__dirname, dir)
}

module.exports = {
  publicPath: './', // 根目录形式，由于是本地页面，故采用相 './' 而非 '/'
  assetsDir: '',
  outputDir: 'dist', // 页面源码构建输出目录

  lintOnSave: true, // eslint-loader 是否在保存的时候检查

  // webpack 配置
  chainWebpack: config => {
    config.resolve.symlinks(true)
  },
  configureWebpack: config => {
    config.module.rules.push({
      test: /\.(cur)$/, 
      loader: 'url-loader', 
      options: { 
        limit: 8000,
        name: 'images/[name]_[hash:7].[ext]',
      }
    })
  },

  // 生产环境是否生成 sourceMap 文件
  productionSourceMap: true,

  // css 相关配置
  css: {
    // extract: true,
    sourceMap: false,
    // css 预设器配置项
    loaderOptions: {},
    requireModuleExtension: true // 仅对 .module.css 后缀的文件做模块化处理
  },

  // use thread-loader for babel & TS in production build
  parallel: require('os').cpus().length > 1,

  // 是否启用 dll
  // dll: false,

  // PWA 插件相关配置
  pwa: {},

  // webpack-dev-server 相关配置
  devServer: {
    open: process.platform === 'darwin',
    disableHostCheck: true,
    host: '127.0.0.1',
    port: 1234,
    https: false,
    hotOnly: false,
    before: app => {}
  },
  
  // 第三方插件配置
  pluginOptions: {
    electronBuilder: {
      builderOptions: {
        "productName": "navigation",
        "appId": "com.summer.east",
        "copyright": "版权所有@东方盛夏",
        "asar": false,
        "files": ["**/*"],
        "directories": {
          "output": "../release/frontend/standard/"
        },
        "nsis": {
          "oneClick": false,
          "allowElevation": true,
          "allowToChangeInstallationDirectory": true,
          "installerIcon": "./prebuilt/logo256.ico",
          "uninstallerIcon": "./prebuilt/uninstall.ico",
          "installerHeaderIcon": "./prebuilt/logo64.ico",
          "createDesktopShortcut": true,
          "createStartMenuShortcut": true,
          "shortcutName": "TugMaster"
        },
        "dmg": {
          "contents": [
            {
              "x": 410,
              "y": 150,
              "type": "link",
              "path": "/Applications"
            },
            {
              "x": 130,
              "y": 150,
              "type": "file"
            }
          ]
        },
        "mac": {
          "icon": "./prebuilt/logo.icns"
        },
        "win": {
          "icon": "./prebuilt/logo256.ico",
          target: [{
            target: 'nsis',
            'arch': [
              'x64'
              // 'ia32'
            ]
          }]
        },
        "linux": {
          "icon": "./prebuilt/logo.png"
        }
      }
    }
  }
}