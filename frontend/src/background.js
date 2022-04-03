import {
    app,
    protocol,
    BrowserWindow,
    ipcMain,
    globalShortcut
} from 'electron'

import {
    createProtocol
} from 'vue-cli-plugin-electron-builder/lib'

const dev_mode = process.env.NODE_ENV !== 'production'

let win

protocol.registerSchemesAsPrivileged([{
    scheme: 'app',
    privileges: {
        secure: true,
        standard: true
    }
}])

function createWindow() {
    win = new BrowserWindow({
        width: 1400,
        height: 800,
        webPreferences: {
            nodeIntegration: true,
            nodeIntegrationInWorker: true,
            webSecurity: false,
            devTools: true
        },
        icon: `${__static}/logo.ico`
    })

    if (dev_mode) {
        win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
        // 安装 vue-devtools 调试插件
        let ses = win.webContents.session;
        let extensions = ses.getAllExtensions()
        if (!extensions['Vue.js devtools']) {
            ses.loadExtension('./vue-devtools')
        }
        if (!process.env.IS_TEST) {
            win.webContents.openDevTools({mode:'detach'})
        }
    } else {
        createProtocol('app')
        win.loadURL('app://./index.html')
    }

    win.on('closed', () => {
        win = null
    })

    win.setMenu(null);
}

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    if (win === null) {
        createWindow()
    }
})

app.on('ready', () => {
    createWindow()
})

app.on('browser-window-created', () => {
    if (dev_mode) {
        globalShortcut.register('f1', () => {
            win.webContents.openDevTools({mode:'detach'});
        })
        globalShortcut.register('f5', () => {
            win.webContents.reload();
        })
    }
})

// Exit cleanly on request from parent process in development mode.
if (dev_mode) {
    if (process.platform === 'win32') {
        process.on('message', data => {
            if (data === 'graceful-exit') {
                app.quit()
            }
        })
    } else {
        process.on('SIGTERM', () => {
            app.quit()
        })
    }
}

// 提供给渲染进程调用
ipcMain.on('open_url', (e, url, width, height) => {
    let new_win = new BrowserWindow({
        width: width,
        height: height,
        frame: true,
        parent: win,
    })
    new_win.loadURL(url);
    new_win.on('closed', () => {
        new_win = null
    })
});

ipcMain.on('hide', (e) => {
    win.hide();
});

ipcMain.on('exit', (e) => {
    win.destroy();
});

ipcMain.on('reload', (e) => {
    app.relaunch({
        args: process.argv.slice(1).concat(['–relaunch'])
    });
    app.exit(0)
});