# 已知DNA中存在A、C、G、T这四种碱基，基因突变可能发生以下事件1.
# 输入描述输入一个整数a表示测试的行数,每行为两段基因片段,以空格隔开,每个片段最长不超过100字符
# 输出描述输出最少变异数,如果基因相同.则输出0

def min_mutation(dna):
    # 假设碱基只有A、C、G、T四种
    mutation_dict = {'A': 'CGT', 'C': 'AGT', 'G': 'ACT', 'T': 'ACG'}

    # 初始化队列，将输入的DNA片段加入队列
    queue = [dna]

    # 初始化已访问的DNA片段集合
    visited = set(dna)

    # 初始化变异次数
    mutations = 0

    while queue:
        # 每次从队列中取出一个DNA片段
        current_dna = queue.pop(0)

        # 遍历当前DNA片段的每个位置
        for i in range(len(current_dna)):
            # 遍历当前碱基可以变异成的碱基
            for mutation in mutation_dict[current_dna[i]]:
                # 构建新的DNA片段
                new_dna = current_dna[:i] + mutation + current_dna[i + 1:]

                # 如果新的DNA片段不在已visited中，则将其加入队列，并标记为已访问
                if new_dna not in visited:
                    queue.append(new_dna)
                    visited.add(new_dna)

                    # 如果新的DNA片段与输入的DNA片段相同，则返回变异次数
                    if new_dna == dna:
                        return mutations + 1

                    # 如果新的DNA片段与输入的DNA片段不同，则继续变异
                    mutations += 1

    # 如果队列中没有找到与输入的DNA片段相同的DNA片段，则返回-1
    return -1


# 测试
dna = input("请输入DNA片段：")
result = min_mutation(dna)
print("最少变异数为：", result)

# 示例
# 输入：AACCGGTT
# 输出：2
