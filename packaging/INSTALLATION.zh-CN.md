# 独立 NextKde 应用

Calendar、Calculator、Weather 合用独立的 `NextKde/kos-apps` 源码仓库与版本；
ListenFree 继续使用自己的独立仓库。
KMusic 继续使用原有安装控制器，不经过这里的安装器。
Settings 与独立仓库随代码分发同一份 `tools/app-installer.py`，只依赖 Python 3 标准库；
安装时不会下载或执行替代安装器。

| 应用键 | 固定仓库 | 应用 ID | 可执行文件／桌面文件 ID |
| --- | --- | --- | --- |
| `calendar` | `NextKde/kos-apps` | `org.nextks.calendar` | `kos-calendar` |
| `calculator` | `NextKde/kos-apps` | `org.nextks.calculator` | `kos-calculator` |
| `weather` | `NextKde/kos-apps` | `org.nextks.weather` | `kos-weather` |
| `listenfree` | `NextKde/ListenFree` | `org.nextkde.ListenFree` | `listenfree` |

Todo 已整合进 Calendar 的提醒事项视图，不再提供独立启动入口。旧安装器管理的
`kos-todo` 链接仅为离线卸载和升级清理保留识别；不会删除外部安装的 Todo。

前三款新版桌面文件为 `org.nextks.<app>.desktop`，命令名不变；ListenFree 仍用
`listenfree.desktop`。商店条目不能指定仓库 URL、任意命令、
可执行文件名或安装根目录。

前三款共用 VERSION／commit／Release，但各有独立包和源码清单，构建时只选
`-DKOS_APPS=<app>`。旧 `org.nextkde.Calendar`、`org.nextkde.Calculator`、
`org.nextkde.Weather` Flatpak 是不同的退役 ref；Settings 报 RETIRED_FLATPAK_ID，
不提供跨身份资料复制；旧用户 ref 移除须单独确认，保留资料、不安装替代包；system／歧义安装交外部管理器。
参见 [兼容与手动过渡说明](ProfileMigration.md) 和 [人工验收矩阵](ProfileMigrationAcceptance.md)。
旧的三个单应用 GitHub 仓库已删除，改用 NextKde/kos-apps；新身份的签名 Release 尚未发布。
旧源码所有权 ID／桌面链接仍严格识别，支持离线查看状态和卸载。

## 命令接口

```sh
python3 packaging/installer.py --app calculator check-update
python3 packaging/installer.py --app calculator check
python3 packaging/installer.py --app calculator install --version 0.2.0
python3 packaging/installer.py --app calculator status
python3 packaging/installer.py --app calculator update
python3 packaging/installer.py --app calculator uninstall
```

可选参数 `--version X.Y.Z` 用来确认发现的最新稳定版本与请求一致，不是任意 tag 或
revision 选择器。版本必须是三个数字组成的语义版本，不接受预发布或构建后缀；比较时
按数字比较，拒绝降级，也拒绝在版本号不变时替换 revision。

- `check-update`：发现并验证版本元数据，不构建。
- `check`：额外下载并校验源码，执行真正的 CMake configure，检查应用开发依赖；
  不编译、不安装。
- `install`／`update`：配置、构建、安装到不可变版本目录，成功后再发布。
  已安装相同 revision 时幂等返回；`update` 要求先有受管理的安装。
- `status`／`uninstall`：完全离线。卸载只删除经校验属于安装器的入口链接、
  不可变版本和所有权清单；保留应用设置、用户数据和诊断日志。

安装器不使用 sudo，不安装系统包，不自动重跑失败构建，也不启动应用。
请自行通过发行版包管理器安装 Python 3、CMake、Ninja、C++ 编译器和应用文档列出的
开发依赖。缺少工具时会列出名称；配置失败返回 `DEPENDENCY_UNSATISFIED`，并给出
仅当前用户可读的完整日志路径。

## 结果协议

标准输出为 JSON Lines。每次操作恰好以一条 `type: "result"` 结束，此前可以有
`type: "progress"`。子进程输出只写入权限为 0600 的日志，不混入 JSON 协议。
所有记录包含 `schemaVersion: 1`、`appId`、`action`、`stage`、`type`、`success`、
`code`、`version`、`revision` 和对象 `details`。

`details` 提供 `installed`、`managed`、`available`、`version`、`revision`、
`currentVersion`、`currentRevision`、`desktopFile` 和 `root`。
其中 `available: true` 只表示本地安装引擎支持该应用，**不表示远端已发布版本**。
成功的 `check-update` 额外提供 `latestVersion` 和 `updateAvailable`。
版本发现失败仍然是失败，不能用商店内置版本号伪造安装状态；已知的本地安装信息会保留。

冲突返回 `EXTERNALLY_MANAGED`，并以 `installed: true`、`managed: false`、
`externalInstallation: true` 标记外部安装；找到固定桌面文件时提供 `desktopFile`。
安装器不会接管、升级或卸载外部安装。

退出码：0 成功，2 预期失败（依赖、版本、冲突、状态），3 子进程超时，130 取消，
1 未预期的安装器错误。无效命令参数也输出一条 JSON 结果；`--help` 正常打印帮助。

## 发布格式与信任边界

版本发现端点固定为：

