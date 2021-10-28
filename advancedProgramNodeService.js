const path = require('path');
const ProgramNodeService = require('rodix_api').ProgramNodeService;
const AdvancedProgramNodeContribution = require(path.join(__dirname, 'advancedProgramNodeContribution'));

class AdvancedProgramNodeService extends ProgramNodeService{
    constructor(daemonService){
        super();

        this.daemonService = daemonService;
    }

    getIcon() {
        return path.join(__dirname, "htmlStore/resource/ico-cmd-advanced.png");
    }

    getTitle(){
        return 'Advanced';
    }

    getHTML(){
        return path.join(__dirname, 'htmlStore/advancedProgramNodeService.html');
    }

    isDeprecated(){
        return false;
    }

    isChildrenAllowed(){
        return false;
    }

    isThreadAllowed() {
        return true;
    }

    createContribution(rodiAPI, dataModel){
        return new AdvancedProgramNodeContribution(rodiAPI, dataModel, this.daemonService);
    }
}

module.exports = AdvancedProgramNodeService;
