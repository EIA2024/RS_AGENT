import os
import argparse
from agent import process_user_query

def process_query(query: str, output_dir: str = "output") -> None:
    """处理单个查询"""
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "query_result.txt")
    
    print(f"\n[系统] 正在处理查询: {query}")
    
    # 运行代理
    result = process_user_query(
        prompt=query,
        output_path=output_file
    )
    
    # 处理结果
    if result == 0:
        print("\n[成功] 查询处理完成！")
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                print("\n--- 查询结果 ---")
                print(f.read())
                print("--- 结果结束 ---")
        except FileNotFoundError:
            print(f"[错误] 未找到输出文件: {output_file}")
    elif result == -2:
        print("\n[成功] 模糊查询已通过交互式澄清完成！")
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                print("\n--- 查询结果 ---")
                print(f.read())
                print("--- 结果结束 ---")
        except FileNotFoundError:
            print(f"[错误] 未找到输出文件: {output_file}")
    elif result == -1:
        print("\n[失败] 查询与系统功能无关，无法处理。")
    else:
        print(f"\n[失败] 查询处理失败，错误代码: {result}")

def main():
    """主函数：处理用户查询"""
    parser = argparse.ArgumentParser(description='RS Agent - 遥感知识问答系统')
    parser.add_argument('--query', type=str, help='要查询的问题')
    parser.add_argument('--output-dir', type=str, default='output', help='输出目录路径')
    
    args = parser.parse_args()
    
    print("="*50)
    print("RS Agent - 遥感知识问答系统")
    print("="*50)
    
    if args.query:
        # 如果提供了命令行参数，直接处理查询
        process_query(args.query, args.output_dir)
    else:
        # 交互模式
        while True:
            query = input("\n请输入您的问题（输入'退出'结束）: ").strip()
            if query.lower() in ['退出', 'exit', 'quit']:
                print("\n[系统] 感谢使用，再见！")
                break
            process_query(query)

if __name__ == "__main__":
    main() 