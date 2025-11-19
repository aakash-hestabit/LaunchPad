const os = require("os");
const process = require("process");

console.log("introspect.js");
console.log("OS: ")
console.log(`       ${os.type()}  ${os.release()}`);

console.log("Architecture: ")
console.log(`       ${os.arch()}`);

console.log("CPU Cores: ")
console.log(`       ${os.cpus().length}`);

console.log("Total Memory: ")
console.log(`       ${(os.totalmem()/(1024**3)).toFixed(2)} GB`);

console.log("System Uptime: ")
console.log(`       ${(os.uptime()/3600).toFixed(2)} hrs`);

console.log("Current Logged User: ")
console.log(`       ${os.userInfo().username}`);

console.log("Node Path: ")
console.log(`       ${process.execPath}`);
