#!/usr/bin/env python3
"""精选纯代码仓库 → 提取源码片段成 MLX-LM text 训练格式（不删文件，绕代理）。"""
import subprocess, os, json

REPOS = {
    "python": ["psf/requests", "tiangolo/fastapi"],
    "typescript": ["colinhacks/zod"],
    "javascript": ["expressjs/express"],
    "java": ["google/guava"],
    "swift": ["Alamofire/Alamofire"],
    "go": ["gin-gonic/gin"],
    "c": ["redis/redis"],
    "c++": ["nlohmann/json", "fmtlib/fmt"],
}

EXT = {
    "python": {".py"}, "typescript": {".ts", ".tsx"}, "javascript": {".js"},
    "java": {".java"}, "swift": {".swift"}, "go": {".go"},
    "c": {".c", ".h"}, "c++": {".cpp", ".cc", ".cxx", ".hpp", ".h"},
}

TMP = "/tmp/code_repos"
OUT = "/Users/hwc/Desktop/lycheeAI-coder-1.7b-xunlian/code_corpus.jsonl"
os.makedirs(TMP, exist_ok=True)

# 绕过本地坏代理
env = os.environ.copy()
for k in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
    env.pop(k, None)

EXCLUDE_DIRS = {"test", "tests", "node_modules", "dist", "build", "vendor",
                ".git", "__pycache__", "example", "examples", "docs", "docs_src",
                ".venv", "venv", "benchmarks", "benchmark", "deps", "dependencies"}
MAX_FILE_SIZE = 500 * 1024
CHUNK = 1500        # 每段约 1500 字符
MAX_FILES_PER_REPO = 80  # 每仓库最多取 80 个文件，控制总量

out_lines = []
for lang, repos in REPOS.items():
    print(f"=== {lang} ===")
    for repo in repos:
        dirpath = os.path.join(TMP, repo.replace("/", "__"))
        if not os.path.isdir(dirpath):
            r = subprocess.run(["git", "clone", "--depth", "1", "-q",
                                f"https://github.com/{repo}.git", dirpath],
                               env=env, timeout=180)
            if r.returncode != 0:
                print(f"  {repo} clone 失败")
                continue
        cnt = 0
        for root, dirs, files in os.walk(dirpath):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                if cnt >= MAX_FILES_PER_REPO:
                    break
                ext = os.path.splitext(f)[1].lower()
                if ext not in EXT[lang]:
                    continue
                fp = os.path.join(root, f)
                if os.path.getsize(fp) > MAX_FILE_SIZE:
                    continue
                try:
                    code = open(fp, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                for i in range(0, len(code), CHUNK):
                    seg = code[i:i + CHUNK].strip()
                    if len(seg) > 50:
                        out_lines.append(json.dumps({"text": seg}, ensure_ascii=False))
                cnt += 1
        print(f"  {repo}: 取 {cnt} 个文件")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))
print(f"\n总片段数: {len(out_lines)}")
print(f"写入: {OUT} ({os.path.getsize(OUT)/1024/1024:.1f} MB)")
