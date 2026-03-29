# 转换示例

## 概述

本文档提供参考文献到BibTeX格式的转换示例，包括英文文献、中文文献和混合文献的转换。**生成 .bib 时尽量附带摘要**：若能从 PDF 提取、用户提供或阅读笔记中得到文章主旨/摘要，在 `note` 字段中增加「摘要: …」；无可靠来源时不编造，可仅保留中文简称/英文原名。

## 摘要写入约定

- **来源**：按优先级使用：(1) 文献自带的摘要（PDF 元数据或正文中的 Abstract/摘要）；(2) 用户提供的摘要或阅读笔记；(3) **若无现成摘要但可读取原文**（如 PDF 正文、已提取文本），则从原文中总结摘要（1～2 句话概括研究问题、方法及主要结论）。
- **格式**：在 `note` 中与简称并列，例如：`note = {中文简称: …；摘要: 研究问题、方法及主要结论的 1～2 句话概括。}` 或 `note = {英文原名: …；摘要: …}`。
- **原则**：有现成摘要则用，无则从原文总结；不编造与原文无关的内容。

## 英文文献转换示例

### 示例1: 期刊论文

**输入**:
```
Bai J, Zhu W, Liu S, et al. Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm[J]. Sustainability, 2025, 17(11): 4805.
```

**输出**:
```bibtex
@article{Bai2025_ImprovedAStar,
    author = {Bai J, Zhu W, Liu S, et al.},
    title = {Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm},
    journal = {Sustainability},
    year = {2025},
    volume = {17},
    number = {11},
    pages = {4805},
    note = {英文原名: Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm}
}
```

### 示例2: 会议论文

**输入**:
```
Li, C., Wang, H., & Zhang, Y. Off-road path planning with improved heuristic A* algorithm in mountainous terrain. Sensors, 2022, 22(18), 6950.
```

**输出**:
```bibtex
@inproceedings{Li2022_OffRoadPathPlanning,
    author = {Li, C., Wang, H., & Zhang, Y.},
    title = {Off-road path planning with improved heuristic A* algorithm in mountainous terrain},
    booktitle = {Sensors Conference},
    year = {2022},
    pages = {6950},
    note = {英文原名: Off-road path planning with improved heuristic A* algorithm in mountainous terrain}
}
```

### 示例3: 学位论文

**输入**:
```
Shen C. A Topology-Aware Hierarchical Planning and Control Framework for Highly Dynamical Autonomous Ground Vehicles[D]. 清华大学, 2025.
```

**输出**:
```bibtex
@phdthesis{Shen2025_TopologyAwarePlanning,
    author = {Shen C.},
    title = {A Topology-Aware Hierarchical Planning and Control Framework for Highly Dynamical Autonomous Ground Vehicles},
    school = {清华大学},
    year = {2025},
    note = {英文原名: A Topology-Aware Hierarchical Planning and Control Framework for Highly Dynamical Autonomous Ground Vehicles}
}
```

### 示例4: 书籍

**输入**:
```
Wong J Y. Theory of ground vehicles[M]. John Wiley & Sons, 2022.
```

**输出**:
```bibtex
@book{Wong2022_GroundVehicles,
    author = {Wong J Y.},
    title = {Theory of ground vehicles},
    publisher = {John Wiley \& Sons},
    year = {2022},
    note = {英文原名: Theory of ground vehicles}
}
```

### 示例5: 技术报告

**输入**:
```
Frankenstein S, Koenig G. Fast all-season soil STrength (FASST)[R]. U.S. Army Engineer Research and Development Center, 2004, ERDC/CRREL SR-04-1.
```

**输出**:
```bibtex
@techreport{Frankenstein2004_FASST,
    author = {Frankenstein S, Koenig G.},
    title = {Fast all-season soil STrength (FASST)},
    institution = {U.S. Army Engineer Research and Development Center},
    year = {2004},
    number = {ERDC/CRREL SR-04-1},
    note = {英文原名: Fast all-season soil STrength (FASST)}
}
```

