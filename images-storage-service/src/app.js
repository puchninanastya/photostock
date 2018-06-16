const app = require('express')();
const bodyParser = require('body-parser');
import apiRouter from './routes/api-router';
import config from './config/config';

/*configure app to use body-parser*/
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());

/*configuring our application routes*/
app.use('/api/v1', apiRouter);


/*tells our application to listen on the specified port*/
app.listen(config.app.port);
console.log("Storage service running on port: " + config.app.port);