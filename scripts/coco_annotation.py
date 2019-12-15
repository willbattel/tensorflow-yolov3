import os
import argparse
from PIL import Image

def convert_coco_annotation(data_path, data_type, out_path):
    image_list_path = os.path.join(data_path, data_type + '.txt')
    with open(image_list_path, 'r') as f:
        lines = f.readlines()
        image_list = [line.strip() for line in lines]

    count = 0
    with open(out_path, 'a') as out_file:
        for image_path in image_list:
            image = Image.open(image_path)
            image_width, image_height = image.size
            annotation = image_path
            label_list_path = image_path.replace("images", "labels").replace("jpg", "txt")
            try:
                with open(label_list_path, 'r') as f:
                    lines = f.readlines()
                    label_list = [line.strip() for line in lines]
                    for label in label_list:
                        components = label.split(" ")
                        # components[0] = class index
                        # components[1] = box center x, normalized
                        # components[2] = box center y, normalized
                        # components[3] = box width, normalized
                        # components[4] = box height, normalized

                        class_index = components[0]
                        x_min = (float(components[1]) - (float(components[3]) * 0.5)) * float(image_width)
                        y_min = (float(components[2]) - (float(components[4]) * 0.5)) * float(image_height)
                        x_max = x_min + (float(components[3]) * float(image_width))
                        y_max = y_min + (float(components[4]) * float(image_height))

                        class_index_str = str(class_index)
                        x_min_str = str(int(round(x_min)))
                        y_min_str = str(int(round(y_min)))
                        x_max_str = str(int(round(x_max)))
                        y_max_str = str(int(round(y_max)))
                        annotation += ' ' + ','.join([x_min_str, y_min_str, x_max_str, y_max_str, class_index_str])
            except FileNotFoundError:
                continue
            count += 1
            print(annotation)
            out_file.write(annotation + "\n")
    return count

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default="/Users/wbattel/Desktop/com/sentryware/tensorflow-yolov3/data/coco")
    parser.add_argument("--train_annotation", default="./data/coco/coco_train.txt")
    parser.add_argument("--test_annotation",  default="./data/coco/coco_test.txt")
    flags = parser.parse_args()

    if os.path.exists(flags.train_annotation):os.remove(flags.train_annotation)
    if os.path.exists(flags.test_annotation):os.remove(flags.test_annotation)

    num_trainvalno5k = convert_coco_annotation(flags.data_path, 'trainvalno5k', flags.train_annotation)
    num_5k = convert_coco_annotation(flags.data_path, '5k', flags.test_annotation)
    print('=> The number of image for train is: %d\tThe number of image for test is: %d' %(num_trainvalno5k, num_5k))


