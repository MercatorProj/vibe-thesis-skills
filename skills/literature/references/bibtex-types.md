# BibTeX类型详细说明

## 概述

本文档详细介绍BibTeX中常用的文献类型及其字段要求。

## 常用文献类型

### 1. 期刊论文（@article）

**适用场景**: 发表在学术期刊上的论文

**必填字段**:
- `author`: 作者
- `title`: 标题
- `journal`: 期刊名称
- `year`: 发表年份

**可选字段**:
- `volume`: 卷号
- `number`: 期号
- `pages`: 页码范围
- `month`: 发表月份
- `note`: 备注信息（建议包含：中文简称/英文原名；若来源可靠可增加「摘要: …」）
- `abstract`: 部分样式支持；本项目习惯将摘要写入 `note` 便于查阅

**示例**:
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

### 2. 会议论文（@inproceedings）

**适用场景**: 发表在学术会议上的论文

**必填字段**:
- `author`: 作者
- `title`: 标题
- `booktitle`: 会议名称
- `year`: 发表年份

**可选字段**:
- `editor`: 会议编辑
- `volume`: 卷号
- `number`: 期号
- `pages`: 页码范围
- `address`: 会议地点
- `month`: 会议月份
- `note`: 备注信息

**示例**:
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

### 3. 学位论文（@phdthesis / @mastersthesis）

**适用场景**: 博士或硕士学位论文

**必填字段**:
- `author`: 作者
- `title`: 标题
- `school`: 学校名称
- `year`: 毕业年份

**可选字段**:
- `address`: 学校地址
- `month`: 毕业月份
- `note`: 备注信息

**示例**:
```bibtex
@phdthesis{Shen2025_TopologyAwarePlanning,
    author = {Shen C.},
    title = {A Topology-Aware Hierarchical Planning and Control Framework for Highly Dynamical Autonomous Ground Vehicles},
    school = {清华大学},
    year = {2025},
    note = {英文原名: A Topology-Aware Hierarchical Planning and Control Framework for Highly Dynamical Autonomous Ground Vehicles}
}
```

### 4. 书籍（@book）

**适用场景**: 正式出版的书籍

**必填字段**:
- `author`: 作者
- `title`: 书名
- `publisher`: 出版社
- `year`: 出版年份

**可选字段**:
- `editor`: 编辑
- `volume`: 卷号
- `number`: 期号
- `series`: 丛书名称
- `address`: 出版社地址
- `edition`: 版本
- `month`: 出版月份
- `note`: 备注信息

**示例**:
```bibtex
@book{Wong2022_GroundVehicles,
    author = {Wong J Y.},
    title = {Theory of ground vehicles},
    publisher = {John Wiley \& Sons},
    year = {2022},
    note = {英文原名: Theory of ground vehicles}
}
```

### 5. 技术报告（@techreport）

**适用场景**: 技术报告、白皮书等

**必填字段**:
- `author`: 作者
- `title`: 标题
- `institution`: 发布机构
- `year`: 发布年份

**可选字段**:
- `type`: 报告类型
- `number`: 报告编号
- `address`: 机构地址
- `month`: 发布月份
- `note`: 备注信息

**示例**:
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

### 6. 网页（@online）

**适用场景**: 网页、在线资源

**必填字段**:
- `author`: 作者
- `title`: 网页标题
- `url`: 网页地址
- `year`: 访问年份

**可选字段**:
- `month`: 访问月份
- `day`: 访问日期
- `note`: 备注信息

**示例**:
```bibtex
@online{USDA2021_SoilEngineering,
    author = {U.S. Department of Agriculture},
    title = {Elementary soils engineering (Chapter. 4)},
    url = {https://directives.nrcs.usda.gov/sites/default/files2/1712930846/31760.pdf},
    year = {2021},
    note = {英文原名: Elementary soils engineering (Chapter. 4)}
}
```

### 7. 未发表论文（@unpublished）

**适用场景**: 未发表的论文、预印本等

**必填字段**:
- `author`: 作者
- `title`: 标题
- `note`: 备注信息（包含状态）

**可选字段**:
- `month`: 完成月份
- `year`: 完成年份

**示例**:
```bibtex
@unpublished{Li2024_VehicleDynamics,
    author = {Li J, Wang Y, Zhang H.},
    title = {Vehicle dynamics modeling in complex terrain},
    note = {预印本，未发表},
    year = {2024},
    note = {英文原名: Vehicle dynamics modeling in complex terrain}
}
```

## 特殊文献类型

### 8. 合集（@collection）

**适用场景**: 多作者合集

**必填字段**:
- `editor`: 编辑
- `title`: 书名
- `publisher`: 出版社
- `year`: 出版年份

### 9. 专利（@patent）

**适用场景**: 专利

**必填字段**:
- `author`: 发明人
- `title`: 专利名称
- `number`: 专利号
- `year`: 申请年份
- `country`: 国家

### 10. 标准（@standard）

**适用场景**: 标准文件

**必填字段**:
- `title`: 标准名称
- `organization`: 制定机构
- `year`: 发布年份

## 字段说明

### 作者字段（author）

**格式**:
- 英文: `Last1 F, Last2 F, Last3 F, et al.`
- 中文: `作者1, 作者2, 作者3, 等.`

**示例**:
```
Bai J, Zhu W, Liu S, et al.
白朝谷, 李春波, 陆海, 等.
```

### 标题字段（title）

**格式**:
- 英文: 首字母大写，其余小写（专有名词除外）
- 中文: 保持原样

**示例**:
```
Path Planning Method for Unmanned Vehicles in Complex Off-Road Environments Based on an Improved A* Algorithm
不同海拔对轻型汽车油耗的影响
```

### 年份字段（year）

**格式**: 四位数字

**示例**:
```
2025
2023
```

### 页码字段（pages）

**格式**:
- 单页: `4805`
- 多页: `81-84`
- 多范围: `1-10, 20-30`

**示例**:
```
pages = {4805}
pages = {81-84}
```

## 字段优先级

### 期刊论文

1. author
2. title
3. journal
4. year
5. volume
6. number
7. pages
8. note

### 会议论文

1. author
2. title
3. booktitle
4. year
5. pages
6. note

### 学位论文

1. author
2. title
3. school
4. year
5. note

### 书籍

1. author
2. title
3. publisher
4. year
5. note

## 注意事项

1. **字段顺序**: 建议按照上述优先级顺序排列字段
2. **标点符号**: 字段值后加逗号，最后一个字段不加逗号
3. **特殊字符**: 特殊字符需要转义（如 `&` → `\&`）
4. **空格**: 字段值前后加空格
5. **大小写**: 英文标题首字母大写，其余小写

## 质量检查清单

创建BibTeX条目时，请检查以下内容：

- [ ] 文献类型选择正确
- [ ] 所有必填字段都已包含
- [ ] 字段值格式正确
- [ ] 标点符号使用正确
- [ ] 特殊字符已转义
- [ ] 字段顺序合理
- [ ] 备注信息包含英文原名或中文简称
- [ ] **摘要**：若有现成摘要或用户/阅读笔记则写入 `note`；若无摘要但可读取原文（PDF 正文、已提取文本），则从原文总结 1～2 句话作为「摘要: …」写入 `note`；仅当既无摘要又无法读原文时省略，不编造

## 参考资料

- BibTeX官方文档: https://www.bibtex.org/
- LaTeX官方文档: https://www.latex-project.org/
- 学术写作指南: https://www.elsevier.com/authors/author-services/writing-your-paper
