const path = require('path');
const DaemonService = require('rodix_api').DaemonService;

class AdvancedDaemonService extends DaemonService{
  constructor() {
      super();

      //this.executablePath = path.join(__dirname, 'exec', 'calculator.py');
      this.executablePath = path.join(__dirname, 'exec', 'calibration_system.py');
      //this.executablePath = path.join(__dirname, 'exec', 'cameraCheck.py');
      this.daemonContribution = null;
    }

    init(daemon) {
        this.daemonContribution = daemon;
    }

    getExecutable() {
      return this.executablePath;
    }
    getTitle(){
        return 'Advanced';
    }
    eventOnWidget(){

    }
    getDaemon() {
      return this.daemonContribution;
    }
}

module.exports = AdvancedDaemonService;
