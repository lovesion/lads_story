# 每日发布

每天在 `content/stories/YYYY-MM-DD/男主名/文章标题.md` 生成 40 篇《恋与深空》乙女向中文短篇。男主目录只能是 `秦彻` 或 `夏以昼`，文件名必须与 Front Matter 的 `title` 完全一致。每篇正文（不含 Front Matter）必须是 **2,000–4,000 个非空白中文字符**，并将精确数值写入 `word_count`；秦彻随机 15–25 篇，夏以昼补足；先运行 `python generator/topic_scheduler.py`，再按返回的种子写作。

必须运行 `python scripts/validate.py`、`python scripts/build_index.py`、再次校验。只有全部通过才提交并推送；内容须遵守适用平台、版权方和法律规则。
