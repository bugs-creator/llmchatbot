# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def Interleaving():
    index_list = []
    for i in total_engine:
        index_list.append(0)
    indexA = 0
    indexB = 0
    indexC = 0
    fused = []
    n = 0
    while n < unique_len:
        for i in range(len(total_engine)):
            if index_list[i] < len(total_engine[i]):
                while total_engine[i][index_list[i]] in fused:
                    index_list[i] += 1
                    if index_list[i] >= len(total_engine[i]):
                        break
                if index_list[i] < len(total_engine[i]):
                    fused.append(total_engine[i][index_list[i]])
                    index_list[i] +=1
                    n+=1
        # if indexA < len(engine_A):
        #     while engine_A[indexA] in fused:
        #         indexA+=1
        #         if indexA >= len(engine_A):
        #             break
        #     if indexA >= len(engine_A):
        #         pass
        #     else:
        #         fused.append(engine_A[indexA])
        #         indexA+=1
        #         i+=1
        # if indexB < len(engine_B):
        #     while engine_B[indexB] in fused:
        #         indexB+=1
        #         if indexB >= len(engine_B):
        #             break
        #     if indexB >= len(engine_B):
        #         pass
        #     else:
        #         fused.append(engine_B[indexB])
        #         indexB+=1
        #         i+=1
        # if indexC < len(engine_C):
        #     while engine_C[indexC] in fused:
        #         indexC+=1
        #         if indexC >= len(engine_C):
        #             break
        #     if indexC >= len(engine_C):
        #         pass
        #     else:
        #         fused.append(engine_C[indexC])
        #         indexC+=1
        #         i+=1
    i = 0
    # while i < unique_len:
    #     if indexA < len(engine_A):
    #         if engine_A[indexA] not in fused:
    #             fused.append(engine_A[indexA])
    #             i+=1
    #             indexA+=1
    #         else:
    #             while engine_A[indexA] in fused:
    #                 indexA+=1
    #                 if indexA >= len(engine_A):
    #                     break
    #             if indexA >= len(engine_A):
    #                 continue
    #             else:
    #                 fused.append(engine_A[indexA])
    #                 indexA+=1
    #     if indexB < len(engine_B):
    #         if engine_B[indexB] not in fused:
    #             fused.append(engine_B[indexB])
    #             i+=1
    #             indexB+= 1
    #         else:
    #             while engine_B[indexB] in fused:
    #                 indexB+=1
    #                 if indexB >= len(engine_B):
    #                     break
    #             if indexB >= len(engine_B):
    #                     continue
    #             else:
    #                 fused.append(engine_B[indexB])
    #                 indexB+=10
    #                 i+=1
    #     if indexC < len(engine_C):
    #         if engine_C[indexC] not in fused:
    #             fused.append(engine_C[indexC])
    #             i += 1
    #             indexC += 1
    #         else:
    #             while engine_C[indexC] in fused:
    #                 indexC+=1
    #                 if indexC >= len(engine_C):
    #                     break
    #             if indexC >= len(engine_C):
    #                     continue
    #             else:
    #                 fused.append(engine_C[indexC])
    #                 indexC+=1
    #                 i+=1
    return fused
# Press the green button in the gutter to run the script.
def BordaFuse():
    no_choose_list = []
    vote_dict_list = []
    for i in total_engine:
        no_choose_list.append(sum(range(1,unique_len-len(i)+1))/(unique_len-len(i)))
        vote_dict = {}
        for n in range(len(i)):
            vote_dict[i[n]] = unique_len - n
        vote_dict_list.append(vote_dict)
    # noChooseA = sum(range(1,unique_len-len(engine_A)+1))/(unique_len-len(engine_A))
    # noChooseB = sum(range(1,unique_len-len(engine_B)+1))/(unique_len-len(engine_B))
    # noChooseC = sum(range(1,unique_len-len(engine_C)+1))/(unique_len-len(engine_C))
    #
    # vote_dict_A = dict()
    # vote_dict_B = dict()
    # vote_dict_C = dict()
    #
    # for i in range(len(engine_A)):
    #     vote_dict_A[engine_A[i]] = unique_len - i
    # for i in range(len(engine_B)):
    #     vote_dict_B[engine_B[i]] = unique_len - i
    fuse = dict()
    for i in set_union:
        scorei= 0
        for n in range(len(vote_dict_list)):
            if i in vote_dict_list[n]:
                scorei+=vote_dict_list[n][i]
            else:
                scorei+=no_choose_list[n]
        fuse[i] = scorei
    return sorted(fuse.items(), key=lambda x: x[1],reverse=True)