```text
https://api.github.com/repos/NextKde/<仓库>/releases/latest
```

必须是已发布、非草稿、非预发布的稳定 release，tag 为 `vX.Y.Z`，并且有且仅有一个
属于所选 kos-apps 应用的 `<appId>.app-release.json` 附件（ListenFree 仍用
`app-release.json`）。清单示例：

```json
{
  "schemaVersion": 1,
  "appId": "org.nextks.calculator",
  "version": "0.1.0",
  "revision": "0123456789012345678901234567890123456789",
  "archiveSha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
}
```

示例散列值必须替换为实际 SHA256。可选 `archiveUrl` 必须严格等于：

```text
https://codeload.github.com/NextKde/<仓库>/tar.gz/<revision>
```

每份 JSON 响应最多 256 KiB，压缩源码最多 256 MiB，展开源码最多 1 GiB／100,000 项。
先校验 SHA256，再解包；拒绝路径穿越、符号链接、硬链接、特殊文件和重复路径。
压缩包必须只有一个顶层目录，并在根目录提供 CMake 项目。

初始 URL 只接受固定仓库的 HTTPS GitHub/API/codeload 路径；重定向另外允许 GitHub
固定附件域名，拒绝其他主机、非 HTTPS、URL 内凭据和非标准端口。
连接读取超时为 15 秒；Unix 主线程信号为完整请求提供元数据／源码每次尝试
45／300 秒的绝对时限，覆盖 DNS、重定向和响应头。整个版本发现过程（两份 JSON
及其重试）另外受 90 秒总时限约束；嵌套时限不会延长外层时限。
瞬时网络失败最多尝试三次并有限退避；TLS、完整性、404 和限流错误不重试。
404 返回 `RELEASE_UNAVAILABLE`；429 或 GitHub 403 限额耗尽返回 `RATE_LIMITED`，
在 GitHub 提供时附带 `retryAfter` 和 `rateLimitReset`。

**信任来自固定 NextKde GitHub 仓库的 HTTPS 发布，不是密码学发布签名。**
SHA256 将源码字节与该发布清单绑定，但不提供独立的发布者身份保证。
CMake 是可执行的构建逻辑，安装操作意味着信任白名单发布者；构建并未沙箱隔离。
不要通过改白名单来安装不可信来源。

## 存储、启动入口与所有权

- `${XDG_DATA_HOME:-~/.local/share}/nextkde-apps/KEY/versions/REVISION/`
- `.../KEY/current`：指向已发布不可变版本的原子切换链接
- `.../KEY/ownership.json`：版本与入口链接的准确所有权清单
- `${XDG_STATE_HOME:-~/.local/state}/nextkde-apps/KEY/{lock,logs/}`
- `~/.local/bin/EXECUTABLE`：经过 `current/bin` 的受管理链接
- `$XDG_DATA_HOME/applications/ID.desktop`：经过 `current` 的桌面入口链接
- `$XDG_DATA_HOME/dbus-1/services/NAME.service`：只为应用实际安装的服务创建

CMake 安装前缀直接使用最终版本路径，不是安装后再改名的临时路径。
发布前保留旧 `current`；配置、构建、安装失败会清理候选目录，旧版本继续可用。
升级成功后仍保留旧版本，直到显式 prune 或卸载。普通取消会向整个子进程组发 TERM，必要时再发 KILL；
配置、构建、安装各自的子进程时限为 30 分钟。

不会覆盖已有用户桌面文件、命令或服务文件；会检查 PATH 以及系统 XDG 桌面／D-Bus
位置中的发行版或 Nix 入口。Calendar 共享 PIM 服务必须直接使用不可变前缀中的
受管理可执行文件，不能通过可能指向另一安装的 systemd 服务启动。
已有核心 PIM 服务入口属于冲突，不会被静默替换；应人工确认包和运行中服务的归属。

应用状态目录中的私有 `transaction.json` 在修改前记录明确归属的候选版本及新旧清单。
后续调用取得锁后先恢复中断操作，离线状态检查／卸载也一样：所有权元数据提交前
回滚到旧版本，提交后向前完成新版本发布和旧服务入口清理；中断卸载按日志清单继续。
写入日志／清单和修改发布目录后进行持久化刷新，再丢弃恢复记录。
因此提交后的取消可能保留已经安装的新版本，不会假称始终保留旧版本。

日志损坏、入口被其他程序替换，或没有有效恢复日志的所有权清单／当前链接损坏时，
都拒绝猜测归属。不要通过删除或篡改清单强行继续。多文件卸载可恢复，但不是瞬间整体
原子操作；磁盘故障或外部替换仍可能需要人工恢复。直接 SIGKILL 安装器可能留下后台
构建进程，普通 TERM 取消才有清理机会。不自动回收旧版本；显式 cleanup-plan/prune 保留 current 和一个回退版本，见兼容说明。

## 人工验证

实际体验前使用隔离 HOME/XDG 目录。确认版本发现与缺依赖提示，安装后通过桌面入口
启动应用，升级到更新版本，取消构建后确认旧入口仍可用。离线检查状态、卸载后确认
应用用户数据保留。已有发行版／Nix／核心 PIM 服务入口时应报告冲突而不是替换。
安装器自身不要求重启合成器。
