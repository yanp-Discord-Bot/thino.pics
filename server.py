import logging
import pathlib
import secrets
import aiohttp
import aiofiles
from quart import Quart, jsonify, send_from_directory, url_for, request, render_template
import random
import os
import quart.flask_patch    




app = Quart(__name__)
from swagger_ui import quart_api_doc
logger = logging.getLogger('thino.pics')
fh = logging.FileHandler('logs/home.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

quart_api_doc(app, config_path="openapi.json", url_prefix='/docs', title='API doc')



@app.route("/")
async def home():
    folder = random.choice(['helltakerpics', 'hentai', 'neko', 'tomboy', 'thighs'])
    choice = random.choice(os.listdir(f"/mnt/volume_nyc1_02/images/{folder}"))
    print(choice)
    

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://i.thino.pics/search/{choice}") as res:
            data = await res.json()
            endpoint = data['url']
            raw_image = data['image']
            filename = data['filename']


            logger.debug(endpoint)
            logger.debug(raw_image)
            logger.debug(filename)
            return await render_template('index.html', host=request.host, raw=raw_image, endpoint=endpoint, filename=filename)





@app.route('/api/v1/helltaker')
async def helltaker():
    choice = random.choice(os.listdir("/mnt/volume_nyc1_02/images/helltakerpics"))
    image = os.path.join("/mnt/volume_nyc1_02/images/helltakerpics", choice)
    raw_image = f"https://i.thino.pics/{choice}"
    return jsonify(url=f"{raw_image}", filename=choice, status=200)

@app.route('/api/v1/hentai')
async def hentai():
    choice = random.choice(os.listdir("/mnt/volume_nyc1_02/images/hentai"))
    image = os.path.join("/mnt/volume_nyc1_02/images/hentai", choice)
    raw_image = f"https://i.thino.pics/{choice}"
    return jsonify(url=f"{raw_image}", filename=choice, status=200)

@app.route("/api/v1/neko")
async def neko():
    choice = random.choice(os.listdir("/mnt/volume_nyc1_02/images/neko"))
    image = os.path.join("/mnt/volume_nyc1_02/images/neko", choice)
    raw_image = f"https://i.thino.pics/{choice}"
    return jsonify(url=f"{raw_image}", filename=choice, status=200)

@app.route("/api/v1/tomboy")
async def tomboy():
    choice = random.choice(os.listdir(f"/mnt/volume_nyc1_02/images/tomboy"))
    raw_image = f"https://i.thino.pics/{choice}"
    return jsonify(url=f"{raw_image}", filename=choice, status=200)

@app.route("/api/v1/femboy")
async def femboy():
    choice = random.choice(os.listdir(f"/mnt/volume_nyc1_02/images/femboy"))
    raw_image = f"https://i.thino.pics/{choice}"
    return jsonify(url=f"{raw_image}", filename=choice, status=200)

@app.route("/api/v1/thighs")
async def thighs():
    choice = random.choice(os.listdir(f"/mnt/volume_nyc1_02/images/thighs"))
    raw_image = f"https://i.thino.pics/{choice}"
    return jsonify(url=f"{raw_image}", filename=choice, status=200)


@app.route('/check', methods=['POST']) #this route is made to be checked with stuff like uptime kuma and other stuff 
async def uptime_check():
    return "Checked!"

app.run(debug=True, port=2030)