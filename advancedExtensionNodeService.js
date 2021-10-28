const path = require('path');
const ExtensionNodeService = require('rodix_api').ExtensionNodeService;
const advancedExtensionNodeContribution = require(path.join(__dirname, 'advancedExtensionNodeContribution'));

class AdvancedExtensionNodeService extends ExtensionNodeService{
    constructor(myDaemonSvc){
        super();
        this.myDaemonSvc = myDaemonSvc;
    }

    getTitle(){
        return 'Calibration system';
    }
    getHTML(){
        return path.join(__dirname, "htmlStore/advancedExtensionNode.html");
    }
    createContribution(rodiAPI, dataModel){
        return new advancedExtensionNodeContribution(rodiAPI, dataModel, this.myDaemonSvc);
    }
}

module.exports = AdvancedExtensionNodeService;