### 示例6: 网页

**输入**:
```
U.S. Department of Agriculture. Elementary soils engineering (Chapter. 4)[EB/OL]. https://directives.nrcs.usda.gov/sites/default/files2/1712930846/31760.pdf, 2021.
```

**输出**:
```bibtex
@online{USDA2021_SoilEngineering,
    author = {U.S. Department of Agriculture},
    title = {Elementary soils engineering (Chapter. 4)},
    url = {https://directives.nrcs.usda.gov/sites/default/files2/1712930846/31760.pdf},
    year = {2021},
    note = {英文原名: Elementary soils engineering (Chapter. 4)}
}
```

## 中文文献转换示例

### 示例1: 期刊论文

**输入**:
```
白朝谷, 李春波, 陆海, 等. 不同海拔对轻型汽车油耗的影响[J]. 专用汽车, 2023(10): 81-84.
```

**输出**:
```bibtex
@article{Bai2023_AltitudeFuelConsumption,
    author = {白朝谷, 李春波, 陆海, 等.},
    title = {不同海拔对轻型汽车油耗的影响},
    journal = {专用汽车},
    year = {2023},
    number = {10},
    pages = {81-84},
    note = {中文简称: 不同海拔对轻型汽车油耗的影响}
}
```

### 示例2: 会议论文

**输入**:
```
李进涛, 高兴川, 杨秀. 青藏高原地区道路通达性评价方法研究[C]// 2018年中国地理学会学术年会, 2018: 1-10.
```

**输出**:
```bibtex
@inproceedings{Li2018_AccessibilityEvaluation,
    author = {李进涛, 高兴川, 杨秀.},
    title = {青藏高原地区道路通达性评价方法研究},
    booktitle = {2018年中国地理学会学术年会},
    year = {2018},
    pages = {1-10},
    note = {中文简称: 青藏高原地区道路通达性评价方法研究}
}
```

### 示例3: 学位论文

**输入**:
```
陶泽兴. 基于复杂地表环境与车辆受力分析的越野机动路径规划方法[D]. 清华大学, 2024.
```

**输出**:
```bibtex
@phdthesis{Tao2024_OffRoadPathPlanning,
    author = {陶泽兴.},
    title = {基于复杂地表环境与车辆受力分析的越野机动路径规划方法},
    school = {清华大学},
    year = {2024},
    note = {中文简称: 基于复杂地表环境与车辆受力分析的越野机动路径规划方法}
}
```

### 示例4: 书籍

**输入**:
```
王健, 李军. 车辆动力学建模与仿真[M]. 机械工业出版社, 2023.
```

**输出**:
```bibtex
@book{Wang2023_VehicleDynamics,
    author = {王健, 李军.},
    title = {车辆动力学建模与仿真},
    publisher = {机械工业出版社},
    year = {2023},
    note = {中文简称: 车辆动力学建模与仿真}
}
```

### 示例5: 技术报告

**输入**:
```
中国科学院青藏高原研究所. 青藏高原环境变化科学评估报告[R]. 科学出版社, 2022.
```

**输出**:
```bibtex
@techreport{CAS2022_TibetanPlateauAssessment,
    author = {中国科学院青藏高原研究所.},
    title = {青藏高原环境变化科学评估报告},
    institution = {科学出版社},
    year = {2022},
    note = {中文简称: 青藏高原环境变化科学评估报告}
}
```

### 示例6: 网页

**输入**:
```
中华人民共和国自然资源部. 青藏高原生态保护法[EB/OL]. http://www.mnr.gov.cn/zwgk/fggw/flfg/202304/t20230426_2786660.html, 2023.
```

**输出**:
```bibtex
@online{MNRC2023_EcologyProtection,
    author = {中华人民共和国自然资源部.},
    title = {青藏高原生态保护法},
    url = {http://www.mnr.gov.cn/zwgk/fggw/flfg/202304/t20230426_2786660.html},
    year = {2023},
    note = {中文简称: 青藏高原生态保护法}
}
```

