#!/usr/bin/env python3
"""
修复中文引号问题
将直引号 (") 替换为弯引号 ("" 或 "")
"""

import os
import re
import sys

def fix_chinese_quotes(content):
    """
    修复中文引号
    规则：
    1. 中文语境下的引号使用弯引号 ""
    2. 英文语境下保持直引号 "
    """
    result = []
    i = 0
    in_quote = False
    
    while i < len(content):
        char = content[i]
        
        if char == '"':
            # 检查是否在中文语境中
            # 如果前后有中文字符，则认为是中文引号
            prev_char = content[i-1] if i > 0 else ''
            next_char = content[i+1] if i < len(content) - 1 else ''
            
            has_chinese_context = (
                re.match(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', prev_char) or
                re.match(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', next_char)
            )
            
            if has_chinese_context:
                if not in_quote:
                    # 开始引号
                    result.append('\u201c')  # "
                    in_quote = True
                else:
                    # 结束引号
                    result.append('\u201d')  # "
                    in_quote = False
            else:
                # 英文语境，保持直引号
                result.append(char)
        else:
            result.append(char)
        
        i += 1
    
    return ''.join(result)

def process_file(filepath):
    """处理单个文件"""
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
    """主函数"""
    if len(sys.argv) > 1:
        # 处理指定文件
        files = sys.argv[1:]
    else:
        # 处理所有 markdown 文件
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
