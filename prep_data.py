#!/usr/bin/env python3
"""下载 CodeAlpaca 代码指令数据，转成 MLX-LM chat 格式 JSONL。
身份 system prompt 保留"由 Qwen3-1.7B 微调而来"。
"""
import json, os
from datasets import load_dataset

OUT_DIR = "/Users/hwc/LycheeAI"
os.makedirs(OUT_DIR, exist_ok=True)

SYS = (
    "你是 LycheeAI-coder-1.7b，一个由 Qwen3-1.7B 通过 LoRA 微调而来的编程助手，"
    "擅长编写清晰、正确、可维护的代码，并给出必要的解释。"
)

print("下载 CodeAlpaca-20k ...")
ds = load_dataset("sahil2801/CodeAlpaca-20k", split="train")
print(f"原始条数: {len(ds)}")

# 取前 N 条，过滤空输出，控制训练时间
N = 2000
ds = ds.select(range(min(N, len(ds))))

lines = []
skipped = 0
for ex in ds:
    instr = (ex.get("instruction") or "").strip()
    inp = (ex.get("input") or "").strip()
    out = (ex.get("output") or "").strip()
    if not instr or not out:
        skipped += 1
        continue
    user = instr + (f"\n{inp}" if inp else "")
    lines.append(json.dumps({
        "messages": [
            {"role": "system", "content": SYS},
            {"role": "user", "content": user},
            {"role": "assistant", "content": out},
        ]
    }, ensure_ascii=False))

out_path = os.path.join(OUT_DIR, "train.jsonl")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"有效条数: {len(lines)}，跳过空输出 {skipped} 条")
print(f"已写入: {out_path}")
print(f"文件大小: {os.path.getsize(out_path)/1024:.1f} KB")
