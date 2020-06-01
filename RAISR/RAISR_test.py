import cv2
import numpy as np
import os
import pickle
from RAISR.hashkey import hashkey
from math import floor
from scipy import interpolate
from RAISR.utils import gaussian2d
import io
import discord

cwd = os.getcwd()

R = 2
patchsize = 11
gradientsize = 9
Qangle = 24
Qstrength = 3
Qcoherence = 3

maxblocksize = max(patchsize, gradientsize)
margin = floor(maxblocksize / 2)
patchmargin = floor(patchsize / 2)
gradientmargin = floor(gradientsize / 2)

with open(cwd + '/RAISR/model/filter' + str(R) + 'x', 'rb') as fp:
    h = pickle.load(fp)

weighting = gaussian2d([gradientsize, gradientsize], 2)
weighting = np.diag(weighting.ravel())


async def RAISR_Test(file_Name, file_Buffer, msg):
    print('\rUpscaling image ' + file_Name)
    origin = cv2.imdecode(file_Buffer, cv2.IMREAD_COLOR)

    ycrcvorigin = cv2.cvtColor(origin, cv2.COLOR_BGR2YCrCb)
    grayorigin = ycrcvorigin[:, :, 0]

    grayorigin = cv2.normalize(grayorigin.astype(
        'float'), None, grayorigin.min() / 255, grayorigin.max() / 255, cv2.NORM_MINMAX)

    heightLR, widthLR = grayorigin.shape
    heightgridLR = np.linspace(0, heightLR - 1, heightLR)
    widthgridLR = np.linspace(0, widthLR - 1, widthLR)
    bilinearinterp = interpolate.interp2d(
        widthgridLR, heightgridLR, grayorigin, kind='linear')
    heightgridHR = np.linspace(0, heightLR - 0.5, heightLR * 2)
    widthgridHR = np.linspace(0, widthLR - 0.5, widthLR * 2)
    upscaledLR = bilinearinterp(widthgridHR, heightgridHR)

    heightHR, widthHR = upscaledLR.shape
    predictHR = np.zeros((heightHR - 2 * margin, widthHR - 2 * margin))
    totaloperations = (heightHR - 2 * margin) * (widthHR - 2 * margin)
    for row in range(margin, heightHR - margin):
        for col in range(margin, widthHR - margin):
            patch = upscaledLR[row - patchmargin:row +
                               patchmargin + 1, col - patchmargin:col + patchmargin + 1]
            patch = patch.ravel()

            gradientblock = upscaledLR[row - gradientmargin:row +
                                       gradientmargin + 1, col - gradientmargin:col + gradientmargin + 1]

            angle, strength, coherence = hashkey(
                gradientblock, Qangle, weighting)

            pixeltype = ((row - margin) % R) * R + ((col - margin) % R)
            predictHR[row - margin, col -
                      margin] = patch.dot(h[angle, strength, coherence, pixeltype])

    predictHR = np.clip(predictHR.astype('float') * 255., 0., 255.)
    result = np.zeros((heightHR, widthHR, 3))
    y = ycrcvorigin[:, :, 0]
    bilinearinterp = interpolate.interp2d(
        widthgridLR, heightgridLR, y, kind='linear')
    result[:, :, 0] = bilinearinterp(widthgridHR, heightgridHR)
    cr = ycrcvorigin[:, :, 1]
    bilinearinterp = interpolate.interp2d(
        widthgridLR, heightgridLR, cr, kind='linear')
    result[:, :, 1] = bilinearinterp(widthgridHR, heightgridHR)
    cv = ycrcvorigin[:, :, 2]
    bilinearinterp = interpolate.interp2d(
        widthgridLR, heightgridLR, cv, kind='linear')
    result[:, :, 2] = bilinearinterp(widthgridHR, heightgridHR)
    result[margin:heightHR - margin, margin:widthHR - margin, 0] = predictHR
    result = cv2.cvtColor(cv2.cvtColor(
        np.uint8(result), cv2.COLOR_YCrCb2RGB), cv2.COLOR_RGB2BGR)

    _, buffer = cv2.imencode(file_Name, result)
    data = io.BytesIO(buffer)
    await msg.channel.send(file=discord.File(data, file_Name))
    print(file_Name + ' Finished.')
