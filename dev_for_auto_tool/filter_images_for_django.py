from torchvision import models
from torchvision import transforms
from torch.utils import data
from PIL import Image
import torch
import os
import argparse
import json
import time
import datetime
from shutil import copyfile
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageFolder(data.Dataset):
    def __init__(self, root, transform=None):
        self.filenames = os.listdir(root)
        self.filenames.sort()
        self.image_paths = [os.path.join(root, filename) for filename in self.filenames]
        self.transform = transform

    def __getitem__(self, index):
        image_path = self.image_paths[index]
        image = Image.open(image_path).convert('RGB')
        if self.transform is not None:
            image = self.transform(image)
        return image

    def __len__(self):
        return len(self.image_paths)


def filter(keyword, save_dir):
    # device setting
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # imagenet class index.json path
    class_idx_path = '/Users/user/Downloads/imagenet/imagenet_class_index.json'
    source_image_dir = '/Users/user/Downloads/Google_crawling/unfiltered/' + save_dir
    target_image_dir = '/Users/user/Downloads/Google_crawling/filtered/' + save_dir
    # target_class = keyword

    topk = 5

    # Imagenet class indices
    json_data = open(class_idx_path).read()
    class_idx2name = json.loads(json_data)
    image_size = 224

    class2idx = {}  # class name to class index (0~1000)
    idx2class = {}  # class index to class name (e.g., tiger)
    for idx, (_, class_name) in class_idx2name.items():
        idx = int(idx)
        class_name = class_name.lower()
        class2idx[class_name] = idx
        idx2class[idx] = class_name

    # Dataset
    transform = transforms.Compose([
        transforms.Resize([image_size, image_size]),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.485, 0.456, 0.406),
                             std=(0.229, 0.224, 0.225))
    ])

    dataset = ImageFolder(source_image_dir, transform=transform)

    if not os.path.exists(target_image_dir):
        os.makedirs(target_image_dir)

    # Data loader
    data_loader = data.DataLoader(dataset=dataset,
                                  batch_size=32,
                                  shuffle=False,
                                  num_workers=2)

    # Model
    resnet = models.resnet18(pretrained=True).to(device)
    resnet = resnet.eval()

    print('Start filtering images..!')

    target_idx = class2idx[keyword.lower()]
    is_target = []
    start_time = time.time()
    with torch.no_grad():
        for i, images in enumerate(data_loader):
            images = images.to(device)
            logits = resnet(images)

            # top 5 select
            _, top_k = logits.topk(k=topk, dim=1)  # (batch_size, topk)
            tmp_target_idx = torch.zeros_like(top_k).fill_(target_idx)
            is_target.append(torch.sum(top_k == tmp_target_idx, dim=1))  # (batch_size)

            et = time.time() - start_time
            et = str(datetime.timedelta(seconds=et))[:-7]
            if (i + 1) % 10 == 0:
                print('Elapsed time: {}, Filtered images: {}'.format(et, (i + 1) * 32))

        is_target = torch.cat(is_target, dim=0)  # binary vectors of shape (num_images)

        for i, filename in enumerate(dataset.filenames):
            # if the model classified an image to the target class, save the image.
            if is_target[i].item() == 1:
                source_path = os.path.join(source_image_dir, filename)
                target_path = os.path.join(target_image_dir, filename)
                copyfile(source_path, target_path)

            et = time.time() - start_time
            et = str(datetime.timedelta(seconds=et))[:-7]
            if (i + 1) % 1000 == 0:
                print('Elapsed time: {}, saved images: {}'.format(et, i + 1))

    print('Finished filtering images..!')

keyword = 'angora'
save_dir = '강호동_필터링테스트_angora'
filter(keyword, save_dir)