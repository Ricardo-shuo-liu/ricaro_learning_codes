import torch
from tqdm import tqdm
import os
from dataclasses import asdict

class Trainer:
    def __init__(self, model, optimizer, loss_fn, train_loader, dev_loader=None, 
                 eval_metric_fn=None, output_dir=None, device='cpu'):
        self.model = model.to(device)
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.train_loader = train_loader
        self.dev_loader = dev_loader
        self.eval_metric_fn = eval_metric_fn
        self.output_dir = output_dir
        self.device = torch.device(device)
        
        if self.output_dir:
            os.makedirs(self.output_dir, exist_ok=True)

    def fit(self, epochs):
        best_metric = float('inf')  # 初始化一个无穷大的 best_metric，用于后续比较
        
        for epoch in range(1, epochs + 1):
            # 1. 执行一个周期的训练
            train_loss = self._train_one_epoch()
            print(f"Epoch {epoch} - Training Loss: {train_loss:.4f}")

            # 2. 执行评估
            metrics = self._evaluate()
            if metrics:
                print(f"Epoch {epoch} - Validation Metrics: {metrics}")
                current_metric = metrics.get('loss')  # 默认监控验证集 loss
                
                # 3. 如果当前 metric 优于历史最优，则保存最佳模型
                if current_metric < best_metric:
                    best_metric = current_metric
                    if self.output_dir:
                        self._save_checkpoint(is_best=True)
                        print(f"New best model saved with validation loss: {best_metric:.4f}")

            # 4. 每个 epoch 结束后，保存最新的模型状态
            if self.output_dir:
                self._save_checkpoint(is_best=False)

    def _train_one_epoch(self):
        """执行一个完整的训练周期。"""
        self.model.train()  # 设置为训练模式
        total_loss = 0
        
        # 使用 tqdm 显示进度条
        for batch in tqdm(self.train_loader, desc=f"Training Epoch"):
            outputs = self._train_step(batch)
            total_loss += outputs['loss'].item()  # 累加 loss
        
        return total_loss / len(self.train_loader)  # 返回平均 loss

    def _train_step(self, batch):
        """执行单个训练步骤（前向、损失、反向）。"""
        # 1. 将数据移动到指定设备
        batch = {k: v.to(self.device) for k, v in batch.items() if isinstance(v, torch.Tensor)}

        # 2. 模型前向传播
        logits = self.model(token_ids=batch['token_ids'], attention_mask=batch['attention_mask'])
        
        # 3. 计算损失
        # CrossEntropyLoss 要求 logits 的形状为 [B, C, L]，label_ids 的形状为 [B, L]
        loss = self.loss_fn(logits.permute(0, 2, 1), batch['label_ids'])
            
        # 4. 反向传播与参数更新
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return {'loss': loss, 'logits': logits}

    def _evaluate(self):
        """在验证集上执行评估。"""
        if self.dev_loader is None:
            return None

        self.model.eval()  # 设置为评估模式
        total_loss = 0
        all_logits = []
        all_labels = []
        all_attention_mask = []

        with torch.no_grad():  # 禁用梯度计算
            for batch in tqdm(self.dev_loader, desc="Evaluating"):
                outputs = self._evaluation_step(batch)
                
                total_loss += outputs['loss'].item()
                # 收集所有批次的 logits 和 labels，用于后续评估
                all_logits.append(outputs['logits'].cpu())
                all_labels.append(batch['label_ids'].cpu())
                all_attention_mask.append(batch['attention_mask'].cpu())
        
        metrics = {}
        # 如果提供了评估函数，则调用它来计算指标
        if self.eval_metric_fn:
            metrics = self.eval_metric_fn(all_logits, all_labels, all_attention_mask)
        
        # 计算并记录平均 loss
        metrics['loss'] = total_loss / len(self.dev_loader)
        return metrics

    def _evaluation_step(self, batch):
        """执行单个评估步骤（前向、损失）。"""
        # 1. 将数据移动到指定设备
        batch = {k: v.to(self.device) for k, v in batch.items() if isinstance(v, torch.Tensor)}
        
        # 2. 模型前向传播
        logits = self.model(token_ids=batch['token_ids'], attention_mask=batch['attention_mask'])
        
        # 3. 计算损失
        loss = self.loss_fn(logits.permute(0, 2, 1), batch['label_ids'])
        
        return {'loss': loss, 'logits': logits}

    def _save_checkpoint(self, is_best):
        """保存模型检查点。"""
        state = {'model_state_dict': self.model.state_dict()}
        if is_best:
            # 保存最佳模型
            torch.save(state, os.path.join(self.output_dir, 'best_model.pth'))
        # 保存最新模型
        torch.save(state, os.path.join(self.output_dir, 'last_model.pth'))