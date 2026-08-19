---
language:
- zh
- en
- yue
license: apache-2.0
base_model: Qwen/Qwen3-1.7B
base_model_relation: finetune
library_name: mlx-lm
pipeline_tag: text-generation
tags:
- qwen3
- coder
- lora
- code
- lychee
- finetune
- multilingual
datasets:
- sahil2801/CodeAlpaca-20k
- shibing624/alpaca-zh
- tatsu-lab/alpaca
- hon9kon9ize/yue-alpaca-chat
---

# mlx-LycheeAI-coder-1.7b

**mlx-LycheeAI-coder-1.7b** 是一个基于 [Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B) 通过 **QLoRA（4-bit）微调**而来的编程助手模型，专注于提升编码能力，擅长编写清晰、正确、可维护的代码。

> ⚠️ **格式说明**：本仓库提供的是 **MLX 格式**模型（`mlx` 前缀即表示此含义），仅支持在 **Apple Silicon Mac** 上通过 [MLX-LM](https://github.com/ml-explore/mlx-lm) 加载，**不兼容** HuggingFace transformers（PyTorch）、Windows/Linux、以及 Ollama（GGUF）。如需跨平台（Ollama / llama.cpp / Windows / Linux）版本，请使用 **GGUF 版**：
> - HuggingFace: [whcl412/LycheeAI-coder-1.7b-GGUF](https://huggingface.co/whcl412/LycheeAI-coder-1.7b-GGUF)
> - ModelScope: [whcl412/LycheeAI-coder-1.7b-GGUF](https://modelscope.cn/models/whcl412/LycheeAI-coder-1.7b-GGUF)

## 模型信息

| 项目 | 说明 |
|------|------|
| 基座模型 | Qwen/Qwen3-1.7B |
| 微调方法 | QLoRA（4-bit 量化 + LoRA，rank 16，16 层） |
| 训练框架 | MLX-LM（Apple Silicon） |
| 许可 | Apache 2.0（跟随基座） |
| 模型大小 | ~968MB（4-bit 量化） |

## 训练细节

- **第一轮（代码专项）**：
  - [CodeAlpaca-20k](https://huggingface.co/datasets/sahil2801/CodeAlpaca-20k)（代码指令 3500 条，重点）
  - 中文对话 800 条（[alpaca-zh](https://huggingface.co/datasets/shibing624/alpaca-zh)）
  - 英语对话 800 条（[Alpaca](https://huggingface.co/datasets/tatsu-lab/alpaca) 英文版）
  - 粤语对话 600 条（[yue-alpaca-chat](https://huggingface.co/datasets/hon9kon9ize/yue-alpaca-chat)）
  - 身份问答 24 条（中/英/粤，强化身份记忆）
  - 共 5724 条，学习率 1e-4，batch size 2，4000 步，LoRA rank 16
- **第二轮（日常对话增量微调）**：
  - 60 条日常对话（中文 32 / 英语 16 / 粤语 12），短问短答、口语化，让模型日常聊天时回复简短自然、不啰嗦
  - 从第一轮权重续训（resume），学习率 5e-5，batch size 2，60 步
- **第三轮（多语言项目 + 场景感知 + emoji）**：
  - 150 条数据：多语言小型项目 90 条（Python 20 / C 10 / C++ 10 / C# 10 / HTML 前端 10 / Java 10 / JavaScript 10 / Swift 5 / Go 5）+ 场景感知对话 60 条（简短 40 + 长篇 20，中英粤）
  - 让模型学会「看场景决定说多说少」（日常闲聊简短带 emoji，技术/代码问题详细完整），并能写多种语言的小型项目
  - 从第二轮权重续训（resume），学习率 5e-5，batch size 2，150 步
- **身份设定**：通过 system prompt + 身份问答样本，固定模型身份为「LycheeAI-coder-1.7b，由 Qwen3-1.7B 微调而来」

## 使用方式

### MLX-LM 加载

```python
from mlx_lm import load, generate

model, tokenizer = load("LycheeAI-coder-1.7b")
response = generate(model, tokenizer, prompt="用 Python 写一个快速排序", max_tokens=200)
print(response)
```

### 快速体验

```bash
mlx_lm.generate --model LycheeAI-coder-1.7b --prompt "写一个二分查找" --max-tokens 200
```

## ⚠️ 已知问题

- **对话能力有限**：本模型定位为**代码优先**的编程助手。虽已通过混合数据（中/英/粤语对话）缓解了纯代码微调导致的对话退化，但作为 1.7B 小模型，通用对话的深度与准确性仍不如专门的大规模聊天模型。生成时可能残留空的 `<think>` 标记（Qwen3 思考模式的痕迹），可忽略或由客户端过滤。

## 预期用途与局限

- **适用**：代码生成、代码补全、简单编程问答、代码解释
- **局限**：1.7B 参数规模有限，复杂推理、长上下文、跨领域知识能力有限；微调数据以 Python/TypeScript/Java/Swift/Go/C/C++ 为主

## 致谢

本模型基于 [Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B) 微调，训练框架为 [MLX-LM](https://github.com/ml-explore/mlx-lm)，训练数据来自 CodeAlpaca 及各开源项目。
