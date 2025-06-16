#!/bin/bash
INPUT_SOURCE="$1"
PATTERN="00000000000f\|panic\|coredump"

# 验证输入源权限
if [[ ! -r "$INPUT_SOURCE" ]]; then
    echo "错误：无法读取输入源 $INPUT_SOURCE" >&2
    exit 1
fi

# 实时监控逻辑
case "$INPUT_SOURCE" in
    /dev/tty*)  # 终端设备特殊处理
        exec stdbuf -oL cat "$INPUT_SOURCE" | grep -i --line-buffered "$PATTERN"
        ;;
    *)
        tail -F "$INPUT_SOURCE" | grep -i --line-buffered "$PATTERN"
        ;;
esac