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

> **当前版本：V13**（开关思考版）

**mlx-LycheeAI-coder-1.7b** 是一个基于 [Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B) 通过 **QLoRA（4-bit）微调**而来的编程助手模型。V13 版本经过十三轮增量微调，在代码能力（9 种语言）与多语言对话（中/英/粤）、情感共情、场景感知回答之间取得均衡，并实现了**可开关的思考能力**（难题自动思考、`/no_think` 直接作答、按难度调整思考深度）。

> 🙏 **关于本项目**：这是一个**个人开发者初次尝试**的开源项目，模型由 1.7B 小参数基座微调而来，能力有限——复杂代码、多步推理可能出错，思考输出偶有格式瑕疵。它更适合作为**轻量本地助手**（简单代码、日常聊天、离线使用），不适合作为生产级编程工具。如果你需要一个「能打」的模型，建议使用更大的开源模型或商业 API。

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
- **第四轮（情感共情 + 格式感知 + 多轮 + 复合逻辑）**：
  - 120 条：情感共情 40 + 格式感知 21（区分「解释概念用纯文字」vs「写代码用代码块」）+ 多轮对话 10 + 复合逻辑对比 11 + 纯代码 18 + 锚点 20
  - 修复评测反馈的四个短板（复合逻辑出错、闲聊乱用代码块、缺情感共情、缺多轮语义追踪）
  - 从第三轮权重续训，学习率 5e-5，batch size 2，120 步
- **第五轮（代码正确性 + 分场合安慰）**：
  - v6.1：133 条（正确代码 79 条覆盖 9 语言 + bug 修复 20 + 全面发展 34），提升代码正确性、减少 bug
  - v6.2：26 条（该安慰 8 + 不该安慰 12 + 锚点 6），学会分场合安慰（明确负面情绪才安慰，中性日常简短回应）
  - 从第四轮权重续训，学习率 5e-5
- **第六轮（可开关思考）**：
  - 159 条：思考模式 80（数学/逻辑/代码调试/多步推理，assistant 输出 `<think>推理</think>` + 答案）+ 直答模式 49（`/no_think` 开头直接答）+ 锚点 30
  - 让模型学会「可开关思考」：正常问会先思考再答，加 `/no_think` 直接答
  - 从第五轮权重续训，学习率 5e-5，160 步
- **第七轮（纠偏身份过拟合 + 按难度调整思考 + 网络用语上下文）**：
  - 100 条：常识纠偏+网络用语 25（ChatGPT=OpenAI、xswl=笑死我了 等）+ 身份 vs 常识区分 10 + 诚实兜底 6 + 按难度调整思考 30 + 网络用语上下文 10 + 锚点 15
  - 修复「被问 XX 是什么就套身份模板」的过拟合问题，学会区分「我是谁」和「别人是谁」，并诚实说「不知道」
  - 从第六轮权重续训，学习率 5e-5，100 步
- **第八轮（拉回代码能力）**：
  - 86 条：完整代码项目 39（含 HTML 计算器完整版）+ 代码调试 15 + 难题思考 10 + 常识纠偏保留 10 + 锚点 15
  - 修复第七轮纠偏数据（短文本过多）导致的代码能力退化
  - 从第七轮权重续训，学习率 5e-5，90 步
- **第九轮（最终均衡版，V10）**：
  - 200 条：代码 75（完整项目 45 + 调试 20 + 概念 10）+ 情感分场合 25 + 日常简短 20 + 常识百科 20 + 难题思考 15 + 多语言 15 + 网络用语 10 + 身份 10 + 诚实兜底 10
  - 整合前八轮所有能力，做最终均衡，目标最大化 1.7B 潜力
  - 从第八轮权重续训，学习率 5e-5，200 步
- **第十轮（均衡版加强思考，V11）**：
  - 250 条：完整代码项目 50 + 代码调试 15（带思考）+ 难题思考 35（数学 20 + 逻辑 15）+ 简单题直答 25 + 情感 25 + 日常 25 + 多语言 20 + 常识 20 + 身份 15 + 网络 10 + 诚实 10
  - 从 v10 续训，学习率 5e-5，250 步
- **第十一轮（思考修复版，V12）**：
  - 150 条：真实分步推理思考题 60（数学 15 + 逻辑 15 + 代码推理 15 + 常识推理 10 + 开关演示 5）+ 锚点 90（代码 30 + 多语言 15 + 常识 12 + 日常 12 + 情感 10 + 身份 6 + 网络 3 + 诚实 2）
  - 把思考样本占比从 V11 的 20% 提到 36.7%，修复 GGUF 版思考退化（空 `<think>` 壳）问题
  - 从 v11 续训，学习率 5e-5，150 步
- **第十二轮（开关思考版，V13）**：
  - 300 条 = 打开思考 200（数学 40 + 逻辑 30 + 代码推理 30 + 常识 20 + 日常 30 + 情感 20 + 多语言 20 + 身份诚实 10，全部带 `<think>`，按难度调深度）+ 关闭思考 100（数学 20 + 代码 20 + 日常 15 + 逻辑 10 + 情感 10 + 多语言 10 + 常识 10 + 身份 5，全部 `/no_think` 直答）
  - 实现 A+B 思考开关：`/no_think` 显式关闭 + 按难度自动调强度；统一思考链模板「先拆 → 再推 → 给结论」；写代码先讲思路
  - 从 v12 续训，学习率 5e-5，300 步
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

## 预期用途与局限

- **适用**：代码生成（9 种语言）、代码调试/修复、编程问答、日常多语言对话（中/英/粤）、情感交流、常识问答、可开关思考（难题会先思考再答）
- **开关思考**：正常提问会输出 `<think>` 推理过程再给答案；在提问前加 `/no_think` 可跳过思考直接回答
- **局限**：1.7B 参数规模有限，复杂推理、长上下文、冷门知识能力有限；深度思考能力受限于模型容量；GGUF 量化版（Ollama / llama.cpp）在长链多步推理上的准确性会略低于 MLX 版（量化损失）。

## 关注作者

📺 **Bilibili**：欢迎关注我的 B 站账号 [https://space.bilibili.com/3493128967293256](https://space.bilibili.com/3493128967293256)，不定期分享 AI 模型训练与折腾记录。

## 致谢

本模型基于 [Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B) 微调，训练框架为 [MLX-LM](https://github.com/ml-explore/mlx-lm)，训练数据来自 CodeAlpaca 及各开源项目。
