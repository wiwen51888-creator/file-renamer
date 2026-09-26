# file-renamer

文件批量重命名工具。支持按序号、日期、正则替换、大小写转换批量改名。

## 安装

无需第三方依赖，Python 3.8+ 即可。

## 用法

```bash
# 按序号重命名（预览，不实际改名）
python renamer.py ./photos --mode seq --dry-run

# 按序号重命名，前缀 vacation
python renamer.py ./photos --mode seq --prefix vacation

# 按修改日期重命名
python renamer.py ./photos --mode date

# 正则替换
python renamer.py ./photos --mode regex --pattern "IMG_(\d+)" --replace "photo_\1"

# 小写化
python renamer.py ./photos --mode lower
```

## 参数

- `--mode`：seq / date / regex / lower / upper
- `--dry-run`：只预览，不实际修改
- `--prefix`：序号模式的前缀
- `--start`：序号起始值（默认 1）
- `--pattern` / `--replace`：正则模式使用
- `--ext`：只处理指定扩展名（如 jpg,png）

## 说明

默认只处理当前目录的文件，不递归。使用 `--dry-run` 先预览，确认无误再去掉。