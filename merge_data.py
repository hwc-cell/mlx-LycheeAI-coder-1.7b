#!/usr/bin/env python3
"""合并指令数据 + 代码语料，统一成 chat 格式（MLX-LM 训练要求）。"""
import json, random, os

D = "/Users/hwc/Desktop/lycheeAI-coder-1.7b-xunlian"
instr_path = os.path.join(D, "train.jsonl")
code_path = os.path.join(D, "code_corpus.jsonl")
out_path = os.path.join(D, "train_merged.jsonl")

SYS = ("你是 LycheeAI-coder-1.7b，一个由 Qwen3-1.7B 通过 LoRA 微调而来的编程助手，"
       "擅长编写清晰、正确、可维护的代码，并给出必要的解释。")
USER_CODE = "请编写以下代码，确保正确、清晰、可维护。"

random.seed(42)

# 1) 指令数据（原本就是 chat 格式）
instr = [l.strip() for l in open(instr_path, encoding="utf-8") if l.strip()]
print(f"指令数据: {len(instr)} 条")

# 2) 代码语料 text → chat 格式
code = [l.strip() for l in open(code_path, encoding="utf-8") if l.strip()]
random.shuffle(code)
code = code[:1000]
code_chat = []
for l in code:
    d = json.loads(l)
    code_chat.append(json.dumps({
        "messages": [
            {"role": "system", "content": SYS},
            {"role": "user", "content": USER_CODE},
            {"role": "assistant", "content": d["text"]},
        ]
    }, ensure_ascii=False))
print(f"代码语料: 抽样 {len(code_chat)} 片段（转 chat）")

merged = instr + code_chat
random.shuffle(merged)

with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(merged))
print(f"\n合并完成: {len(merged)} 条，全 chat 格式")
print(f"写入: {out_path} ({os.path.getsize(out_path)/1024/1024:.1f} MB)")

bad = sum(1 for l in merged if "messages" not in l)
print(f"非 chat 行: {bad}")
