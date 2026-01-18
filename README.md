Personal Learning Code Repository
个人全栈 AI 学习代码仓库 | AI Infra / C++ / DL / RL / NLP / ML

    持续更新 ✨ | 个人学习练手代码合集，纯学习用途，所有核心代码附带详细注释，侧重原理理解与手写复现

📚 仓库简介
本仓库汇总本人学习过程中所有手写的练手代码、算法实现、工程化实践代码，覆盖AI 工程化 + 编程语言 + 全方向 AI 算法，无商业用途，仅作个人学习记录与复盘使用。
核心包含方向：

    AI Infra（AI 基础设施 / AI 工程化）核心实践代码
    C++ 从零基础入门到进阶的全量学习代码
    深度学习 (DL) / 强化学习 (RL) / 自然语言处理 (NLP) 经典算法与模型复现
    传统机器学习 (ML) 基础算法实现与调优实践
    轻量化学习笔记与核心知识点总结

🗂️ 仓库目录结构
```
├── 01-AI_Infra          # AI基础设施/AI工程化 学习代码 | 分布式训练/算子封装/模型部署/工程脚本
├── 02-Cpp_Learning      # C++ 学习代码 | 基础语法/进阶特性/STL/多线程/AI场景C++实现
├── 03-Deep_Learning     # 深度学习(DL) | CNN/RNN/Transformer/经典模型复现/梯度优化/框架实践
├── 04-Reinforcement_Learning # 强化学习(RL) | DQN/PPO/TD3/SAC/世界模型/Neural Physics 算法实现
├── 05-NLP_Learning      # 自然语言处理(NLP) | 文本预处理/词向量/TextCNN/Transformer/下游任务实践
├── 06-Machine_Learning  # 传统机器学习(ML) | 监督/无监督算法/特征工程/模型评估/调参实践
├── utils                # 通用工具类 | 跨模块复用的函数/数据处理/可视化/日志脚本
└── notes                # 学习笔记 | 核心知识点总结/公式推导/易错点记录 (Markdown)
```
📖 模块内容说明
✅ 01-AI_Infra
AI 工程化 / AI 基础设施相关学习代码，聚焦 AI 算法落地的工程能力，偏底层与实战：

    分布式训练基础、并行计算逻辑实现
    AI 框架核心原理：张量计算、算子封装、前向 / 反向传播底层逻辑
    模型部署与推理优化、训练数据流水线构建
    训练脚本封装、日志监控、超参调优工具
    AI 实验管理、模型保存与加载的工程化实现

✅ 02-Cpp_Learning
C++ 循序渐进的全阶段学习代码，覆盖从入门到适配 AI 场景的全部内容：

    基础语法：变量、循环、函数、指针、引用、结构体、类与对象、继承与多态
    进阶特性：模板编程、STL 容器 / 算法、智能指针、内存管理、多线程编程
    实战练习：经典数据结构实现、算法题解、小功能模块封装
    AI 场景适配：C++ 实现轻量化张量运算、算子逻辑、基础推理脚本

✅ 03-Deep_Learning
深度学习核心知识点与经典模型的手写实现，以理解原理为核心，兼顾框架实践：

    神经网络基础：全连接层、卷积层、池化层、循环层、注意力机制核心实现
    经典模型复现：ResNet、MobileNet、BERT 基础版、GAN、VAE 等轻量化实现
    优化方法：梯度下降、反向传播、正则化、BatchNorm、Dropout 手写逻辑
    框架实践：PyTorch/TensorFlow 基础用法、模型定义与训练流程封装

✅ 04-Reinforcement_Learning
强化学习全方向学习代码，包含基础到进阶的核心算法与实践：

    经典 RL 算法：DQN、Double DQN、Dueling DQN、PPO、TD3、SAC、A2C 完整实现
    进阶内容：世界模型 (World Models)、Neural Physics 相关实践代码
    基础理论：马尔可夫决策过程、策略梯度、值函数估计、蒙特卡洛采样
    环境交互：Gym 环境适配、自定义简单决策环境实现

✅ 05-NLP_Learning
自然语言处理全流程学习代码，从文本预处理到下游任务全覆盖：

    文本预处理：分词、去停用词、文本清洗、词性标注、数据增强
    词向量实现：Word2Vec、GloVe、FastText、Sentence-BERT
    经典模型：TextCNN、TextRNN、Transformer 文本分类 / 生成 / 匹配实践
    工具库使用：HuggingFace Transformers、NLTK、Spacy 基础与进阶用法
    下游任务：情感分析、命名实体识别、文本摘要、机器翻译轻量化实现

✅ 06-Machine_Learning
传统机器学习经典算法的手写实现 + 框架调用对比，吃透底层原理：

    监督学习：线性回归、逻辑回归、决策树、随机森林、XGBoost、SVM、KNN
    无监督学习：K-Means、层次聚类、DBSCAN、PCA 降维、因子分析
    特征工程：数据归一化 / 标准化、缺失值处理、特征选择与降维、特征交叉
    模型评估：交叉验证、混淆矩阵、ROC/AUC、精准率 / 召回率计算

✅ utils & notes

    utils: 所有模块通用的工具函数，一次编写、跨模块复用，减少冗余代码
    notes: 轻量化学习笔记，只记录核心知识点、公式推导、代码易错点，方便快速复盘，无长篇大论

⚙️ 开发环境 & 依赖说明

    均为稳定版环境，所有代码均可正常运行，无需刻意追求最新版本

    编程语言：Python 3.9+ ｜ C++11/14/17 (GCC/Clang/VS 均可编译)
    Python 核心依赖：numpy, pandas, torch, tensorflow, gym, transformers, scikit-learn, matplotlib
    C++ 工具：CMake 3.20+
    交互式学习：Jupyter Notebook (部分代码为.ipynb 格式)

📝 学习说明

    本仓库所有代码均为个人手写学习代码，非搬运，核心逻辑均附带中文注释，便于自身复盘与理解。
    代码以「理解原理」为首要目标，均为极简实现版本，非工业级生产代码，适合学习阶段使用。
    仓库会随学习进度持续更新，不断补充新的算法、工程化实践与知识点总结。
    代码如有疏漏或优化空间，欢迎指正，互相学习进步。

📄 License
This repository is licensed under the MIT License.
Feel free to use and modify the code for learning purposes.