def RRF():
    fused = dict()

    for i in set_union:
        scorei = 0
        for engine in total_engine:
            if i in engine:
                rank = engine.index(i)+1
                scorei+=i/(60+rank)

        fused[i] = scorei

    return sorted(fused.items(), key=lambda x: x[1],reverse=True)


def score_Normalisation(engine_dict):
    sorted_engine = sorted(engine_dict.items(), key=lambda x: x[1],reverse=True)
    max_score = sorted_engine[0][1]
    min_score = sorted_engine[-1][1]
    norm_dict = dict()
    for k,v in engine_dict.items():
        norm_dict[k] = (v - min_score)/(max_score-min_score)
    return norm_dict

def comb_sum():
    fused = dict()
    for i in set_dict_union:
        scorei = 0
        for norm_dict in norm_total_dict:
            if i in norm_dict:
                scorei+=norm_dict[i]
        fused[i] = scorei
    return sorted(fused.items(), key=lambda x: x[1],reverse=True)

def comb_mnz():
    fused = dict()
    for i in set_dict_union:
        scorei = 0
        apper_times = 0
        for norm_dict in norm_total_dict:
            if i in norm_dict:
                scorei+=norm_dict[i]
                apper_times+=1
        fused[i] = scorei * apper_times
    return sorted(fused.items(), key=lambda x: x[1],reverse=True)

if __name__ == '__main__':
    # engine_A = [10,18,4,6,5,17,11,14]
    # engine_B = [18,6,1,2,17]
    engine_A = [13,7,15,2,5,1,0,3,4]
    # engine_C = [6,4,3,18,5,10,15,19]
    engine_B = [6,9,15,12,5,14,13]
    engine_C= [3,8,6,0,9,5,7,4,14,11]
    total_engine = [engine_A,engine_B,engine_C]
    set_union = set()
    for i in total_engine:
        set_union = set_union.union(set(i))
    unique_len = len(set_union)
    # engineA_dict = {
    #     '10':0.82,
    #     '9':0.57,
    #     '12':0.48,
    #     '11':0.46,
    #     '8':0.41,
    #     '1':0.37,
    #     '6':0.26,
    #     '7':0.19
    # }
    #
    # engineB_dict = {
    #     '5': 947,
    #     '1': 936,
    #     '11': 860,
    #     '2': 516,
    #     '8': 414,
    #     '6': 300,
    #     '4': 153,
    #     '10': 26
    # }
    # engineC_dict = {
    #     '12': 9.93,
    #     '1': 9.00,
    #     '2': 7.88,
    #     '6': 6.69,
    #     '7': 5.03,
    #     '8': 4.22,
    #     '5': 3.63,
    #     '3': 0.76
    # }


    engineA_dict = {
        '1':0.9595,
        '12':0.4709,
        '10':0.3829,
        '9':	0.3384,
        '14':0.2777,
        '11':0.1164,
        '4':0.0806,

    }
    engineB_dict = {
        '1': 977.5494,
        '3': 667.1508,
        '0': 605.9753,
        '15': 377.0779,
        '13': 343.3506,
        '14': 316.1724,
        '8': 290.6457,
        '12': 179.1258,
        '11': 171.0962,
        '6': 1.5012
    }
    engineC_dict = {
        '4': 093.7531,
        '8':80.7096,
        '10':77.2629,
        '5':58.2031,
        '14': 53.4187,
        '2': 45.0629,
        '15': 32.1298,
        '1':26.5387,
        '12':8.1426


    }
    total_dict = [engineA_dict,engineB_dict,engineC_dict]
    norm_total_dict = []
    set_dict_union = set()
    for i in total_dict:
        norm_total_dict.append(score_Normalisation(i))
        set_dict_union = set_dict_union.union(i.keys())
    print('Interleaving',Interleaving())
    print('BoradFuse',BordaFuse())
    print('RRF',RRF())
    print('combSUM',comb_sum())
    print('combMNZ',comb_mnz())

    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
