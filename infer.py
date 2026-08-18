#!/usr/bin/env python3
"""LycheeAI-coder-1.7b 推理示例：加载模型并生成代码。"""
from mlx_lm import load, generate

MODEL = "LycheeAI-coder-1.7b"

SYS = ("你是 LycheeAI-coder-1.7b，一个由 Qwen3-1.7B 通过 LoRA 微调而来的编程助手，"
       "擅长编写清晰、正确、可维护的代码，并给出必要的解释。")


def main():
    model, tokenizer = load(MODEL)
    print("模型加载完成，输入问题（输入 quit 退出）：")
    while True:
        user = input("\n>>> ").strip()
        if user.lower() in {"quit", "exit", "q"}:
            break
        msgs = [
            {"role": "system", "content": SYS},
            {"role": "user", "content": user},
        ]
        prompt = tokenizer.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False)
        out = generate(model, tokenizer, prompt=prompt, max_tokens=512)
        print(out)


if __name__ == "__main__":
    main()
