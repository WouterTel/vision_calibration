const xmlrpc = require('xmlrpc');

class XMLRPC {
    constructor(url){
        this.client = xmlrpc.createClient(url);
    }
    ext_calibrate_camera(cb){
        this.client.methodCall('ext_calibrate_camera', [],  function(err, value){
            if(cb){
                cb(err, value);
            }
        });
    }
    ext_initial_calibration(cb){
        this.client.methodCall('ext_initial_calibration', [], function(err, value){
            if(cb){
                cb(err, value);
            }
        });
    }
    ext_operation_calibration(cb){
        this.client.methodCall('ext_operation_calibration', [], function(err, value){
            if(cb){
                cb(err, value);
            }
        });
    }
}

module.exports = XMLRPC;