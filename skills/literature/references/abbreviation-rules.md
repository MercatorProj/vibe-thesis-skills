# 简称生成规则

## 概述

本文档详细介绍文献简称的生成规则，包括英文文献和中文文献的简称生成方法。

## 简称生成原则

### 1. 唯一性原则

- 每个文献必须有唯一的简称
- 简称应能唯一标识该文献

### 2. 可读性原则

- 简称应易于阅读和记忆
- 避免使用过于复杂的缩写

### 3. 一致性原则

- 同类文献使用相同的简称格式
- 保持简称风格一致

### 4. 信息性原则

- 简称应包含作者名、年份和关键词
- 便于快速识别文献内容

## 英文文献简称生成规则

### 规则1: 作者姓氏首字母 + 年份 + 中文关键词

**格式**: `AuthorInitialsYear_ChineseKeywords`

**示例**:
```
Bai J, Zhu W, Liu S, et al. Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm[J]. Sustainability, 2025, 17(11): 4805.

简称: Bai2025_改进A星算法
```

### 规则2: 多作者处理

**格式**: `FirstAuthorInitialsYear_ChineseKeywords`

**示例**:
```
Li, C., Wang, H., & Zhang, Y. Off-road path planning with improved heuristic A* algorithm in mountainous terrain. Sensors, 2022, 22(18), 6950.

简称: Li2022_山地越野路径规划
```

### 规则3: 关键词提取

**关键词选择优先级**:
1. 论文标题中的核心名词
2. 论文标题中的动词
3. 论文标题中的形容词
4. 论文标题中的副词

**示例**:
```
Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm

关键词: 改进A星算法
```

### 规则4: 特殊字符处理

- 去掉特殊字符（如 `*`, `+`, `-`, `_` 等）
- 保留字母和数字

**示例**:
```
Improved A* Algorithm → ImprovedAStar
```

## 中文文献简称生成规则

### 规则1: 作者姓氏首字母 + 年份 + 中文关键词

**格式**: `AuthorSurnameInitialsYear_ChineseKeywords`

**示例**:
```
白朝谷, 李春波, 陆海, 等. 不同海拔对轻型汽车油耗的影响[J]. 专用汽车, 2023(10): 81-84.

简称: Bai2023_AltitudeFuelConsumption
```

### 规则2: 中文关键词提取

**提取原则**:
- 使用论文标题中的核心名词
- 保持简洁明了
- 便于记忆

**示例**:
```
不同海拔对轻型汽车油耗的影响 → 海拔对油耗影响
```

### 规则3: 多作者处理

**格式**: `FirstAuthorSurnameInitialsYear_ChineseKeywords`

**示例**:
```
高兴川, 杨秀, 李进涛. 1976—2016年青藏高原地区通达性空间格局演变[J]. 地理研究, 2018, 37(1): 13-26.

简称: Gao2018_通达性空间格局
```

### 规则4: 特殊字符处理

- 去掉中文标点符号
- 保留汉字和数字

**示例**:
```
1976—2016年青藏高原地区通达性空间格局演变 → AccessibilityPattern
```

## 混合文献简称生成规则

### 规则1: 所有文献使用中文规则

**英文文献示例**:
```
Bai J, Zhu W, Liu S, et al. Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm[J]. Sustainability, 2025, 17(11): 4805.

简称: Bai2025_改进A星算法
```

### 规则2: 中文文献使用中文规则

**示例**:
```
白朝谷, 李春波, 陆海, 等. 不同海拔对轻型汽车油耗的影响[J]. 专用汽车, 2023(10): 81-84.

简称: Bai2023_海拔对油耗影响
```

### 规则3: 中英文混合文献

**格式**: `AuthorInitialsYear_ChineseKeywords`

**示例**:
```
Wang F, Li Z, Chen B. Effect of low temperature on the performance of internal combustion engines: A review[J]. Applied Thermal Engineering, 2020, 179: 115688.

简称: Wang2020_低温对内燃机性能影响
```

## 简称命名规范

