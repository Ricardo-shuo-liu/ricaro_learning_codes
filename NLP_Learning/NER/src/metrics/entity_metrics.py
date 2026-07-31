# src/metrics/entity_metrics.py
import torch

def _trans_entity2tuple(label_ids, id2tag):
    """
    将标签ID序列转换为实体元组列表（严格 BMES 解码）。
    仅在遇到 E- 或 S- 时落盘；遇到新的 B- 或 O 不闭合未完成片段。
    """
    entities = []
    current_entity = None

    for i, label_id in enumerate(label_ids):
        # 将标签ID映射为字符串标签，未知则视作 'O'
        tag = id2tag.get(label_id.item(), 'O')

        if tag.startswith('B-'):
            # 开启新片段：记录类型与起始位置；end 暂定为 i+1
            current_entity = (tag[2:], i, i + 1)
        elif tag.startswith('M-'):
            # 仅当已存在片段，且类型一致时续接（扩展 end）
            if current_entity and current_entity[0] == tag[2:]:
                current_entity = (current_entity[0], current_entity[1], i + 1)
            else:
                # 类型不一致或不存在片段：丢弃未完成片段
                current_entity = None
        elif tag.startswith('E-'):
            # 仅当已存在片段且类型一致时闭合并落盘
            if current_entity and current_entity[0] == tag[2:]:
                current_entity = (current_entity[0], current_entity[1], i + 1)
                entities.append(current_entity)
            # 无论是否匹配，E- 都视为一次片段结束
            current_entity = None
        elif tag.startswith('S-'):
            # 单字实体：直接落盘（start=i, end=i+1）
            entities.append((tag[2:], i, i + 1))
            current_entity = None
        else:  # 'O'
            # 非实体位置：严格模式不闭合未完成片段，直接丢弃
            current_entity = None

    # 返回集合去重
    return set(entities)

def calculate_entity_level_metrics(all_pred_ids, all_label_ids, id2tag):
    """
    逐样本评估（未使用 mask），解码采用严格 BMES。
    """
    true_entities = set()
    pred_entities = set()

    # 遍历批次中的每一个样本
    for i in range(len(all_label_ids)):
        # 将标签ID序列解码为实体集合（严格 BMES）
        sample_true_entities = _trans_entity2tuple(all_label_ids[i], id2tag)
        sample_pred_entities = _trans_entity2tuple(all_pred_ids[i], id2tag)
        
        true_entities.update(sample_true_entities)
        pred_entities.update(sample_pred_entities)
        
    # 计算 TP / FP / FN
    num_correct = len(true_entities.intersection(pred_entities))  # TP
    num_true = len(true_entities)   # TP + FN
    num_pred = len(pred_entities)   # TP + FP

    # 计算 P / R / F1（含零保护）
    precision = num_correct / num_pred if num_pred > 0 else 0.0
    recall = num_correct / num_true if num_true > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {"precision": precision, "recall": recall, "f1": f1}