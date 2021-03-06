This is Asset pricing estimation homework
"""
import statsmodels.api as sm
import numpy as np
import pandas as pd
from scipy.stats import f
ff3 = pd.read_excel('code/data1.xlsx',"Sheet3")
p25=pd.read_excel('code/data1.xlsx','Sheet1')
m10=pd.read_excel('code/data1.xlsx','Sheet2')
rev_m10 = pd.read_excel()

#%%
rf=ff3.RF/100
ff3=ff3.iloc[:,[0,1,2]]/100
p25=(p25/100).sub(rf,axis=0)
m10=(m10/100).sub(rf,axis=0)

ff3.index= pd.to_datetime(ff3.index, yearfirst=True, format='%Y%m')
p25.index= pd.to_datetime(p25.index, yearfirst=True, format='%Y%m')
m10.index= pd.to_datetime(m10.index, yearfirst=True, format='%Y%m')
#%%
class famafrench(object):
    """
    fama french class
    attributes are X and y variables
    
    methods: regression
    """
    def __init__(self, y=p25, start='1963-7',end='2017-12'):
        self.start = start
        self.end = end
        self.y = y[start:end]
        
    def __str__(self):
        return 'from %s to %s' %(self.start, self.end)
    
    def variables(self):
        X = ff3[self.start:self.end]
        Y = self.y[self.start:self.end]
        return Y,X
    
    def regression(self):
        X = self.variables()[1]
        X = sm.add_constant(X)
        Y = self.variables()[0]
        model = sm.OLS(Y,X)
        results = model.fit()
        return results
    
    def regression_r2(self):
        r2_list= []
        for i in self.variables()[0].columns:
            X = self.variables()[1]
            X = sm.add_constant(X)
            Y = self.variables()[0][i]
            model = sm.OLS(Y,X)
            results = model.fit()
            r2_list.append(results.rsquared)
        return r2_list
    
    def GRS_test(self):
        n = len(self.y.columns)
        const = (414-n-3)/n
        
        res_cov = self.regression().resid.cov().values
        inv_res_cov = np.linalg.pinv(res_cov)
        ahat = self.regression().params.loc['const'].values
        num = np.matmul(np.matmul(ahat,inv_res_cov),ahat.T)
        
        E_f = ff3.mean().values
        cov_fact = ff3.cov()
        inv_cov_fact = np.linalg.pinv(cov_fact)
        denom = 1 + np.matmul(np.matmul(E_f, inv_cov_fact),E_f.T)
         
        GRS = const * (num / denom)
        rv = f(n,414-n-3)
        p_GRS = rv.cdf(GRS)
        return GRS, p_GRS
    
