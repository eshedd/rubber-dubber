from ultralytics import YOLO

CLASSES = ['green', 'red', 'yellow']
model = YOLO('weights/best.pt', type='v8')
results = model('img/test.jpg')[0]

lights = []
for pred in results:
    l, t, r, b, conf, label = pred
    midpt = tuple(map(int, ((r-l)/2+l, (b-t)/2+l)))
    lights.append([midpt, int(label), float(conf)])

print(lights)