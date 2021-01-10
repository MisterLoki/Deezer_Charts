from PIL import Image, ImageDraw, ImageFilter ,ImageFont
import requests

from util import ImageUtil, Utility



def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return None

def getdata():
    print("Get Data From the API")
    try:  
        resp = requests.get('https://api.deezer.com/chart',headers={})
        featured = resp.json()["tracks"]["data"]
        return featured[0:10]
    except:
        return None   

data = getdata()

if data is not None :
    print("Generate Image")
    filename = 'assets/images/empty.png'
    bg = Image.open(filename, 'r').convert("RGBA")
    text_img = Image.new('RGB', (640,640), (0,0,0))
    text_img.paste(bg, (0,0),mask=bg)
    last_item = None
    for x in data :
        title = x["title_short"]
        artist = x["artist"]["name"]
        if find_between(title , '(feat. ' , ')' ) is not None:
            artist = artist + " , " + find_between(title , '(feat. ' , ')' )
        if find_between(title , '' , '(feat. ' ) is not None:
            title = find_between(title , '' , '(feat. ' )  
        title_font = ImageFont.truetype('assets/fonts/BurbankBigRegular-Black.otf', 20)
        artist_font = ImageFont.truetype('assets/fonts/BurbankBigRegular-Black.otf', 20)
        if str(x["position"]) == "1":           
            image_editable = ImageDraw.Draw(text_img)
            image_editable.text((84,193), title,(0,0,0) , font=title_font)
            image_editable.text((341,193), artist,(0,0,0) , font=title_font)
        else :
            image_editable = ImageDraw.Draw(text_img)
            w, h = title_font.getsize(last_item)
            image_editable.text((84,177+16+(43*(x["position"]-1))), title,(0,0,0) , font=title_font)
            image_editable.text((341,177+16+(43*(x["position"]-1))), artist,(0,0,0) , font=title_font)
        last_item = title
            
    text_img.save("generate.png", format="png")
    print("Done")
else : 
    print("Error")