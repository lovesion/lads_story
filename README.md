# LADS Story Content

《恋与深空》每日乙女向 2,000–4,000 字短篇的**内容同步仓库**。这里不包含 Android App 或其他客户端代码；客户端只读取 `metadata/index.json` 与正文 Markdown。

## 发布步骤

```powershell
python scripts/validate.py
python scripts/build_index.py
```

文章放在 `content/stories/YYYY-MM-DD/`。每日生产规范见 `generator/daily-run.md`。
文章采用三级目录：`content/stories/日期/男主名/文章标题.md`，例如 `content/stories/2026-08-13/秦彻/雨声停在门外·第1夜（秦彻）.md`。

