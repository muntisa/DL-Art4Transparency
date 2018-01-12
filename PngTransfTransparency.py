# PngTransfTransparency
# Transfer transparency from one image to other
# (extra corrections for margine pixels and shine)

from PIL import Image

def PngTransfTransparency(TransparentPNG,TargetPNG,CorrectedPNG):
    # inputs:
    # TransparentPNG = file (+ path) for the transparent PNG used as source to transfer transparency
    # TargetPNG = file (+ path) for the PNG that should be modified by adding transparency from the source
    # CorrectedPNG = the resulting image (target image with the transparency from transparent image)
    
    # get pixels from transparent image
    img = Image.open(TransparentPNG) #image path and name
    img = img.convert("RGBA")
    datas = img.getdata()
    # get pixels from Target image without transparency
    img2 = Image.open(TargetPNG) #image path and name
    img2 = img2.convert("RGBA")
    datas2 = img2.getdata()

    # Create a new PNG based on Target PNG and the transparency from Transparent PNG
    newData = [] # pixels for the new PNG
    for i in range(len(datas)):
        item = datas[i]  # each pixel from transparent png
        item2= datas2[i] # each pixel from non-transparent png

        # if there is a transparent pixel transfer it to the other image
        if item[3] == 0:
            newData.append((255, 255, 255, 0))
        else:
            # if is not a trasparent pixel, transfer the initial transparency (pixel shine)
            newData.append((item2[0], item2[1], item2[2], item[3]))
                
    img.putdata(newData)
    img.save(CorrectedPNG, "PNG") # save the corrected image
    return

########################################

if __name__ == "__main__":
    TransparentPNG = './autumn-png-leaf_resizedx.png'
    TargetPNG      = './autumn-png-leaf_starry-night-van-gogh_fchollet_10.png'
    CorrectedPNG   = TargetPNG[:-4] + '_corr.png'
    PngTransfTransparency(TransparentPNG,TargetPNG,CorrectedPNG)
