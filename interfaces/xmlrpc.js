const xmlrpc = require('xmlrpc');

class XMLRPC {
    constructor(url){
        this.client = xmlrpc.createClient(url);
    }
    ext_setMsg(msg, cb){
        this.client.methodCall('ext_setMsg', [msg], function(err, value){
            if(cb){
                cb(err, value);
            }
        });
    }
    ext_getMsg(cb){
        this.client.methodCall('ext_getMsg', [], function(err, value){
            if(cb){
                cb(err, value);
            }
        });
    }
    ext_add(operand1, operand2, cb){
        this.client.methodCall('ext_add', [operand1, operand2], function(err, value){
            if(cb){
                cb(err, value);
            }
        });
    }
    ext_subtract(operand1, operand2, cb){
        this.client.methodCall('ext_subtract', [operand1, operand2], function(err, value){
            if(cb){
                cb(err, value);
            }
        }.bind(this));
    }
    ext_divide(operand1, operand2, cb){
        this.client.methodCall('ext_divide', [operand1, operand2], function(err, value){
            if(cb){
                cb(err, value);
            }
        }.bind(this));
    }
    ext_multiply(operand1, operand2, cb){
        this.client.methodCall('ext_multiply', [operand1, operand2], function(err, value){
            if(cb){
                cb(err, value);
            }
        });
    }
}

module.exports = XMLRPC;