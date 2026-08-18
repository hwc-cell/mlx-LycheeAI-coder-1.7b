#!/usr/bin/env bash
# LycheeAI-coder-1.7b 微调脚本
# 1) 官方 FP16 模型转 4bit MLX 格式
# 2) LoRA 微调（4bit QLoRA，半小时内）
set -e
VENV=/Users/hwc/.workbuddy/binaries/python/envs/mlx
export HF_ENDPOINT=https://hf-mirror.com
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY all_proxy

SRC=/Users/hwc/.cache/hf/Qwen3-1.7B
MLX4=/Users/hwc/LycheeAI/Qwen3-1.7B-4bit-mlx
DATA=/Users/hwc/LycheeAI
ADAPTER=/Users/hwc/LycheeAI/adapters

echo "=== 1) 转 4bit MLX 格式 ==="
if [ ! -d "$MLX4" ]; then
  "$VENV/bin/mlx_lm.convert" --hf-path "$SRC" -q --q-bits 4 --mlx-path "$MLX4"
else
  echo "已存在 $MLX4，跳过转换"
fi

echo "=== 2) LoRA 微调（batch 2, 1500 iters）==="
"$VENV/bin/mlx_lm.lora" \
  --model "$MLX4" \
  --train \
  --data "$DATA" \
  --fine-tune-type lora \
  --num-layers 16 \
  --batch-size 2 \
  --iters 1500 \
  --learning-rate 2e-4 \
  --adapter-path "$ADAPTER" \
  --grad-checkpoint \
  --save-every 500

echo "=== 完成 ==="
ls -la "$ADAPTER" 2>/dev/null
