### 常用命令

| 命令 | 实际执行 | 用途与限制 |
| --- | --- | --- |
| `npm ci` | 按 `package-lock.json` 安装依赖 | 严格按锁文件安装，会删除已有 `node_modules`；不会修改锁文件。 |
| `npm run dev` | `vite` | 启动 Vite 开发服务（端口见下文）。仅用于本地开发，后端 API 需另行在本地启动。 |
| `npm run typecheck` | `vue-tsc -b` | 按 `tsconfig.json` 的项目引用做 TypeScript / Vue 类型检查。 |
| `npm test` | `vitest run`（先执行 `pretest`） | 单次运行 Vitest 测试，不进入 watch 模式。`pretest` 说明见下文。 |
| `npm run build` | `vue-tsc -b && vite-ssg build && node scripts/finalize-seo-build.mjs && node scripts/build-home-renderer.mjs` | 完整构建：类型检查 → SSG 预渲染构建到 `dist/` → 生成 `dist/spa.html`、`dist/404.html`、`sitemap.xml`、`robots.txt` 等 SEO 产物 → 构建边缘首页渲染器到 `.edge/`。 |
| `npm run build:spa` | `vue-tsc -b && vite build` | 纯前端 SPA 构建：类型检查后用 Vite 构建，不做 SSG 预渲染、SEO 收尾和边缘渲染器构建，产物与完整构建不同。 |
| `npm run preview` | `vite preview` | 在本地静态预览已构建的 `dist/` 产物，需先执行构建；仅用于本地查看。 |

