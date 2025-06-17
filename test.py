import os
from agent import run_analysis_agent

def test_scenario_1():
    """测试场景1：模糊术语查询"""
    print("\n" + "="*50)
    print("测试场景1：模糊术语查询")
    print("="*50)
    
    # 测试用例1：模糊的术语
    test_query = "土地湿度是什么？"
    output_file = "output/test_scenario_1_result.txt"
    
    print(f"\n[测试] 输入查询: {test_query}")
    result = run_analysis_agent(
        instruction=1,  # 直接使用instruction 1进行测试
        prompt=test_query,
        output_path=output_file
    )
    
    print(f"\n[测试] 结果代码: {result}")
    if result == 0:
        print("[测试] 测试成功！")
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                print("\n--- 输出文件内容 ---")
                print(f.read())
                print("--- 文件结束 ---")
        except FileNotFoundError:
            print(f"[错误] 未找到输出文件: {output_file}")
    else:
        print("[测试] 测试失败！")

def test_scenario_2():
    """测试场景2：明确术语查询"""
    print("\n" + "="*50)
    print("测试场景2：明确术语查询")
    print("="*50)
    
    # 测试用例2：明确的术语
    test_query = "RSHub是什么？"
    output_file = "output/test_scenario_2_result.txt"
    
    print(f"\n[测试] 输入查询: {test_query}")
    result = run_analysis_agent(
        instruction=1,
        prompt=test_query,
        output_path=output_file
    )
    
    print(f"\n[测试] 结果代码: {result}")
    if result == 0:
        print("[测试] 测试成功！")
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                print("\n--- 输出文件内容 ---")
                print(f.read())
                print("--- 文件结束 ---")
        except FileNotFoundError:
            print(f"[错误] 未找到输出文件: {output_file}")
    else:
        print("[测试] 测试失败！")

if __name__ == "__main__":
    # 确保输出目录存在
    os.makedirs("output", exist_ok=True)
    
    # 运行测试场景
    test_scenario_1()
    test_scenario_2() 