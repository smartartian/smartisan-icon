# Smartisan Icons (Vue 3 重构版)

本项目是 Smartisan Icons 的 Vue 3 重构版本，旨在提供更现代化的开发体验和更高效的图标浏览功能。

## ✨ 特性

- **Vue 3 + Vite**: 采用最新的前端技术栈，开发响应迅速，构建高效。
- **响应式设计**: 适配不同屏幕尺寸，提供流畅的浏览体验。
- **实时搜索**: 支持通过图标名称或文件名快速筛选图标。
- **分页加载**: 优化大量图标展示时的性能，支持分页浏览。
- **一键复制**: 支持复制图标路径、名称以及 Base64 编码。
- **加载优化**: 实现了页面加载遮罩和图片骨架屏效果，提升用户体验。

## 🛠️ 技术栈

- [Vue 3](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Vite](https://vitejs.dev/) - 下一代前端构建工具
- [Python](https://www.python.org/) - 用于生成图标数据索引脚本 (`update_icon_data.py`)

## 📂 目录结构

```
.
├── public/              # 静态资源目录
│   ├── icon/            # 存放所有图标文件
│   ├── app_icon_map.json # 图标名称映射文件
│   └── data.js          # 图标索引数据（由脚本生成）
├── src/                 # 源代码目录
│   ├── App.vue          # 主组件
│   ├── main.js          # 入口文件
│   └── style.css        # 全局样式
├── index.html           # 入口 HTML
├── vite.config.js       # Vite 配置文件
├── update_icon_data.py  # 图标数据更新脚本
└── package.json         # 项目依赖配置
```

## 🚀 快速开始

### 前置要求

- Node.js (建议 v16+)
- Python 3 (用于运行数据更新脚本)

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

浏览器访问 `http://localhost:5173` 即可预览。

### 更新图标数据

如果你添加或删除了 `public/icon/` 目录下的图标，请运行以下命令更新索引：

```bash
python3 update_icon_data.py
```

### 构建生产版本

```bash
npm run build
```

构建产物将输出到 `dist` 目录。

## 📄 许可证

[ISC](LICENSE)
