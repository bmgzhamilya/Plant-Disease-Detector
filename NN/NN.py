from NN.NN_info import *
from config import *
from collections import Counter
import math

def get_image_disease(filename):
    trains = train

    images_folder = path_to_directory + "static/Images/"
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
    
    response = disease_response("IMAGE", [result], [description], []) 
    
    return response

def split_video_to_frames(video_file_path, frames_folder):
      # Создаем папку, если она не существует
  if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)

  # Открываем видеофайл
  video_capture = cv2.VideoCapture(video_file_path)

  # Нумеруем кадры с нуля
  frame_number = 0

  # Пока есть кадры в видео
  while True:
    # Читаем очередной кадр
    success, frame = video_capture.read()

    # Если кадр не удалось прочитать (конец видео)
    if not success:
      break

    # Формируем имя файла для текущего кадра
    frame_file_name = f'frame{frame_number:06d}.jpg'
    frame_file_path = os.path.join(frames_folder, frame_file_name)

    # Сохраняем кадр в файл
    cv2.imwrite(frame_file_path, frame)

    # Увеличиваем номер кадра
    frame_number += 1

  # Закрываем видеофайл
  video_capture.release()

def get_video_disease(filename):
    split_video_to_frames(path_to_directory + '/static/Videos/' + filename, path_to_directory + "/static/Images/Uploads")
    trains = train

    images_folder = path_to_directory + "static/Images/"
    
    train_transform = transforms.Compose([
        transforms.ToTensor()
    ])
    train1 = ImageFolder(path_to_directory + "static/Images", transform=train_transform)
    min_size = min(train1[0][0].shape[1:3])
    print(min_size)
    train_transform = transforms.Compose([
        transforms.CenterCrop(min_size),
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

    items = []
    video_results = []
    for i in range(len(images)):
        img, _ = images[i]
        img = transformer(img)
        result, description = predict_image(img, model)
        video_results.append(str(math.floor(i/60)) + ":" + str(round(i%60)) +" - " + result)
        items.append(result)
        #show_image(img, result)
    response = disease_response("VIDEO", video_results, ["hello"], Counter(items).most_common())     
    
    return response
    #print(description)
    #print('Label:', filename, ', Predicted:', result)