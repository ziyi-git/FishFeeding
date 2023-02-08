import torch
import numpy
import PIL
import PIL.Image
import time
import argparse

from liteflownet import estimate

arguments_strModel = 'default' # 'default', or 'kitti', or 'sintel'
arguments_strOne = '/data/Workspace/FishFeedingAnalysis/liteflownet/images/one.png'
arguments_strTwo = '/data/Workspace/FishFeedingAnalysis/liteflownet/images/two.png'
arguments_strOut = './out.flo'

if __name__ == '__main__':
    tenOne = torch.FloatTensor(numpy.ascontiguousarray(numpy.array(PIL.Image.open(arguments_strOne))[:, :, ::-1].transpose(2, 0, 1).astype(numpy.float32) * (1.0 / 255.0)))
    tenTwo = torch.FloatTensor(numpy.ascontiguousarray(numpy.array(PIL.Image.open(arguments_strTwo))[:, :, ::-1].transpose(2, 0, 1).astype(numpy.float32) * (1.0 / 255.0)))

    model_time = time.time()
    tenOutput = estimate(tenOne, tenTwo)
    print("duration = {}".format(time.time() - model_time))

    model_time = time.time()
    tenOutput = estimate(tenOne, tenTwo)
    print("duration = {}".format(time.time() - model_time))

    model_time = time.time()
    tenOutput = estimate(tenOne, tenTwo)
    print("duration = {}".format(time.time() - model_time))

    model_time = time.time()
    tenOutput = estimate(tenOne, tenTwo)
    print("duration = {}".format(time.time() - model_time))
    print("tenOutput type: {}".format(tenOutput))
    
    # objOutput = open(arguments_strOut, 'wb')

    # numpy.array([ 80, 73, 69, 72 ], numpy.uint8).tofile(objOutput)
    # numpy.array([ tenOutput.shape[2], tenOutput.shape[1] ], numpy.int32).tofile(objOutput)
    # numpy.array(tenOutput.numpy().transpose(1, 2, 0), numpy.float32).tofile(objOutput)

    # objOutput.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help="restore checkpoint")
    parser.add_argument('--model_name', help="define model name", default="GMA")
    parser.add_argument('--path', help="dataset for evaluation")
    parser.add_argument('--num_heads', default=1, type=int,
                        help='number of heads in attention and aggregation')
    parser.add_argument('--position_only', default=False, action='store_true',
                        help='only use position-wise attention')
    parser.add_argument('--position_and_content', default=False, action='store_true',
                        help='use position and content-wise attention')
    parser.add_argument('--mixed_precision', action='store_true', help='use mixed precision')
    args = parser.parse_args()

    demo(args)