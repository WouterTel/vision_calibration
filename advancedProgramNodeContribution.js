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
        let initVec = this.extension.getInitialCalibration();
       
        let deltaVec = [0,0,0,0,0,0];
        this.xmlrpcClient = new Xmlrpc(xmlrpcURL);
        
        this.xmlrpcClient.ext_operation_calibration(initVec,function(err, rst){
            //this.dataModel.set('deltaVec',rst)
        }.bind(this));

        this.console.log(`${deltaVec}`);
        //deltaVec = this.dataModel.get('deltaVec');
        //this.console.log(`${deltaVec}`);
        //enterWriter.appendLine(`let deltaVec = [${deltaVec}];`);
    }
    isDefined(){
       // return (
       //     this.dataModel.get('showType') &&
       //     this.extension.getXMLRPCClient() !== null &&
       //     this.extension.getOperator() !== undefined
       // );
       return true;
    }
/*
    onSbShowType(type, data){
        if(type === 'select'){
            this.dataModel.set('showType', data.selected);
        }
    }
    */
}

module.exports = AdvancedProgramNodeContribution;