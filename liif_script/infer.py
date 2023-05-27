"""
This module contains the functionality to to infer new images using trained
Liif model. Is meant to be uses as an extra script for the git project
https://github.com/yinboc/liif.

:author: Ruben Moya Vazquez <rmoyav@uoc.edu>
:date: 27/05/2023
"""

import argparse
import os
from PIL import Image
import glob
import torch
from torchvision import transforms

import models
from utils import make_coord
from test import batched_predict

###############################################################################
#                                                                             #
#                                 FUNCTIONS                                   #
#                                                                             #
###############################################################################

def infer_images(input:str, output:str, model:str, gpu:str) -> None:
    """This function will take an input directory, an output directory,
    a trained liif model and a gpu id and will infer the input images
    into the output directory using the given model and CUDA gpu.

    Args:
        input (str): the input directory containing the base images
        output (str): the output directory to store the infered images
        model (str): the trained liif model checkpoint path
        gpu (str): the gpu to use
    """
    h = 256
    w = 256
    coord = make_coord((h, w)).cuda()
    use_model = models.make(torch.load(model)['model'], load_sd=True).cuda()
    cell = torch.ones_like(coord)
    cell[:, 0] *= 2 / h
    cell[:, 1] *= 2 / w
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu
    output_path = os.path.join(os.getcwd(), output)
    os.makedirs(output_path, exist_ok=True)
    if os.path.isdir(input):
        for input_img in glob.glob(os.path.join(input, '*.png')):
            file_name = os.path.splitext(os.path.basename(input_img))[0]
            img = transforms.ToTensor()(Image.open(input_img).convert('RGB'))
            pred = batched_predict(use_model, ((img - 0.5) / 0.5).cuda().unsqueeze(0),
                coord.unsqueeze(0), cell.unsqueeze(0), bsize=30000)[0]
            pred = (pred * 0.5 + 0.5).clamp(0, 1).view(h, w, 3).permute(2, 0, 1).cpu()
            transforms.ToPILImage()(pred).save(os.path.join(output_path, f"{file_name}_infered.png"))


###############################################################################
#                                                                             #
#                                   MAIN                                      #
#                                                                             #
###############################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='load\\test_64_256\\lr_64')
    parser.add_argument('--model')
    parser.add_argument('--output', default='output')
    parser.add_argument('--gpu', default='0')
    args = parser.parse_args()
    print("Infering new images...")
    infer_images(args.input, args.output, args.model, args.gpu)
    print("All images have been infered...")
   