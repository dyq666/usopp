## 项目概述

项目名: 海贼王乌索普.

简介: 学习数据结构和算法.

目录结构:

- structure 数据结构.
- test 每种数据结构的测试.
- leetcode 题解和相应测试.

## 使用方式

安装: pip install -r requirement.txt

运行测试: pytest ./test

## 项目说明

目前包含以下数据结构:

  - 动态数组 DynamicArrayV2 (可用于实现栈)
  - 循环数组 LoopArrayV3 (可用于实现双向队列)
  - 头指针单向链表 LinkedListV1 (可用于实现栈)
  - 头尾指针单向链表 LinkedListV2 (可用于实现栈, 队列)
  - 二分搜索树 BST (可用于实现集合, 字典)
  - 最大堆 MaxHeap (可用于实现优先级队列)
  - 线段树 SegmentTree
  - 字典树 Trie
  - 并查集 UnionFindV2
  - AVL 树 AVL (可用于实现集合, 字典)
  - 哈希表 HashTable (可用于实现集合, 字典)

### 相关练习题

链表:
  - LeetCode 92, 翻转链表. 这是一道纯链表操作的题目.

哈希表:
  - LeetCode 387, 寻找第一个只出现一次的字符. 这是一道帮助理解哈希函数的题目.

TODO:
  - 实现开放地址法的哈希表, 
    [原理说明](https://www.geeksforgeeks.org/hashing-set-3-open-addressing/), 
    [参考实现](https://gist.github.com/EntilZha/5397c02dc6be389c85d8)
