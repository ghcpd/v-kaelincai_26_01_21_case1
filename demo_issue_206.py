"""
演示脚本：展示prettytable的基本功能
Issue #206: Add mypy via pre-commit and make mypy pass

这个脚本演示prettytable的基本功能是否正常工作。
在添加mypy类型检查后，代码功能应该保持不变。
"""

from prettytable import PrettyTable

def demo_basic_table():
    """创建一个基本的表格"""
    print("=" * 60)
    print("演示1: 基本表格")
    print("=" * 60)
    
    table = PrettyTable()
    table.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
    table.add_row(["Adelaide", 1295, 1158259, 600.5])
    table.add_row(["Brisbane", 5905, 1857594, 1146.4])
    table.add_row(["Darwin", 112, 120900, 1714.7])
    table.add_row(["Hobart", 1357, 205556, 619.5])
    
    print(table)
    print()

def demo_alignment():
    """演示对齐功能"""
    print("=" * 60)
    print("演示2: 对齐设置")
    print("=" * 60)
    
    table = PrettyTable()
    table.field_names = ["Name", "Age", "City"]
    table.add_row(["Alice", 30, "New York"])
    table.add_row(["Bob", 25, "Los Angeles"])
    table.add_row(["Charlie", 35, "Chicago"])
    
    # 设置对齐
    table.align["Name"] = "l"  # 左对齐
    table.align["Age"] = "r"   # 右对齐
    table.align["City"] = "c"  # 居中对齐
    
    print(table)
    print()

def demo_sorting():
    """演示排序功能"""
    print("=" * 60)
    print("演示3: 排序功能")
    print("=" * 60)
    
    table = PrettyTable()
    table.field_names = ["Name", "Score"]
    table.add_row(["Alice", 85])
    table.add_row(["Bob", 92])
    table.add_row(["Charlie", 78])
    table.add_row(["David", 95])
    
    print("原始顺序:")
    print(table)
    print()
    
    print("按Score降序排序:")
    print(table.get_string(sortby="Score", reversesort=True))
    print()

def demo_styling():
    """演示样式设置"""
    print("=" * 60)
    print("演示4: 样式设置")
    print("=" * 60)
    
    table = PrettyTable()
    table.field_names = ["Item", "Price"]
    table.add_row(["Apple", "$1.50"])
    table.add_row(["Banana", "$0.75"])
    table.add_row(["Orange", "$1.25"])
    
    # 设置边框样式
    table.border = True
    table.header = True
    table.padding_width = 2
    
    print(table)
    print()

if __name__ == "__main__":
    print("PrettyTable Issue #206 演示")
    print("展示基本功能 - 在添加mypy类型检查前后应该保持一致")
    print()
    
    demo_basic_table()
    demo_alignment()
    demo_sorting()
    demo_styling()
    
    print("=" * 60)
    print("所有演示完成！")
    print("下一步：运行 'mypy src/prettytable' 查看类型错误")
    print("=" * 60)
