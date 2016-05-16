DevTools Package Description
============================

The DevTools package is a simple set of tools for analyzing within
the [CMSSW framework](https://github.com/cms-sw/cmssw).

Installation
------------

Current CMSSW version ``CMSSW_8_0_8``.

```bash
cmsrel CMSSW_8_0_8
cd CMSSW_8_0_8/src
cmsenv
git cms-init
git clone --recursive git@github.com:dntaylor/DevTools.git -b 80X
./DevTools/recipe/recipe.sh
``` 
