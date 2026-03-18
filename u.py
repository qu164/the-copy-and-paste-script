# -*- coding: utf-8 -*-
import pandas as pd

# --- 配置区 ---
excel_input = "table.xlsx"      
txt_input = "thinking.txt"      
output_file = "table_filled.csv"   

start_row = 1                   # 这个参数现在可以删掉不用了
end_row = 50                    

def batch_fill():
    try:
        # 1. 读取思维链
        with open(txt_input, 'r', encoding='utf-8') as f:
            thinking_lines = [line.strip() for line in f if line.strip()]
        
        print(f"成功读取到 {len(thinking_lines)} 条思维链。")

        # 2. 读取Excel —— 关键修复：header=None
        df = pd.read_excel(excel_input, sheet_name="Sheet1", engine="openpyxl", header=None)
        df.iloc[:, 0] = df.iloc[:, 0].astype(str)

        print(f"Excel 共读取到 {len(df)} 行数据（已强制把第一行当作数据）")

        # 3. 严格一一对应插入（从第0行开始）
        success_count = 0
        for i, text in enumerate(thinking_lines):
            current_idx = i                     # ← 严格从第一行开始
            
            if current_idx >= len(df) or current_idx >= end_row:
                break
            
            try:
                original = df.iloc[current_idx, 0]
                
                # 字符串替换插入 Thinking
                if '"Thinking": ""' in original:
                    new_str = original.replace('"Thinking": ""', f'"Thinking": "{text}"')
                elif '"Thinking":""' in original:
                    new_str = original.replace('"Thinking":""', f'"Thinking": "{text}"')
                else:
                    if original.endswith('}'):
                        new_str = original[:-1] + f', "Thinking": "{text}"' + '}'
                    else:
                        new_str = original
                
                df.iloc[current_idx, 0] = new_str
                success_count += 1
                
            except Exception as e:
                print(f"第 {current_idx + 1} 行插入失败: {e}")

        # 4. 保存
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"处理完成！成功填充 {success_count} 条思维链")
        print(f"结果已保存至: {output_file}")

    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == "__main__":
    batch_fill()