## 环境说明
python3+

## 使用的第三方库
| 库名 | 用途 |
|----|----|
| requests | 构造 HTTP 请求 |
| PyExecJS   | 运行 JS 脚本   |

```
pip install requests
pip install PyExecJS
```

## 使用流程
1. 准备好 python3 运行环境并安装所需第三方库
2. 修改 `setting.py` 中的 `CONFIG` 项，将自己的智慧济大用户名密码填入
3. 切换到项目根目录执行 `python run.py` 命令

## 错误处理
为每一个操作点都增加了异常捕获，当程序运行过程中出现异常则停止程序进程并将异常记录到 log 目录

## 请求流程梳理
1. 调用 sso.ujn.edu.cn 获取 fanxiao.ujn.edu.cn 的 TOKEN 获取连接
2. 调用 fanxiao.ujn.edu.cn 的 TOKEN 获取连接获取 fanxiao.ujn.edu.cn 的 TOKEN
3. 调用 fanxiao.ujn.edu.cn 的 createTemperatureRecordCopy 接口方法生成体温记录

注：其中 1 和 2 应在同一会话下完成

## 未来可期
1. 增加报错后自动重试
2. 增加报错短信提醒
3. 增加当前已填写情况输出