### 1. 大小写规则

- 首字母大写
- 其余字母小写（专有名词除外）
- 单词之间使用下划线分隔

**示例**:
```
Bai2025_ImprovedAStar
Bai2023_AltitudeFuelConsumption
```

### 2. 长度限制

- 简称长度建议不超过30个字符
- 避免过长的简称

**示例**:
```
# 好的简称
Bai2025_ImprovedAStar

# 不好的简称
Bai2025_PathPlanningMethodForUnmannedVehiclesInComplexOffRoadEnvironmentsBasedOnAnImprovedAStarAlgorithm
```

### 3. 特殊情况处理

- 相同作者同一年份发表多篇论文：添加字母后缀
- 示例: `Bai2025a_ImprovedAStar`, `Bai2025b_VehicleDynamics`

## 简称生成工具

### 1. 手动生成

**步骤**:
1. 提取作者姓氏首字母
2. 提取年份
3. 提取中文关键词
4. 组合成简称

**示例**:
```
Bai J, Zhu W, Liu S, et al. Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm[J]. Sustainability, 2025, 17(11): 4805.

1. 作者姓氏首字母: Bai
2. 年份: 2025
3. 中文关键词: 改进A星算法
4. 简称: Bai2025_改进A星算法
```

### 2. 自动生成

**工具**:
- Python脚本
- 正则表达式
- 自然语言处理工具

**示例脚本**:
```python
import re

def generate_abbreviation(reference):
    # 提取作者首字母
    author_match = re.search(r'^([A-Za-z]+) ', reference)
    if author_match:
        author = author_match.group(1)
    else:
        author = 'Unknown'
    
    # 提取年份
    year_match = re.search(r'\b(20\d{2})\b', reference)
    if year_match:
        year = year_match.group(1)
    else:
        year = '0000'
    
    # 提取关键词
    title_match = re.search(r'\. ([^\[]+)\[', reference)
    if title_match:
        title = title_match.group(1)
        # 提取核心关键词
        keywords = re.findall(r'(\b[A-Z][a-z]+\b)', title)
        if keywords:
            keyword = ''.join(keywords[:2])
        else:
            keyword = 'Keyword'
    else:
        keyword = 'Keyword'
    
    return f'{author}{year}_{keyword}'
```

## 质量检查清单

生成简称后，请检查以下内容：

- [ ] 简称包含作者名、年份和关键词
- [ ] 简称唯一
- [ ] 简称易于阅读和记忆
- [ ] 简称格式符合规范
- [ ] 简称长度合适
- [ ] 特殊字符处理正确
- [ ] 中英文文献使用不同的规则

## 常见错误

### 错误1: 简称重复

**错误示例**:
```
Bai2025_路径规划
Bai2025_路径规划
```

**正确示例**:
```
Bai2025_改进A星算法
Bai2025_车辆动力学
```

### 错误2: 简称过长

**错误示例**:
```
Bai2025_复杂越野环境下基于改进A星算法的无人车辆路径规划方法
```

**正确示例**:
```
Bai2025_改进A星算法
```

### 错误3: 简称信息不足

**错误示例**:
```
Bai2025
```

**正确示例**:
```
Bai2025_改进A星算法
```

### 错误4: 中英文规则混淆

**错误示例**:
```
白朝谷2023_AltitudeFuelConsumption
```

**正确示例**:
```
Bai2023_海拔对油耗影响
```

## 最佳实践

### 1. 保持一致性

- 所有文献使用相同的简称格式
- 避免混合使用不同的规则

### 2. 便于记忆

- 使用常见的关键词
- 避免使用过于专业的术语

### 3. 易于识别

- 简称应能快速反映文献内容
- 避免使用模糊的关键词

### 4. 定期检查

- 定期检查简称的唯一性
- 及时更新重复的简称

## 参考资料

- 学术写作指南: https://www.elsevier.com/authors/author-services/writing-your-paper
- BibTeX官方文档: https://www.bibtex.org/
- 文献管理软件指南: https://www.zotero.org/
