import pandas as pd
# from pandas import Series, DataFrame
from scipy.stats import norm


def classification(file_name, k, x):
    df = pd.read_csv(file_name, header=-1)
    total_size = len(df)

    pcx_list = []
    pxc_pc_list = []
    sum_pxc_pc = 0.0

    for i in range(k):

        sample = df.loc[df[1] == i]

        mean = sample.mean()[0]

        sigma = sample.std(ddof=0)[0]

        pxc = norm.pdf(x, mean, sigma)

        sample_size = len(sample)
        pc = sample_size / total_size

        pxc_pc = pc * pxc

        sum_pxc_pc += pxc_pc

        pxc_pc_list.append(pxc_pc)

        for pxc_pc_i in pxc_pc_list:
            pcx = pxc_pc_i / sum_pxc_pc
            pcx_list.append(pcx)

    return pcx_list.index(max(pcx_list))
