# src/models/ner_model.py
import torch.nn as nn
import torch.nn.utils.rnn as rnn
from .base import BaseNerNetwork # 导入基类

class BiGRUNerNetWork(BaseNerNetwork):
    def __init__(self, vocab_size, hidden_size, num_tags, num_gru_layers=1):
        super().__init__()
        # 1. Token Embedding 层
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        
        # 2. 使用 ModuleList 构建多层双向 GRU
        self.gru_layers = nn.ModuleList()
        for _ in range(num_gru_layers):
            self.gru_layers.append(
            nn.GRU(
                    input_size=hidden_size,
                hidden_size=hidden_size,
                num_layers=1,
                batch_first=True,
                bidirectional=True  # 开启双向
                )
            )
        
        # 3. 特征融合层
        self.fc = nn.Linear(hidden_size * 2, hidden_size)
        
        # 4. 分类决策层 (Classifier)
        self.classifier = nn.Linear(hidden_size, num_tags)

    def forward(self, token_ids, attention_mask):
        # 1. 计算真实长度
        lengths = attention_mask.sum(dim=1).cpu()
        
        # 2. 获取词向量
        embedded_text = self.embedding(token_ids)

        # 3. 打包序列
        current_packed_input = rnn.pack_padded_sequence(
            embedded_text, lengths, batch_first=True, enforce_sorted=False
        )
        
        # 4. 循环通过 GRU 层
        for gru_layer in self.gru_layers:
            # GRU 输出 (packed)
            packed_output, _ = gru_layer(current_packed_input)
            
            # 解包以进行后续操作，并指定 total_length
            output, _ = rnn.pad_packed_sequence(
                packed_output, batch_first=True, total_length=token_ids.shape[1]
            )
            
            # 特征融合
            features = self.fc(output)
            
            # 残差连接
            # 同样需要解包上一层的输入
            input_padded, _ = rnn.pad_packed_sequence(
                current_packed_input, batch_first=True, total_length=token_ids.shape[1]
            )
            current_input = features + input_padded
            
            # 重新打包作为下一层的输入
            current_packed_input = rnn.pack_padded_sequence(
                current_input, lengths, batch_first=True, enforce_sorted=False
            )
            
        # 5. 解包最终输出用于分类
        final_output, _ = rnn.pad_packed_sequence(
            current_packed_input, batch_first=True, total_length=token_ids.shape[1]
        )
        
        # 6. 分类
        logits = self.classifier(final_output)
        
        return logits