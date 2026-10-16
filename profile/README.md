<div align="center">

# 安信可科技 · Ai-Thinker

**让物联网开发更简单 · Making IoT Development Simpler**

[产品官网 Website](https://www.ai-thinker.com) ·
[文档中心 Docs](https://docs.ai-thinker.com) ·
[商城 Store](https://shop.ai-thinker.com) ·
[社区 Community](https://www.ai-thinker.com/community)

[![Followers](https://img.shields.io/github/followers/Ai-Thinker-AiPi?label=Followers&style=flat-square)](https://github.com/Ai-Thinker-AiPi)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

</div>

---

## 关于我们 About

安信可科技是一家专注于**无线通信模组**与**物联网开发平台**的科技公司，总部位于中国深圳，在上海、北京设有分支机构。公司围绕 Wi-Fi / Bluetooth 模组、MCU 主控方案与配套开发工具，构建了从芯片、模组、固件到开发板的完整产品体系，服务高校教学、创客 DIY、工业物联与 AIoT 应用开发者。

Ai-Thinker builds **wireless communication modules** and **IoT development platforms** for makers, educators, and industry engineers — from chips and modules to firmware, reference boards, and debugging tools.

> 📌 发布前请核对型号命名与文档路径与官网实际在售产品保持一致。

---

## 产品线 Product Lines

| 产品线 | 说明 | 常用主控 |
| --- | --- | --- |
| **Wi-Fi / BLE 模组**<br>Wireless Modules | 串口透传、低功耗、认证齐全的无线模组 | ESP32-S3 / ESP32-C6 |
| **RISC-V MCU**<br>MCU Series | 高性能 RISC-V 主控，配套官方 SDK | BL618 / BL616 / BL602 |
| **开发板与评估板**<br>Development Boards | 免焊验证、传感器扩展、一键烧录 | ESP32-S3 / BL618 |
| **调试与烧录工具**<br>Debug & Flash Tools | SWD 调试 + 高速串口 + USB 测试 | ST-LinK343 |
| **AI 应用方案**<br>AI Solutions | 语音交互、端侧 AI、IoT + LLM 集成 | BL618 / ESP32-S3 |

---

## 快速上手 Quick Start

### 1️⃣ 选型 Select a Module

按核心需求快速定位模组：

```text
需要 Wi-Fi + BLE + 摄像头 ？      → ESP32-S3 系列
需要高主频 + 大存储 + RISC-V ？   → BL618 / BL616
需要超低成本 Wi-Fi 模组？         → BL602
只需要串口透传，快速联网？        → Wi-Fi 串口透传模组
```

### 2️⃣ 烧录与调试 Flash & Debug

新板到手三步走：

```bash
# 克隆示例仓库（将<repo> 替换为具体仓库名）
git clone https://github.com/Ai-Thinker-AiPi/<repo>.git
cd <repo>

# 按你的主控选择工具链
# ESP32-S3 : ESP-IDF  或 Arduino IDE
# BL618    : Bouffalo SDK 或 Xuantie-900 工具链
make            # 编译
make flash      # 烧录
make monitor    # 串口监视
```

> 🔌 **不想折腾命令行？** 使用 **ST-LinK343** —— 支持 SWD 调试、6M 波特率高速串口、预留 USB 测试排针、一键上下电快速触发烧录，电源防短路防反插。它能陪你走完整个大学调试生涯。

### 3️⃣ 获取支持 Get Support

- 📖 **文档**：先查[文档中心](https://docs.ai-thinker.com)，常见问题都有沉淀
- 💬 **社区**：[技术社区](https://www.ai-thinker.com/community)提问，附型号 + 接线图 + 复现步骤，回复更快
- 🐛 **Bug 反馈**：各产品仓库提 Issue，请填写系统/模组型号、SDK 版本、复现现象

---

## 开源项目 Featured Repositories

浏览全部仓库：**[github.com/Ai-Thinker-AiPi](https://github.com/Ai-Thinker-AiPi)**

| 仓库类型 Repository | 内容 Content |
| --- | --- |
| **开发板例程**<br>Board Examples | 各系列开发板的示例代码、原理图与 BOM |
| **SDK 与固件**<br>SDK & Firmware | 官方 SDK 移植说明、固件构建脚本 |
| **调试工具**<br>Debug Tools | 烧录器、串口工具的配置与使用 |
| **教程与文档**<br>Tutorials & Docs | 入门教程、踩坑记录、最小可行项目 |

> 📌 本表为分类说明，不是具体仓库链接。发布公开仓库后，请在组织首页右侧 **View as** 菜单中置顶（public 与 member 各最多 6 个，需 owner 权限）。

---

## 为什么选择安信可 Why Ai-Thinker

- 🛡️ **合规可靠** — 模组通过 FCC / CE / SRRC 等认证，直接用于产品化设计
- 🧩 **开发生态完整** — 官方 SDK、例程、原理图、BSP 全部开源
- 🎓 **教学友好** — 开发板资料丰富，社区活跃，高校课程与竞赛常用
- 🔧 **工具齐备** — 从烧录器到串口助手，配套工具一站配齐

---

## 参与贡献 Contributing

我们欢迎所有形式的贡献：

- 📝 **提交 Issue**：反馈 Bug、提出功能建议，请附详细环境信息
- 🔧 **提交 PR**：修复 Bug、完善文档、补充例程，保持与主干一致
- 📖 **改进文档**：错别字、缺失步骤、翻译问题都欢迎指正
- 💡 **分享方案**：把你的项目做成例程，帮助更多开发者

提交前请确认代码风格与目标仓库一致，涉及硬件改动的 PR 请同时更新原理图与 BOM。

---

## 获取帮助 Getting Help

| 渠道 Channel | 适用场景 |
| --- | --- |
| [文档中心 Docs](https://docs.ai-thinker.com) | 产品规格、接线、SDK 用法 |
| [技术社区 Community](https://www.ai-thinker.com/community) | 调试求助、方案讨论 |
| [产品仓库 Issues](https://github.com/Ai-Thinker-AiPi) | Bug 反馈、功能建议 |
| 商务合作 | 定制模组、批量采购，请联系官网客服 |

---

## 许可与版权 License

本仓库内容遵循 [MIT License](LICENSE)。

Content in this repository is licensed under the [MIT License](LICENSE).

---

<div align="center">

**安信可科技 · Ai-Thinker Technology**

Made with ❤️ for makers, students and engineers in China and around the world.

</div>
