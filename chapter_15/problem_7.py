from __future__ import print_function
import os, sys
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats, linalg
from scipy.stats import multivariate_normal
from problem_5 import multivar_normal


def main(arguments):

    mean = np.array([0,2])
    cov  = np.matrix('3 1;1 3') #NOTE: BOOK HAS ERROR IN COV MATRIX
    observations = 100
    # 1) Generate 100 random vectors from multivar normal
    samples = multivar_normal(mean,cov,observations)

    # 2) Find true correlation (we have exact parameters from generating normal)
    #    Find plug in estimator for correlation
    #    Find 95 % CI (boostrap and fischer methods)
    sample_mean = np.mean(samples,axis=0)
    sample_cov  = np.cov(np.transpose(samples))
    sample_corr = np.corrcoef(np.transpose(samples))[0][1]
    #print('sample_mean'); print(sample_mean)
    #print('sample_cov'); print(sample_cov)
    print('sample_corr: {0:f}'.format(sample_corr))
    #true correlation: r = 1/3

    #Bootstraping
    B = 10000
    boot_est = np.zeros(B)
    for i in range(B):
        # sampling rows = data points
        idx          = np.random.choice(samples.shape[0], samples.shape[0])
        boot_samples = samples[idx, :]
        boot_est[i]     = np.corrcoef(np.transpose(boot_samples))[0][1]
    se_boot = np.std(boot_est)


    #Fischer magic
    theta_hat = (1/2)*(np.log(1+sample_corr) - np.log(1-sample_corr))
    se_fisc   = 1/np.sqrt(observations-3)
    a         = theta_hat - 1.96*se_fisc
    b         = theta_hat + 1.96*se_fisc
    l_corr    = (np.exp(2*a) - 1)/(np.exp(2*a) + 1)
    r_corr    = (np.exp(2*b) - 1)/(np.exp(2*b) + 1)

    print('95% CI via Boot   : {0:f}, {1:f}'.format(sample_corr-1.96*se_boot, sample_corr+1.96*se_boot))
    print('95% CI via Fischer: {0:f}, {1:f}'.format(l_corr,r_corr))

    #Display CI for correlation
    if(True):
        bins =  np.linspace(np.amin(boot_est), np.amax(boot_est),50)
        plt.hist(boot_est,bins=bins)
        plt.axvline(x=sample_corr-1.96*se_boot); plt.axvline(x=sample_corr+1.96*se_boot)
        plt.axvline(x=l_corr, color='red'); plt.axvline(x=r_corr, color='red')
        plt.axvline(x=sample_corr, color='black')
        plt.show()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
