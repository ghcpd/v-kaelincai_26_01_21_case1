"""
测试脚本：验证prettytable的核心功能
Issue #206: Add mypy via pre-commit and make mypy pass

这个测试脚本用于验证在添加mypy类型检查和修复类型错误后，
prettytable的核心功能是否仍然正常工作。
"""

import sys
from prettytable import PrettyTable

def test_basic_creation():
    """测试基本的表格创建"""
    print("测试1: 基本表格创建...", end=" ")
    try:
        table = PrettyTable()
        table.field_names = ["Name", "Age"]
        table.add_row(["Alice", 30])
        result = table.get_string()
        assert "Alice" in result
        assert "30" in result
        print("✓ 通过")
        return True
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False

def test_alignment():
    """测试对齐功能"""
    print("测试2: 对齐功能...", end=" ")
    try:
        table = PrettyTable()
        table.field_names = ["Left", "Center", "Right"]
        table.add_row(["L", "C", "R"])
        table.align["Left"] = "l"
        table.align["Center"] = "c"
        table.align["Right"] = "r"
        result = table.get_string()
        assert len(result) > 0
        print("✓ 通过")
        return True
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False

def test_sorting():
    """测试排序功能"""
    print("测试3: 排序功能...", end=" ")
    try:
        table = PrettyTable()
        table.field_names = ["Name", "Score"]
        table.add_row(["Alice", 85])
        table.add_row(["Bob", 92])
        table.add_row(["Charlie", 78])
        
        # 测试排序
        sorted_result = table.get_string(sortby="Score")
        assert "Charlie" in sorted_result
        print("✓ 通过")
        return True
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False

def test_border_settings():
    """测试边框设置"""
    print("测试4: 边框设置...", end=" ")
    try:
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        
        # 测试边框开关
        table.border = False
        no_border = table.get_string()
        
        table.border = True
        with_border = table.get_string()
        
        assert len(with_border) > len(no_border)
        print("✓ 通过")
        return True
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False

def test_max_width():
    """测试最大宽度设置"""
    print("测试5: 最大宽度设置...", end=" ")
    try:
        table = PrettyTable()
        table.field_names = ["Long Text"]
        table.add_row(["This is a very long text that should be wrapped"])
        table.max_width["Long Text"] = 20
        result = table.get_string()
        assert len(result) > 0
        print("✓ 通过")
        return True
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False

def test_add_column():
    """测试添加列"""
    print("测试6: 添加列...", end=" ")
    try:
        table = PrettyTable()
        table.add_column("Name", ["Alice", "Bob", "Charlie"])
        table.add_column("Age", [30, 25, 35])
        result = table.get_string()
        assert "Alice" in result
        assert "30" in result
        print("✓ 通过")
        return True
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False

def test_field_names():
    """测试字段名设置"""
    print("测试7: 字段名设置...", end=" ")
    try:
        table = PrettyTable()
        table.field_names = ["Column1", "Column2", "Column3"]
        assert len(table.field_names) == 3
        assert "Column1" in table.field_names
        print("✓ 通过")
        return True
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False

def test_clear():
    """测试清除数据"""
    print("测试8: 清除数据...", end=" ")
    try:
        table = PrettyTable()
        table.field_names = ["A", "B"]
        table.add_row([1, 2])
        table.add_row([3, 4])
        
        # 清除行
        table.clear_rows()
        result = table.get_string()
        
        # 表头应该还在，但数据行应该没了
        assert "A" in result
        assert "1" not in result
        print("✓ 通过")
        return True
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("PrettyTable Issue #206 - 功能测试套件")
    print("=" * 60)
    print()
    
    tests = [
        test_basic_creation,
        test_alignment,
        test_sorting,
        test_border_settings,
        test_max_width,
        test_add_column,
        test_field_names,
        test_clear,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print()
    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    if failed == 0:
        print("✓ 所有测试通过！prettytable的核心功能正常工作。")
        print("  可以安全地进行mypy类型检查和修复。")
        return 0
    else:
        print("✗ 有测试失败！请先修复功能问题。")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
