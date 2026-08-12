# LADS Story Content

《恋与深空》每日乙女向短篇的**内容同步仓库**。这里不包含 Android App 或其他客户端代码；客户端只读取 `metadata/index.json` 与正文 Markdown。

## 发布步骤

```powershell
python scripts/validate.py
python scripts/build_index.py
```

文章放在 `content/stories/YYYY-MM-DD/`。每日生产规范见 `generator/daily-run.md`。

