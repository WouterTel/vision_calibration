const path = require('path');
const PluginActivator = require('rodix_api').PluginActivator;
const advancedDaemonSvc = require(path.join(__dirname, 'advancedDaemonService'));
const advancedExtensionSvc = require(path.join(__dirname, 'advancedExtensionNodeService'));
const advancedProgramSvc = require(path.join(__dirname, 'advancedProgramNodeService'));

class Activator extends PluginActivator {
    constructor() {
        super();
    }

    start(context) {
        let advancedDaemonService = new advancedDaemonSvc();

        context.registerService('advancedDaemonService', advancedDaemonService);
        context.registerService('advancedExtension', new advancedExtensionSvc(advancedDaemonService));
        context.registerService('advancedProgram', new advancedProgramSvc(advancedDaemonService));
    }

    stop() {
    }
}

module.exports = Activator;
