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

### 前端
进入 release/frontend/standard/ 目录，其中含有前端工具的安装包版本（navigation Setup.exe）和免安装版本（win-unpacked 目录），可以根据需要选择一种发布方式安装运行。
如需快速运行查看，可进入 win-unpacked 目录，执行其中的`navigation.exe`即可启动前端工具。

### 计算服务
进入 release/compute_service/ 目录，执行：
```shell
python server.pyc
```
可以将预置依赖库的 python 环境和编译后的计算服务打包发布，根据需要添加易用的启动脚本。

## 补充说明

data_service 目前只是一个预留框架（前端工具中也预留了相关接口），它需要结合具体的传感器接口实现。现有程序中，前端工具展示的传感器图表是动态生成的虚拟数据，而位置和航速数据来自计算服务。
