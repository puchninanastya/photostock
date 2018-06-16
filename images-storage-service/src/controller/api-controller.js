const cloudinary = require('cloudinary');
const multer  = require('multer');
const upload = multer({ dest: 'uploads/' });
import config from '../config/config';

export default new class ApiController {

    constructor() {
        console.log('api controller constuctor() ');
        /*configure our Cloudinary*/
        cloudinary.config({
            cloud_name: config.cloudinary.cloud_name,
            api_key: config.cloudinary.api_key,
            api_secret: config.cloudinary.api_secret
        });
        console.log('cloudinary configured.');
    }

    async multiple_upload(req, res) {
        console.log('multiple upload () ');
        /* we would receive a request of file paths as array */
        let files = req.files;

        console.log('body: ');
        console.log(req.body);
        console.log('files: ');
        console.log(files);

        let multipleUpload = new Promise(async (resolve, reject) => {

            console.log('in upload() ');

            if (files) {
                let upload_len = files.length;
                console.log('files len');
                console.log(files.length);
                let upload_res = [];

                for (let i = 0; i <= upload_len; i++) {

                    let filePath = undefined;
                    if (files[i]) {
                        filePath = files[i].path;
                    }
                    console.log('filePath: ');
                    console.log(filePath);


                    await cloudinary.v2.uploader.upload(filePath, (error, result) => {

                        console.log('upload cloudinary callback() ');
                        console.log('upload res len: ');
                        console.log(upload_res.length);

                        if (upload_res.length === upload_len) {
                            /* resolve promise after upload is complete */
                            console.log('upload completed..');
                            resolve(upload_res)
                        } else if (result) {
                            /*push public_ids in an array */
                            upload_res.push(result.public_id);
                            console.log('plus one resolved..');
                        } else if (error) {
                            console.log('oh shit');
                            console.log(error);
                            reject(error)
                        }

                    });

                }
            } else {
                console.log('empty files list');
            }
        })
            .then((result) => result)
            .catch((error) => error);

        if (files) {
            let upload = await multipleUpload;
            res.json( {'response': upload });
        } else {
            res.status(400).end();
        }
    }

}
