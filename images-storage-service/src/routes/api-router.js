const express = require('express');
const multer  = require('multer');
const upload = multer({ dest: 'uploads/' });
import apiController from '../controller/api-controller';

const apiRouter = express.Router();
/*first route {multiple image upload}*/
apiRouter.post('/multiple_uploads', upload.array('images', 12), apiController.multiple_upload);

export default apiRouter;