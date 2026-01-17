import os
import json

# 配置路径
icon_dir = 'smartisan-icon/icon'
output_file = 'smartisan-icon/data.js'

def update_data():
    if not os.path.exists(icon_dir):
        print(f"Error: Directory '{icon_dir}' not found.")
        # Fallback check if running from inside smartisan-icon
        if os.path.exists('icon') and os.path.exists('data.js'):
             print("Seems we are inside smartisan-icon, using local paths.")
             icon_dir_local = 'icon'
             output_file_local = 'data.js'
             # ... (logic to run with local paths)
             # But let's stick to absolute-ish paths from root
             return

    # 获取所有 png 文件
    try:
        icons = [f for f in os.listdir(icon_dir) if f.endswith('.png') and not f.startswith('.')]
        icons.sort()
        
        # 生成 JS 内容
        js_content = f"window.icons = {json.dumps(icons, indent=4)};"

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(js_content)

        print(f"Successfully updated {output_file}")
        print(f"Total icons found: {len(icons)}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    update_data()
