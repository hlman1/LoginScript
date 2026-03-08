#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可视化匹配结果 - 帮助检查标记位置是否正确
"""
import cv2
import numpy as np
from pathlib import Path

print("=" * 70)
print("可视化匹配结果")
print("=" * 70)
print()

# 读取模板
template_path = Path('src/accept_button.png')
template = cv2.imread(str(template_path), cv2.IMREAD_GRAYSCALE)
template_h, template_w = template.shape
print(f"模板尺寸: {template_w} x {template_h}")
print()

# 测试图片
test_images = [
    ('test_images_temp/1.png', '图片1'),
    ('test_images_temp/2.png', '图片2'),
    ('test_images_temp/3.png', '图片3')
]

for img_path, name in test_images:
    print(f"[{name}] {img_path}")
    print("-" * 70)

    # 读取图片
    img = cv2.imread(img_path)
    if img is None:
        print(f"  无法读取图片")
        print()
        continue

    img_h, img_w = img.shape[:2]
    print(f"  图片尺寸: {img_w} x {img_h}")

    # 转灰度并匹配
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray, template, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    similarity = max_val
    loc = max_loc

    print(f"  相似度: {similarity*100:.2f}%")
    print(f"  匹配位置 (左上角): ({loc[0]}, {loc[1]})")

    # 计算矩形的四个角
    top_left = loc
    top_right = (loc[0] + template_w, loc[1])
    bottom_left = (loc[0], loc[1] + template_h)
    bottom_right = (loc[0] + template_w, loc[1] + template_h)
    center = (loc[0] + template_w // 2, loc[1] + template_h // 2)

    print(f"  匹配区域:")
    print(f"    左上角: {top_left}")
    print(f"    右上角: {top_right}")
    print(f"    左下角: {bottom_left}")
    print(f"    右下角: {bottom_right}")
    print(f"    中心点: {center}")

    # 创建标记图片（多种颜色）
    marked = img.copy()

    # 1. 绿色矩形框 (匹配区域)
    cv2.rectangle(marked, top_left, bottom_right, (0, 255, 0), 3)

    # 2. 红色中心点
    cv2.circle(marked, center, 5, (0, 0, 255), -1)

    # 3. 蓝色十字线（指向中心）
    cv2.line(marked, (center[0], 0), (center[0], img_h), (255, 0, 0), 1)
    cv2.line(marked, (0, center[1]), (img_w, center[1]), (255, 0, 0), 1)

    # 4. 添加文字标签
    label_pos = (loc[0], loc[1] - 10)
    cv2.putText(marked, f"{similarity*100:.1f}%", label_pos,
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 保存
    output_path = Path("test_results") / f"visual_{name}.png"
    cv2.imwrite(str(output_path), marked)
    print(f"  已保存可视化图片: {output_path.name}")

    # 提取匹配区域并放大显示
    match_region = img[loc[1]:loc[1]+template_h, loc[0]:loc[0]+template_w]
    # 放大 4 倍方便查看
    zoomed = cv2.resize(match_region, None, fx=4, fy=4, interpolation=cv2.INTER_NEAREST)
    zoomed_path = Path("test_results") / f"zoomed_{name}.png"
    cv2.imwrite(str(zoomed_path), zoomed)
    print(f"  已保存放大区域: {zoomed_path.name}")

    print()

print("=" * 70)
print("可视化完成！")
print()
print("标记说明:")
print("  绿色矩形框 = 匹配到的'接受'按钮区域")
print("  红色圆点 = 点击位置（中心点）")
print("  蓝色十字线 = 辅助线")
print("  文字标签 = 相似度百分比")
print()
print("请检查 test_results/ 目录中的图片:")
print("  visual_*.png - 带标记的完整图片")
print("  zoomed_*.png - 放大的匹配区域")
print("=" * 70)