## 混合文献转换示例

### 示例1: 中英文混合

**输入**:
```
Bai J, Zhu W, Liu S, et al. Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm[J]. Sustainability, 2025, 17(11): 4805.

白朝谷, 李春波, 陆海, 等. 不同海拔对轻型汽车油耗的影响[J]. 专用汽车, 2023(10): 81-84.

Li, C., Wang, H., & Zhang, Y. Off-road path planning with improved heuristic A* algorithm in mountainous terrain. Sensors, 2022, 22(18), 6950.

高兴川, 杨秀, 李进涛. 1976—2016年青藏高原地区通达性空间格局演变[J]. 地理研究, 2018, 37(1): 13-26.
```

**输出**:
```bibtex
@article{Bai2025_ImprovedAStar,
    author = {Bai J, Zhu W, Liu S, et al.},
    title = {Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm},
    journal = {Sustainability},
    year = {2025},
    volume = {17},
    number = {11},
    pages = {4805},
    note = {英文原名: Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm}
}

@article{Bai2023_AltitudeFuelConsumption,
    author = {白朝谷, 李春波, 陆海, 等.},
    title = {不同海拔对轻型汽车油耗的影响},
    journal = {专用汽车},
    year = {2023},
    number = {10},
    pages = {81-84},
    note = {中文简称: 不同海拔对轻型汽车油耗的影响}
}

@inproceedings{Li2022_OffRoadPathPlanning,
    author = {Li, C., Wang, H., & Zhang, Y.},
    title = {Off-road path planning with improved heuristic A* algorithm in mountainous terrain},
    booktitle = {Sensors Conference},
    year = {2022},
    pages = {6950},
    note = {英文原名: Off-road path planning with improved heuristic A* algorithm in mountainous terrain}
}

@article{Gao2018_AccessibilityPattern,
    author = {高兴川, 杨秀, 李进涛.},
    title = {1976—2016年青藏高原地区通达性空间格局演变},
    journal = {地理研究},
    year = {2018},
    volume = {37},
    number = {1},
    pages = {13-26},
    note = {中文简称: 1976—2016年青藏高原地区通达性空间格局演变}
}
```

## 特殊情况转换示例

### 示例1: 无作者文献

**输入**:
```
[J]. 中国公路学报, 2023, 36(5): 1-10.
```

**输出**:
```bibtex
@article{Unknown2023_JournalArticle,
    author = {[未知作者]},
    title = {[未知标题]},
    journal = {中国公路学报},
    year = {2023},
    volume = {36},
    number = {5},
    pages = {1-10},
    note = {中文简称: 未知文献}
}
```

### 示例2: 无年份文献

**输入**:
```
张三, 李四. 车辆动力学研究[J]. 汽车工程.
```

**输出**:
```bibtex
@article{Zhang0000_VehicleDynamics,
    author = {张三, 李四.},
    title = {车辆动力学研究},
    journal = {汽车工程},
    year = {0000},
    note = {中文简称: 车辆动力学研究}
}
```

### 示例3: 无标题文献

**输入**:
```
王五, 赵六. [J]. 机械工程学报, 2024, 50(2): 1-10.
```

**输出**:
```bibtex
@article{Wang2024_UnknownTitle,
    author = {王五, 赵六.},
    title = {[未知标题]},
    journal = {机械工程学报},
    year = {2024},
    volume = {50},
    number = {2},
    pages = {1-10},
    note = {中文简称: 未知标题文献}
}
```

### 示例4: 多卷期文献

**输入**:
```
Smith J, Johnson A. A study on vehicle dynamics[J]. Journal of Automotive Engineering, 2023, 45(3-4): 100-120.
```

**输出**:
```bibtex
@article{Smith2023_VehicleDynamics,
    author = {Smith J, Johnson A.},
    title = {A study on vehicle dynamics},
    journal = {Journal of Automotive Engineering},
    year = {2023},
    volume = {45},
    number = {3-4},
    pages = {100-120},
    note = {英文原名: A study on vehicle dynamics}
}
```

