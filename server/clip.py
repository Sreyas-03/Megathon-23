import torch
from CLIP import clip
from PIL import Image
import numpy as np
import ssl
import cv2

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

# def extract_information(text):
#     nlp = spacy.load("en_core_web_sm")
#     doc = nlp(text)

#     # Extract nouns, verbs, and named entities
#     nouns = [token.text for token in doc if token.pos_ == "NOUN"]
#     verbs = [token.text for token in doc if token.pos_ == "VERB"]
#     entities = [ent.text for ent in doc.ents] # entities meaning named entities, whcih means names of people, places, organizations, etc.

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# paths = [
#     "../sales.jpeg",
#     "../sales2.jpeg",
#     "../swe.jpeg",
#     "../swe2.jpeg",
#     "../research2.jpeg",
#     "../ml.jpeg",
#     "../dec.png",
#     "../research2.png",
#     "../adv.jpg",
#     "../lawyer.jpeg",
#     "../doctor.jpeg",
#     "../doctor2.png",
#     "../teacher.jpeg",
#     "../teacher2.png",
#     "../researcher3.jpeg",
# ]

def gen_imgs(labels):
    imgs = []
    width, height = 256, 256
    for label in labels:
        blank_image = np.zeros((height, width, 3), dtype=np.uint8)
        font_scale = 2
        font_thickness = 3
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_color = (255, 255, 255)  # White color in BGR
        line_type = cv2.LINE_AA

        # Get the size of the text bounding box
        text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]

        # Calculate the position to center the text
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2

        # Put the text on the blank image
        cv2.putText(blank_image, label, (text_x, text_y), font, font_scale, font_color, font_thickness, line_type)
        # cv2.imshow('Centered Text on Blank Image', blank_image)
        # cv2.waitKey(0)
        img = preprocess(Image.fromarray(blank_image)).unsqueeze(0).to(device)
        imgs.append(img)
    
    return torch.cat(imgs, dim=0)

# images = []
# for path in paths:
#     img = preprocess(Image.open(path)).unsqueeze(0).to(device)
#     # print(img.shape)
#     images.append(img)

labels = [
    "sales"
    "sales manager",
    
    "software engineer",
    "software developer",
    "network engineer",
    "database administrator",
    "database engineer",
    "IT project manager",
    "systems administrator",

    "marketing manager",
    "content marketer",
    "market research analyst",
    "digital marketing",

    "teacher",
    "professor",
    
    "researcher",
    "civil engineer",
    "mechanical engineer",
    "electrical engineer",

    "medical",
    "nurse",
    "physician",
    "therapist",
    "healthcare",
    "health",
    "doctor",

    "lawyer",
    "accountant",
    "financial analyst",
    "investment banker",
    "finance"
 ]

labels = np.array(labels)

# images = torch.cat(images, dim=0)
images = gen_imgs(labels)
# images = torch.concatenate([image, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12, image13, image14, image15])

# prompt = "Talent Acquisition Specialist at Genpact, responsible for sourcing, screening, hiring qualified candidates various roles across organization. "

arr = [
    "Experience in Database Management, Data Mining, Software Development Fundamentals, Strategic Planning, Operating Systems, Requirements Analysis, Data warehousing, Data Modeling and Data Marts. Area of expertise encompasses Database designing, ETL phases of Data warehousing. Execution of test plans for loading the data successfully. Strong database skills with Oracle (performance tuning, complex SQL)"
]





### Best Answer:
best = "It depends on how desperate I am for getting the job. If I already have a job offer in hand, and don't really consider this interview to be my best choice,  I will help him out. I would also look if there are other people around to help, in that case I might proceed for the interview."

### Mediocre Answer:
med = "I would go to the interview as there are other people to help him out with crossing the road."

### Bad Answer:
bad = "I would go and help him cross the road, regardless of the risk of losing the job."
arr = [best, med, bad]


def check_answer(user = ["I would not go and help him cross the road, regardless of the risk of losing the job."]):
    # user = [user]

    text = clip.tokenize(arr).to(device)
    user_text = clip.tokenize(user).to(device)
    # print(text)
    with torch.no_grad():
        # image_features = model.encode_image(images)
        
        # print(image_features.shape)
        text_features = model.encode_text(text)
        user_text_features = model.encode_text(user_text)
        # print(user_text_features)

        # print(text_features.shape)
        # image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        user_text_features /= user_text_features.norm(dim=-1, keepdim=True)
        # print(text_features)
        # print(user_text_features)
        scores = text_features @ user_text_features.T
        scores = torch.argmax(scores).item()
        return scores
        # print(f"Cosine Distance of images: {image_features @ image_features.T}")
        # dist = image_features @ text_features.T
        # print(dist)
        # l = torch.argsort(dist[:, 0])[-2:].tolist()
        # labels = np.array(labels)
        # print(labels[torch.argsort(dist[:, 0])[-2:].tolist()][::-1])
        # for i in range(dist.shape[0]):
        #     print(dist[i], labels[i])

        # logits_per_image, logits_per_text = model(image, text)
        # probs = logits_per_image.softmax(dim=-1).cpu().numpy()

    # print("Label probs:", probs)  # prints: [[0.9927937  0.00421068 0.00299572]]


def analyze_about(arr = "I would not go and help him cross the road, regardless of the risk of losing the job."):
    arr = [arr]
    text = clip.tokenize(arr).to(device)
    print(text)
    with torch.no_grad():
        image_features = model.encode_image(images)
        
        # print(image_features.shape)
        text_features = model.encode_text(text)
        # print(text_features.shape)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        # print(f"Cosine Distance of images: {image_features @ image_features.T}")
        dist = image_features @ text_features.T
        # print(f"Cosine Distance ")
        # print(dist)
        # l = torch.argsort(dist[:, 0])[-2:].tolist()
        # print(dist)
        # labels = np.array(labels)
        return labels[torch.argsort(dist[:, 0])[-5:].tolist()][::-1]
        retval = []
        for i in range(dist.shape[0]):
            retval.append(labels[i])
        return retval


if __name__ == "__main__":
    print(analyze_about())