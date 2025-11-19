const fs1 = require('fs/promises');
const fs = require('fs')
const path = require('path');
const filePath = path.join(__dirname,'50mb.txt');
const LOG_FILE_PATH = path.join(__dirname, '..','logs', 'day1-perf.json');
let jsonString = "";
const result = {
    excecutionTime_Buffer:0,
    memoryUsage_Buffer : 0,
    excecutionTime_Stream:0,
    memoryUsage_Stream : 0,
}
function format(data) {
  return Math.round(data.heapUsed / 1024 / 1024 * 100) / 100
}
async function readFileFunction(){
    console.log("-----------BUFFER STATS-----------")
    console.log();
    const initialMem = format(process.memoryUsage());
    console.log('Memory usage at start:', initialMem, 'MB'); 
    const startTime = process.hrtime.bigint();

    const content = await fs1.readFile(filePath,'utf-8');
    console.log('Memory usage after reading file:', format(process.memoryUsage()), 'MB'); 
    
    const endTime = process.hrtime.bigint(); 
    const totTime = (Number(endTime-startTime) / 1e6).toFixed(2); 
    const finalMem = format(process.memoryUsage());
    result.excecutionTime_Buffer = totTime +" ms";
    result.memoryUsage_Buffer = (finalMem - initialMem).toFixed(2)+" MB";
    console.log('Memory usage at end:', finalMem, 'MB'); 
    console.log(`Total memory used by readFile(Buffer): ${(finalMem - initialMem).toFixed(2)} MB`);
    console.log(`Total time taken  by readFile(Buffer): ${totTime} ms`)

    
}


async function createReadStreamFunction(){
    console.log();console.log()
    console.log("-----------STREAM STATS-----------")
    console.log();
    const initialMem = format(process.memoryUsage());
    console.log('Memory usage at start:', initialMem, 'MB'); 
    const startTime = process.hrtime.bigint();
    const readStream = fs.createReadStream(filePath,'utf-8');
    console.log('Memory usage after stream creation:', format(process.memoryUsage()), 'MB');
    readStream.on('data', (chunk) => {
    });
    readStream.on('end', () => {
        const endTime = process.hrtime.bigint(); 
        const totTime = (Number(endTime-startTime) / 1e6).toFixed(2); 
        const finalMem = format(process.memoryUsage()); 
        result.excecutionTime_Stream = totTime +" ms";
        result.memoryUsage_Stream = (finalMem - initialMem).toFixed(2) +" MB";
        console.log('Memory usage at end:', finalMem, 'MB'); 
        console.log(`Total memory used by Stream (fs.createReadStream): ${(finalMem - initialMem).toFixed(2)} MB`);
        console.log(`Total time taken  Stream (fs.createReadStream): ${totTime} ms`)
        console.log(result)
        jsonString = JSON.stringify(result, null, 2); 
        fs1.writeFile(LOG_FILE_PATH, jsonString, { encoding: 'utf-8' });
    });
    readStream.on('error', (err) => {
        console.error('An error occurred:', err);
    });
}
;(async ()=>{
    await fs1.mkdir(path.dirname(LOG_FILE_PATH), { recursive: true }); // making the directory
    await readFileFunction();
    await createReadStreamFunction();
    

})();
