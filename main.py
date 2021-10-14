import cv2, os

def add_text(img,text,loc):
    BLACK = (0,0,0)
    font = cv2.FONT_HERSHEY_COMPLEX
    font_size = 8
    font_color = BLACK
    font_thickness = 30

    text_size, _ = cv2.getTextSize(text,font,font_size,font_thickness)

    img = cv2.putText(img, text, (loc[0]-int(text_size[0]/2), loc[1]+int(text_size[1]/2)), font, font_size, font_color, font_thickness, cv2.LINE_AA)

    return img

def shrink(img, scale=0.3):
    return cv2.resize(img, (int(img.shape[1]*scale), int(img.shape[0]*scale)))

if __name__ == '__main__':
    # Read image files
    images = os.listdir('images')
    img_vec = []
    for i,img_file in enumerate(images):
        img = cv2.imread('images/' + img_file)
        w = img.shape[1]
        h = img.shape[0]
        c = (w-500,h-500)
        r = 200
        
        img = cv2.circle(img, c, r, (255,0,0), 60)
        img = cv2.circle(img, c, r, (255,255,255), -1)
        img = add_text(img,str(i+1),c)

        img_vec.append(shrink(img))

    # Assemble images into rows
    img_rows = []
    i = 0
    while i<len(img_vec):
        img_rows.append(cv2.hconcat(img_vec[i:i+3]))
        i+= 3

    # Add white rectangles if necessary
    if img_rows[-1].shape[1] != img_rows[-2].shape[1]:
        img_rows[-1] = cv2.copyMakeBorder(img_rows[-1], 0, 0, 0, img_rows[-2].shape[1]-img_rows[-1].shape[1], cv2.BORDER_CONSTANT, value=[255,255,255])

    # Assemble rows into catalog
    img = cv2.vconcat(img_rows)

    # img = cv2.resize(img, (int(img.shape[1]*0.03), int(img.shape[0]*0.03)))
    cv2.imshow('Pic',img)
    key = cv2.waitKey(3000)

    # Save image
    cv2.imwrite('catalog.jpg',img)