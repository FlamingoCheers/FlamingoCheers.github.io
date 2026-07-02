#!/usr/bin/env python3
"""
修复中文引号问题
将直引号 (") 替换为弯引号 (\u201c\u201d)
规则：中文语境下使用弯引号，英文语境下保持直引号
"""

import os
import re
import sys


def fix_chinese_quotes(content):
    result = []
    in_quote = False

    for i, char in enumerate(content):
        if char == '"':
            prev_char = content[i - 1] if i > 0 else ''
            next_char = content[i + 1] if i < len(content) - 1 else ''

            has_chinese_context = (
                re.match(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', prev_char)
                or re.match(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', next_char)
            )

            if has_chinese_context:
                if not in_quote:
                    result.append('\u201c')
                    in_quote = True
                else:
                    result.append('\u201d')
                    in_quote = False
            else:
                result.append(char)
        else:
            result.append(char)

    return ''.join(result)


def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = fix_chinese_quotes(content)

        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"已修复: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"处理 {filepath} 时出错: {e}")
        return False


def main():
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        blog_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        content_dir = os.path.join(blog_dir, 'content', 'posts')

        if not os.path.exists(content_dir):
            print(f"目录不存在: {content_dir}")
            sys.exit(1)

        files = []
        for root, dirs, filenames in os.walk(content_dir):
            for filename in filenames:
                if filename.endswith('.md'):
                    files.append(os.path.join(root, filename))

    fixed_count = 0
    for filepath in files:
        if process_file(filepath):
            fixed_count += 1

    print(f"\n共修复 {fixed_count} 个文件")


if __name__ == '__main__':
    main()
