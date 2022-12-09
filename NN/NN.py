from NN.NN_info import *


def get_image_disease(filename):
    trains = train

    images_folder = "/opt/site/static/"
    train_transform = transforms.Compose([
        transforms.Resize((256,256)),
        transforms.ToTensor()
    ])
    images = ImageFolder(images_folder, train_transform)

    PATH = 'models/plant-disease-model.pth'
    device = torch.device("cpu")

    model = to_device(ResNet9(3, len(trains.classes)), device)
    model.load_state_dict(torch.load(PATH, map_location=torch.device('cpu')))
    model.eval()

    transformer = transforms.Resize(256)

    img, _ = images[-1]
    img = transformer(img)
    result, description = predict_image(img, model)
    print(description)
    print('Label:', filename, ', Predicted:', result)
    return (result, description)
