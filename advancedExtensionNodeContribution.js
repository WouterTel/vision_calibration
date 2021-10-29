const ExtensionNodeContribution = require('rodix_api').ExtensionNodeContribution;
const Xmlrpc = require('./interfaces/xmlrpc_new');

let xmlrpcURL = 'http://localhost:60050/RPC2';

class AdvancedExtensionNodeContribution extends ExtensionNodeContribution {
    constructor(rodiAPI, dataModel, daemonService){
        super();
        this.rodiAPI = rodiAPI;
        this.daemonSvc = daemonService;
        this.dataModel = dataModel;
        this.uiHandler = rodiAPI.getUIHandler();
        this.components = this.uiHandler.getAllUIComponents();
        this.console = this.rodiAPI.getUserInteraction().Console;

        /* Component Events */
        this.uiHandler.on('btnStart', this.onBtnStart.bind(this));
        this.uiHandler.on('btnInitCal', this.onInitCal.bind(this));

        /* Initialize */
        this.xmlrpcClient = null;
        if(!this.dataModel.has('userMsg')){
            this.dataModel.set('userMsg', '(no message)');
        }

    }

    openView(){}
    closeView(){}
    generateScript(EnterWriter, Exitwriter){
        EnterWriter.appendLine(`let advancedXMLClient = rpcFactory('xmlrpc', '${xmlrpcURL}');`);
    }

    onBtnStart(type){
        if(type === 'click'){
            if(this.daemonSvc.getDaemon().start()){
                this.xmlrpcClient = new Xmlrpc(xmlrpcURL);
                this.console.log(`Daemon is running.`)
                this.uiHandler.render();
            }
        }
    }
    onInitCal(type){
        if(type === 'click'){
            this.xmlrpcClient.ext_initial_calibration(function(err, rst){
                this.dataModel.set('initVec', rst);
                //this.console.log(`${rst}`);
            }.bind(this));
        }
    }
    getXMLRPCClient(){
        return this.xmlrpcClient;
    }
    getInitialCalibration(){
        let initVec = this.dataModel.get('initVec');
        //this.console.log(`${initVec}`);
        return initVec;
    }
}


module.exports = AdvancedExtensionNodeContribution;
