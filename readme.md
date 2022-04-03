## 构建

### 前端
进入 frontend 目录：

1、安装 node 依赖
```shell
npm install
```
2、执行 `build.ps1`脚本
构建完成后，相关二进制会输出到项目根目录下的 release/frontend/standard/ 中。

### 计算服务
进入 compute_service 目录，执行 `build.ps1`脚本。
构建完成后，相关二进制会输出到项目根目录下的 release/compute_service/ 中。

## 运行

### 安装 python 依赖
```shell
python -m pip install -r python_env.txt
```

### 计算服务

进入 release/compute_service/ 目录，执行：

```shell
python server.pyc
```

### 地图服务

进入 map_tile_service 目录，解压其中的`zip`文件，解压后执行其中的`run.bat`即可启动地图瓦片服务，前端工具将请求此服务以显示航海地图，仅用于测试阶段。

### 前端

进入 release/frontend/standard/ 目录，其中含有前端工具的安装包版本（navigation Setup.exe）和免安装版本（win-unpacked 目录），可以根据需要选择一种发布方式安装运行。
如需快速运行查看，可进入 win-unpacked 目录，执行其中的`navigation.exe`即可启动前端工具。

## 补充说明

data_service 目前只是一个预留框架（前端工具中也预留了相关接口），它需要结合具体的传感器接口实现。现有程序中，前端工具展示的传感器图表是动态生成的虚拟数据，而位置和航速数据来自计算服务。

map_tile_service 是从某卫星企业提供的民用海事地图上抓取的地图瓦片，按地图瓦片服务协议分级归档，这里我只取了沿海地区的部分数据，仅用于开发测试阶段，如涉及版权和安全问题，请地图提供方联系我删除。

敬告：本项目源码未经作者许可，严禁商用，违者将被追究法律责任。
