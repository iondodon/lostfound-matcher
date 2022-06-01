import os
from PIL import Image
from torchvision import transforms
from numpy.testing import assert_almost_equal
import pickle
import torch
from tqdm import tqdm
from torchvision import models
import pandas as pd
import numpy as np
from urllib.request import urlopen
from io import BytesIO
from PIL import Image
import numpy as np


# needed input dimensions for the CNN
inputDim = (224,224)
inputDir = "./image_processing/originalImages"
inputDirCNN = "./image_processing/inputImagesCNN"

os.makedirs(inputDirCNN, exist_ok = True)

transformationForCNNInput = transforms.Compose([transforms.Resize(inputDim)])

# for this prototype we use no gpu, cuda= False and as model resnet18 to obtain feature vectors

class Img2VecResnet18():
    def __init__(self):
        
        self.device = torch.device("cpu")
        self.numberFeatures = 512
        self.modelName = "resnet-18"
        self.model, self.featureLayer = self.getFeatureLayer()
        self.model = self.model.to(self.device)
        self.model.eval()
        self.toTensor = transforms.ToTensor()
        
        # normalize the resized images as expected by resnet18
        # [0.485, 0.456, 0.406] --> normalized mean value of ImageNet, [0.229, 0.224, 0.225] std of ImageNet
        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        
    def getVec(self, img):
        image = self.normalize(self.toTensor(img)).unsqueeze(0).to(self.device)
        embedding = torch.zeros(1, self.numberFeatures, 1, 1)

        def copyData(m, i, o): embedding.copy_(o.data)

        h = self.featureLayer.register_forward_hook(copyData)
        self.model(image)
        h.remove()

        return embedding.numpy()[0, :, 0, 0]

    def getFeatureLayer(self):
        
        cnnModel = models.resnet18(pretrained=True)
        layer = cnnModel._modules.get('avgpool')
        self.layer_output_size = 512
        
        return cnnModel, layer


def getSimilarityMatrix(vectors):
    v = np.array(list(vectors.values())).T
    sim = np.inner(v.T, v.T) / ((np.linalg.norm(v, axis=0).reshape(-1,1)) * ((np.linalg.norm(v, axis=0).reshape(-1,1)).T))
    keys = list(vectors.keys())
    matrix = pd.DataFrame(sim, columns = keys, index = keys)
    
    return matrix


# get image from URL
def get_image_from_URL(url):
    response = urlopen(url)
    image = Image.open(BytesIO(response.read()))
    image = np.array(image)

    # convert to Image object
    image = Image.fromarray(image)
    
    return image


list_of_image_urls = [
    "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
    "https://arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/WALN4MAIT4I6VLRIPUMJQAJIME.jpg"
]


# save the images to the originalImages folder
for url in list_of_image_urls:
    image = get_image_from_URL(url)

    image.save(os.path.join(inputDir, url.split('/')[-1]))



for imageName in os.listdir(inputDir):
    I = Image.open(os.path.join(inputDir, imageName)).convert('RGB')
    newI = transformationForCNNInput(I)

    newI.save(os.path.join(inputDirCNN, imageName))
    
    newI.close()
    I.close()



# generate vectors for all the images in the set
img2vec = Img2VecResnet18() 

allVectors = {}
print("Converting images to feature vectors:")
for image in tqdm(os.listdir(inputDirCNN)):
    I = Image.open(os.path.join(inputDirCNN, image)).convert('RGB')
    vec = img2vec.getVec(I)
    allVectors[image] = vec
    I.close()

        
similarityMatrix = getSimilarityMatrix(allVectors)

k = 2 # the number of top similar images to be stored

similarNames = pd.DataFrame(index = similarityMatrix.index, columns = range(k))
similarValues = pd.DataFrame(index = similarityMatrix.index, columns = range(k))

for j in tqdm(range(similarityMatrix.shape[0])):
    kSimilar = similarityMatrix.iloc[j, :].sort_values(ascending = False).head(k)
    similarNames.iloc[j, :] = list(kSimilar.index)
    similarValues.iloc[j, :] = kSimilar.values
    
# similarNames.to_pickle("similarNames.pkl")
# similarValues.to_pickle("similarValues.pkl")

# print(similarNames, similarValues)

print("The similarity percentage is: {}".format(similarValues.iloc[0,1]))