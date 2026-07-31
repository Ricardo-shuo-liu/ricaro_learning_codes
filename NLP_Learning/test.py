import torch
import torch.nn as nn

gru = nn.GRU(
    input_size=16,
    hidden_size=32,
    num_layers=2,
    bidirectional=True,    # 双向 directions=2
    batch_first=True
)
B, L = 3, 10
x = torch.randn(B, L, 16)

output, h_n = gru(x)
print("output shape:", output.shape)  # [3, 10, 64]  (32*2)
print("h_n shape:", h_n.shape)        # [4, 3, 32]   (2层×2方向=4)
