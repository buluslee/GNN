# GNN
本文件介绍了几个基础的GNN模型并且将其对应的模型的代码进行了复现和注释，其目的是让对GNN感兴趣的人能够去更快速的了解GNN模型
而进阶部分是对于不同的图类型——异构图、二部图（特殊异构图）、符号图、动态图的图结构特点的相关模型介绍.

传统的graph embedding为deep walk，LINE，Node2vec，struc2vec，SDNE
同构图模型为GCN，GAT,Graphsage
异构图模型为HAN，GTN,GATNE,BiNE
每个模型是由源码，我编写的ipynb文件，pdf文件（包含论文理论解析和代码的讲解）构成的。

建议学习方式：
1. 看pdf的理论部分了解模型架构和特点
2. 结合ipynb文件和pdf代码部分去学习模型框架是如何构建的
3. 学习好之后再去学习对应的源码，从而融会贯通。
