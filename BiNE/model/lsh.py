#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'CLH'
from datasketch import MinHashLSHForest, MinHash, MinHashLSH
import random
## 构建LSH结构
def construct_lsh(obj_dict):
    ##lsh_0 的阈值设置为 0，这意味着它会接受所有相似度的对象；
    ##lsh_5 的阈值设置为 0.6，只接受相似度高于或等于 0.6 的对象。这两个LSH对象都使用 128 个置换
    lsh_0 = MinHashLSH(threshold=0, num_perm=128,params=None)
    lsh_5 = MinHashLSH(threshold=0.6, num_perm=128,params=None)
    # forest = MinHashLSHForest(num_perm=128)
    keys = list(obj_dict.keys())
    values = list(obj_dict.values())
    ms = []
    ##构建两个不同阈值的 LSH 结构，允许以不同的相似度阈值查询对象
    for i in range(len(keys)):
        temp = MinHash(num_perm=128)
        for d in values[i]:
            temp.update(d.encode('utf8'))
        ms.append(temp)
        lsh_0.insert(keys[i], temp)
        lsh_5.insert(keys[i], temp)
    return lsh_0,lsh_5, keys, ms

## 6-1-1 get_negs_by_lsh
def get_negs_by_lsh(user_dict, item_dict, num_negs):
    ## 计算负样本的数量,至少300个
    sample_num_u = max(300, int(len(user_dict)*0.01*num_negs))
    sample_num_v = max(300, int(len(item_dict)*0.01*num_negs))
    ## 调用负样本生成函数call_get_negs_by_lsh
    negs_u = call_get_negs_by_lsh(sample_num_u,user_dict)
    negs_v = call_get_negs_by_lsh(sample_num_v,item_dict)
    return negs_u,negs_v

def call_get_negs_by_lsh(sample_num, obj_dict):
    ## 调用 construct_lsh 函数对对象构建
    lsh_0,lsh_5, keys, ms = construct_lsh(obj_dict)
    visited = []
    negs_dict = {}
    ## 遍历每个节点
    for i in range(len(keys)):
        ## 将每个未访问过的节点作为负样本。使用 LSH 查询相似和高度相似的对象集合，并从剩余对象中随机抽取负样本
        record = []
        if i in visited:
            continue
        visited.append(i)
        record.append(i)
        ##和中心节点相关的所有节点
        total_list = set(keys)
        ##和中心节点相似度高的节点
        sim_list = set(lsh_0.query(ms[i]))
        high_sim_list = set(lsh_5.query(ms[i]))
        ##在全部相关联的节点中减去相似度高的节点剩下的是负样本节点
        total_list = list(total_list - sim_list)

        ##total_list中随机抽取一定数量的负样本，
        for j in high_sim_list:
            total_list = set(total_list)
            ind = keys.index(j)
            if ind not in visited:
                visited.append(ind)
                record.append(ind)
            sim_list_child = set(lsh_0.query(ms[ind]))
            total_list = list(total_list - sim_list_child)
        total_list = random.sample(list(total_list), min(sample_num, len(total_list)))
        ##将这些负样本分配给与当前对象i相似的所有对象j
        for j in record:
            key = keys[j]
            negs_dict[key] = total_list
    return negs_dict
