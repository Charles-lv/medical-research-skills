#!/usr/bin/env bash
# lite_update_report.sh — 上游同步后，判断 lite 分支需要吸收哪些更新
# 用法: bash lite_update_report.sh <OLD_REF> <NEW_REF> [keep.txt]
#   OLD_REF = 上次构建 lite 时 main 的提交（建议打 tag: lite-base-YYYYMMDD）
#   NEW_REF = Sync fork 之后的 main（通常就写 main 或 origin/main）
# 输出三段: [1] 保留 skill 的变更  [2] 上游新增 skill（候选）  [3] 保留 skill 在上游被删/改名
# 只读: 不改任何文件、不推送。
# [✓沙箱实跑] 2026-09-19，合成仓库（二级目录带空格、同名 skill、删除、新增 四种情形）
set -euo pipefail
OLD="${1:?需要 OLD_REF}"; NEW="${2:?需要 NEW_REF}"; KEEP="${3:-keep.txt}"
git rev-parse --verify -q "$OLD^{commit}" >/dev/null || { echo "[FAIL] 找不到 $OLD"; exit 1; }
git rev-parse --verify -q "$NEW^{commit}" >/dev/null || { echo "[FAIL] 找不到 $NEW"; exit 1; }
mapfile -t NAMES < <(sed 's/\r$//' "$KEEP" | grep -v '^[[:space:]]*#' | grep -v '^[[:space:]]*$')
echo "[info] 区间: $(git rev-parse --short "$OLD") .. $(git rev-parse --short "$NEW")  | 上游新提交数: $(git rev-list --count "$OLD..$NEW")"
echo "[info] keep 条目数: ${#NAMES[@]}"

skill_dir() { # $1=ref $2=name → 打印所有匹配目录(可能多个)
  git ls-tree -r --name-only "$1" | grep -E "(^|/)$2/SKILL\.md$" | sed 's#/SKILL\.md$##' || true
}

echo; echo "===== [1] 保留 skill 的变更 ====="
n_chg=0; n_same=0; n_gone=0; n_amb=0; GONE=()
for s in "${NAMES[@]}"; do
  mapfile -t D < <(skill_dir "$NEW" "$s")
  if [ "${#D[@]}" -eq 0 ]; then GONE+=("$s"); n_gone=$((n_gone+1)); continue; fi
  [ "${#D[@]}" -gt 1 ] && { echo "[warn] $s 在 NEW 中有 ${#D[@]} 处同名，逐一列出"; n_amb=$((n_amb+1)); }
  any=0
  for d in "${D[@]}"; do
    out=$(git diff --name-status "$OLD" "$NEW" -- "$d/")
    if [ -n "$out" ]; then
      any=1
      add=$(git diff --numstat "$OLD" "$NEW" -- "$d/" | awk '{a+=$1;r+=$2} END{printf "+%d/-%d 行", a, r}')
      echo "--- $s  [$d]  $add"
      echo "$out" | sed 's/^/      /'
    fi
  done
  [ "$any" -eq 1 ] && n_chg=$((n_chg+1)) || n_same=$((n_same+1))
done
echo "[info] 有变更: $n_chg | 无变更: $n_same | 同名多处: $n_amb | NEW 中找不到: $n_gone"

echo; echo "===== [2] 上游新增 skill（候选，需人工判断是否加入 keep） ====="
n_new=0
while IFS=$'\t' read -r st path; do
  [ -z "${path:-}" ] && continue
  d=${path%/SKILL.md}; name=${d##*/}
  desc=$(git show "$NEW:$path" | awk 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f&&/^description:/{sub(/^description:[ ]*/,"");print;exit}')
  size=$(git ls-tree -r -l "$NEW" -- "$d/" | awk '{s+=$4} END{printf "%.1f", s/1024}')
  printf '%-45s %6s KB  [%s]\n      %s\n' "$name" "$size" "$d" "${desc:0:160}"
  n_new=$((n_new+1))
done < <(git diff --name-status --diff-filter=A "$OLD" "$NEW" | grep -E '/SKILL\.md$' || true)
echo "[info] 新增 skill 数: $n_new"

echo; echo "===== [3] 保留 skill 在上游被删除或改名 ====="
for s in "${GONE[@]+"${GONE[@]}"}"; do
  mapfile -t OD < <(skill_dir "$OLD" "$s")
  ren=$(git diff --name-status -M "$OLD" "$NEW" | awk -F'\t' -v p="/$s/SKILL.md" '$1 ~ /^R/ && index($2,p) {print $3}')
  if [ -n "$ren" ]; then fate="改名为 ${ren%/SKILL.md}"; else fate="已删除"; fi
  echo "--- $s  旧位置: ${OD[*]:-无}  →  $fate"
done
[ "$n_gone" -eq 0 ] && echo "(无)"
exit 0
