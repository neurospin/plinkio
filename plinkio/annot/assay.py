# -*- coding: utf-8 -*-

import numpy as np

plinkAssayDict = {}
plinkAssayDict['FID'] = 0
plinkAssayDict['IID'] = 1
plinkAssayDict['GENDER'] = 4

plinkAssayFormatDict = {}
#plinkAssayFormatDict['FID'] = '%04d'
plinkAssayFormatDict['FID'] = '%s'
plinkAssayFormatDict['IID'] = '%012d'
plinkAssayFormatDict['GENDER'] = '%1d'

encodeSnpMatrix = np.array([0, 128, 1, 2], dtype=np.uint8)
encodeMinAllCount = np.array([2, 128, 1, 0], dtype=np.uint8)
