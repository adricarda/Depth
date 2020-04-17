import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

# class BerHu(nn.Module):
#     def __init__(self, meter_threshold=100, error_threshold=0.2):
#         super(BerHu, self).__init__()
#         self.error_threshold = error_threshold
#         self.meter_threshold = meter_threshold
    
#     def forward(self, prediction, target):
#         prediction = prediction.squeeze()
#         mask = target>0
#         target[target>self.meter_threshold] = self.meter_threshold
#         target /= self.meter_threshold

#         print(prediction.max())
#         print(target.max())

#         print(prediction.min())
#         print(target.min())

#         prediction = prediction * mask
#         target = target * mask

#         diff = torch.abs(target-prediction)
#         delta = self.error_threshold * torch.max(diff).item()

#         part1 = -F.threshold(-diff, -delta, 0.)
#         part2 = F.threshold(diff**2 - delta**2, 0., -delta**2.) + delta**2
#         part2 = part2 / (2.*delta)

#         loss = part1 + part2
#         loss = torch.sum(loss)
#         return loss

class Masked_L1_loss(nn.Module):
    def __init__(self, threshold=100, **kwargs):
        self.threshold = threshold
        self.e = 1e-10
        super().__init__(**kwargs)
        
    def forward(self, prediction, target):
        gt = target.clone()
        prediction = prediction.squeeze()
        valid_map = gt>0
        gt[gt>self.threshold] = self.threshold
        gt /= self.threshold
        error = torch.abs(gt[valid_map]-prediction[valid_map])/torch.sum(valid_map)
        return torch.sum(error)

def get_loss_fn(loss_name='crossentropy', **kwargs):

    if loss_name=='crossentropy':
        return nn.CrossEntropyLoss(**kwargs)
    if loss_name=='beruh':
        return BerHu(**kwargs)
    if loss_name=='l1':
        return Masked_L1_loss(**kwargs)    
    else:
        return nn.CrossEntropyLoss(**kwargs)