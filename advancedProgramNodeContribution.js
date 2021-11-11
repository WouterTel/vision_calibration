const ProgramNodeContribution = require('rodix_api').ProgramNodeContribution;
const Xmlrpc = require('./interfaces/xmlrpc_new');

let xmlrpcURL = 'http://localhost:60050/RPC2';

class AdvancedProgramNodeContribution extends ProgramNodeContribution {
    constructor(rodiAPI, dataModel, daemonService){
        super();
        this.rodiAPI = rodiAPI;
        this.dataModel = dataModel;
        this.daemonSvc = daemonService;
        this.uiHandler = rodiAPI.getUIHandler();
        this.components = this.uiHandler.getAllUIComponents();
        this.console = this.rodiAPI.getUserInteraction().Console;
        this.extension = rodiAPI.getExtensionContribution('AdvancedExtensionNodeContribution');

    }

    initializeNode(thisNode, callback) {
        callback(null, thisNode);
    }

    openView(){}
    closeView(){}
    generateScript(enterWriter, exitWriter){
        
        this.xmlrpcClient = new Xmlrpc(xmlrpcURL);
        let initVec = this.extension.getInitialCalibration();
        enterWriter.appendLine(`let advancedXMLClient = rpcFactory('xmlrpc', '${xmlrpcURL}');`);
        enterWriter.appendLine(`let vec = [${initVec[0]},${initVec[1]},${initVec[2]},${initVec[3]},${initVec[4]},${initVec[5]},${initVec[6]},${initVec[7]},${initVec[8]},${initVec[9]},${initVec[10]},${initVec[11]}];`);
        enterWriter.appendLine(`let deltaVec = advancedXMLClient.ext_operation_calibration(vec);`);
        enterWriter.appendLine(`console.log(deltaVec);`);
        
        
    }
    isDefined(){
       return true;
    }

}

module.exports = AdvancedProgramNodeContribution;