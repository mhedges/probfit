# -*- coding: utf-8 -*-
# <nbformat>3</nbformat>

# <codecell>

from dist_fit import *
import numpy as np

# <codecell>

#it defines some c function(no python call)
#will wrap this one soon this shows the argument of the function
print crystalball.func_code.co_varnames[:crystalball.func_code.co_argcount]
vc = np.vectorize(crystalball)
x = linspace(-1,2,100)
plot(x,vc(x,1,1,1,1))
ylim(ymin=0)
#note that this is not normalized

# <codecell>

#automatic cache normalization of any distribution (for given range)
#you can skip this if your function is properly normalize
ncball = Normalize(crystalball,(-1,2))
print ncball(1.,1.,1.,1.,1.)

# <codecell>

print ncball.func_code.co_varnames[:ncball.func_code.co_argcount]
#and you can do toy generation from any distribution as well
#and compare the result for you
#if you are getting weird result from the fit make sure the normalization is the correct range
g = gen_toy(ncball,10000,(-1,2),alpha=1.,n=2.,mean=1.,sigma=1.,quiet=False)

# <codecell>

#yep it works
hist(g,bins=100,histtype='step');
#it's just a normal numpy array
print g

# <codecell>

#now you can fit
#takes argument like one in pyminuit
# give the named parameter to tell wheree to start
# and limit_name = tuple to tell it the range
uml,minu = fit_uml(ncball,g,alpha=1.,n=2.,mean=1.2,sigma=1.,
    limit_n=(1.,10.),limit_sigma=(0.01,3),limit_mean=(0.7,1),quiet=False)
uml.show(minu)
#see it works
#you can access it like a map
print minu.values

# <codecell>

#lets try a function that builtin one is not availble
#this is slow though you can speed this up by using cython but for most purpose this is fast "enough"
peak1 = randn(10000)
peak2 = randn(5000)+10
twopeak = np.append(peak1,peak2)
hist(twopeak,bins=100,histtype='step');

# <codecell>

#you can define you own funciton and use automatic normalization
#I know not all functions have analytic formula for normalization
@normalized_function(-20,20)
def tofit(x,m1,s1,m2,s2,a):
    g1 = gaussian(x,m1,s1)
    g2 = gaussian(x,m2,s2)
    ret = a*g1+(1-a)*g2
    return ret

# <codecell>

#see all good
uml, minu = fit_uml(tofit,twopeak,m1=0.,m2=10.,s1=2.,s2=2.,a=0.5)
uml.draw(minu)

# <codecell>

#now what if things doesn't fit
#it will throw error and plot what it have so far
#so give it a sensible starting point and limit
#these error include error matrix not accurate not positive definite edm problem and etc.
uml, minu = fit_uml(tofit,twopeak,m1=0.,m2=10.,s1=2.,s2=2.,a=3.)

# <codecell>

#chi2 fit is also there
#it will refuse to fit histogram with zero bin though
#it is meaning less to do that anyway

#Remember our ncball we can extend it
#this add N to the end of argument list (N is meaningful only when funciton is normalized)
encball = Extend(ncball)
print encball.func_code.co_varnames[:encball.func_code.co_argcount]

#and fit it with chi^2
uml,minu = fit_binx2(encball,g,alpha=1.,n=2.,mean=1.,sigma=1.,N=7000.,
    limit_n=(1.,10.),limit_sigma=(0.01,3),limit_mean=(0.7,1),quiet=False)
uml.show(minu)

# <codecell>

#you can try to get other information from minuit object
dir(minu)

# <codecell>

#there is also binned poisson
uml,minu = fit_binpoisson(encball,g,alpha=1.,n=2.,mean=1.,sigma=1.,N=7000.,
    limit_n=(1.,10.),limit_sigma=(0.01,3),limit_mean=(0.7,1),quiet=False)
uml.show(minu)

# <codecell>

#guessing initial parameter can be hard so I made these for you
try_uml(tofit,twopeak,m1=0.,m2=10.,s1=2.,s2=2.,a=0.1)

# <codecell>

#take list too so you can try a bunch of parameters at once
#it returns the best one
besttry = try_uml(tofit,twopeak,m1=0.,m2=10.,s1=1.,s2=1.,a=(0.4,0.5,0.7,0.9))
print besttry

# <codecell>

#a nice trick is to use keyword expansion on the return argument
uml,minu = fit_uml(tofit,twopeak,**besttry)
uml.show(minu)

# <codecell>

