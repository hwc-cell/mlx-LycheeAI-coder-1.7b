---
language:
- zh
- en
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
datasets:
- sahil2801/CodeAlpaca-20k
- github-code-corpus
---

# mlx-LycheeAI-coder-1.7b

**mlx-LycheeAI-coder-1.7b** 是一个基于 [Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B) 通过 **QLoRA（4-bit）微调**而来的编程助手模型，专注于提升编码能力，擅长编写清晰、正确、可维护的代码。

> ⚠️ **格式说明**：本仓库提供的是 **MLX 格式**模型（`mlx` 前缀即表示此含义），仅支持在 **Apple Silicon Mac** 上通过 [MLX-LM](https://github.com/ml-explore/mlx-lm) 加载，**不兼容** HuggingFace transformers（PyTorch）、Windows/Linux、以及 Ollama（GGUF）。如需跨平台版本，请关注后续的 GGUF 版本。

## 模型信息

| 项目 | 说明 |
|------|------|
| 基座模型 | Qwen/Qwen3-1.7B |
| 微调方法 | QLoRA（4-bit 量化 + LoRA，rank 16，16 层） |
| 训练框架 | MLX-LM（Apple Silicon） |
| 许可 | Apache 2.0（跟随基座） |
| 模型大小 | ~968MB（4-bit 量化） |

## 训练细节

- **训练数据**：
  - [CodeAlpaca-20k](https://huggingface.co/datasets/sahil2801/CodeAlpaca-20k)（代码指令，取 2000 条）
  - 精选 GitHub 高质量开源仓库源码（requests、fastapi、zod、express、guava、Alamofire、gin、redis、nlohmann/json、fmt 等，取 1000 片段）
- **超参数**：学习率 2e-4，batch size 2，1500 步，LoRA rank 16
- **身份设定**：训练时通过 system prompt 固定模型身份为"由 Qwen3-1.7B 微调而来"

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

- **通用对话体验不佳**：本模型使用纯代码指令数据微调，通用闲聊（问候、天气、日常问答等）能力有所退化，可能出现答非所问、回复英文或复读训练数据片段的情况。**建议仅用于代码相关任务**（代码生成、补全、解释、改 bug），日常对话请使用通用聊天模型。

## 预期用途与局限

- **适用**：代码生成、代码补全、简单编程问答、代码解释
- **局限**：1.7B 参数规模有限，复杂推理、长上下文、跨领域知识能力有限；微调数据以 Python/TypeScript/Java/Swift/Go/C/C++ 为主

## 致谢

本模型基于 [Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B) 微调，训练框架为 [MLX-LM](https://github.com/ml-explore/mlx-lm)，训练数据来自 CodeAlpaca 及各开源项目。