### 示例5: 多页码范围文献

**输入**:
```
Brown K, Davis B. Path planning in complex environments[J]. Robotics and Autonomous Systems, 2022, 150: 1-10, 20-30.
```

**输出**:
```bibtex
@article{Brown2022_PathPlanning,
    author = {Brown K, Davis B.},
    title = {Path planning in complex environments},
    journal = {Robotics and Autonomous Systems},
    year = {2022},
    volume = {150},
    pages = {1-10, 20-30},
    note = {英文原名: Path planning in complex environments}
}
```

## 转换流程示例

### 示例1: 完整转换流程

**输入**:
```
1. Bai J, Zhu W, Liu S, et al. Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm[J]. Sustainability, 2025, 17(11): 4805.
2. 白朝谷, 李春波, 陆海, 等. 不同海拔对轻型汽车油耗的影响[J]. 专用汽车, 2023(10): 81-84.
```

**步骤1: 识别文献类型**

- 第1篇: 英文期刊论文
- 第2篇: 中文期刊论文

**步骤2: 提取作者和年份**

- 第1篇: 作者Bai J, 年份2025
- 第2篇: 作者白朝谷, 年份2023

**步骤3: 生成简称**

- 第1篇: Bai2025_ImprovedAStar
- 第2篇: Bai2023_AltitudeFuelConsumption

**步骤4: 生成BibTeX条目**

生成每条条目时，若存在该文献的摘要或阅读总结，在 `note` 中增加「摘要: …」；否则仅写中文简称/英文原名。

```bibtex
@article{Bai2025_ImprovedAStar,
    author = {Bai J, Zhu W, Liu S, et al.},
    title = {Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm},
    journal = {Sustainability},
    year = {2025},
    volume = {17},
    number = {11},
    pages = {4805},
    note = {英文原名: Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm}
}

@article{Bai2023_AltitudeFuelConsumption,
    author = {白朝谷, 李春波, 陆海, 等.},
    title = {不同海拔对轻型汽车油耗的影响},
    journal = {专用汽车},
    year = {2023},
    number = {10},
    pages = {81-84},
    note = {中文简称: 不同海拔对轻型汽车油耗的影响}
}
```

## 质量检查示例

### 示例1: 检查BibTeX条目

**输入**:
```bibtex
@article{Bai2025_ImprovedAStar,
    author = {Bai J, Zhu W, Liu S, et al.},
    title = {Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm},
    journal = {Sustainability},
    year = {2025},
    volume = {17},
    number = {11},
    pages = {4805},
    note = {英文原名: Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm}
}
```

**检查内容**:

- [x] 文献类型正确（@article）
- [x] 作者字段正确
- [x] 标题字段正确
- [x] 期刊字段正确
- [x] 年份字段正确
- [x] 卷号字段正确
- [x] 期号字段正确
- [x] 页码字段正确
- [x] 备注字段包含英文原名
- [x] 简称包含作者名、年份和关键词

### 示例2: 检查简称

**输入**:
```
Bai2025_ImprovedAStar
```

**检查内容**:

- [x] 包含作者名（Bai）
- [x] 包含年份（2025）
- [x] 包含关键词（ImprovedAStar）
- [x] 格式正确（驼峰式命名）
- [x] 长度合适（不超过30个字符）

## 常见错误示例

### 错误1: 字段缺失

**错误输入**:
```bibtex
@article{Bai2025_ImprovedAStar,
    author = {Bai J, Zhu W, Liu S, et al.},
    title = {Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm},
    year = {2025}
}
```

**正确输入**:
```bibtex
@article{Bai2025_ImprovedAStar,
    author = {Bai J, Zhu W, Liu S, et al.},
    title = {Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm},
    journal = {Sustainability},
    year = {2025},
    volume = {17},
    number = {11},
    pages = {4805},
    note = {英文原名: Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm}
}
```

### 错误2: 格式错误

**错误输入**:
```bibtex
@article{Bai2025_ImprovedAStar,
    author = 