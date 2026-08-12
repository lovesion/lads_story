# 每日发布

每天在 `content/stories/YYYY-MM-DD/男主名/文章标题.md` 创作 40 篇《恋与深空》乙女向中文独立短篇。男主目录只能是 `秦彻` 或 `夏以昼`，文件名必须与 Front Matter 的 `title` 完全一致。每篇标题必须独立、有场景感，不得使用“第几夜”“第几篇”等编号，也不重复附加男主姓名。每篇正文（不含 Front Matter）必须是 **2,000–4,000 个非空白中文字符**，并将精确数值写入 `word_count`；秦彻随机 15–25 篇，夏以昼补足；先运行 `python generator/topic_scheduler.py`，将输出仅用作避重参考。

正文不能由脚本、固定句库或统一情节模板批量拼装。逐篇先执行 `generator/editorial-run.md`：各自确定前提、角色动机、冲突、情绪路径与世界观锚点，并在写后独立进行 OOC 与世界观审校。原作细节不确定时不得编造；使用克制的通用场景或清晰 AU。写作采用适合 LOFTER 阅读的节奏，但不复制或仿写任何特定作者。AI 辅助文本若发布到 LOFTER，应按平台功能与适用规定做透明声明，例如标注 `#AI辅助#`。

必须运行 `python scripts/validate.py`、`python scripts/build_index.py`、再次校验。只有全部通过才提交并推送；内容须遵守适用平台、版权方和法律规则。
