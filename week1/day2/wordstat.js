const fs = require('fs');
const path = require('path');
const os = require('os');
const { Worker } = require('worker_threads');

const startTime = process.hrtime.bigint();

const log_file_path = path.join(__dirname, '..', 'logs', 'day2_cli_output_worker_threads.json');

let result = {
    total_words: 0,
    unique_words_length: 0,
    unique_words: {},
    longest_word: "",
    smallest_word: "",
    top_n_most_repeated_words: []
};

function splitWords(text) {
    let cleanedText = text.replace(/\./g, ' ');
    return cleanedText.trim().split(/\s+/);
}

function parseArgs() {
    const args = process.argv.slice(2);
    const options = {
        file: null,
        topN: 10,
        minLen: 3,
        unique: false
    };

    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--file':
                options.file = args[i + 1];
                i++;
                break;
            case '--top':
                options.topN = parseInt(args[i + 1], 10);
                i++;
                break;
            case '--minLen':
                options.minLen = parseInt(args[i + 1], 10);
                i++;
                break;
            case '--unique':
                options.unique = true;
                break;
            default:
                console.log(`Unknown argument: ${args[i]}`);
                break;
        }
    }

    if (!options.file) {
        console.error("--file <filename> argument not provided. Please provide the filename.");
        process.exit(1);
    }

    return options;
}

async function readAndProcessFile(options) {
    try {
        const datah = await fs.promises.readFile(options.file, 'utf8');
        const data = splitWords(datah);
        const thread_count = os.cpus().length;
        const chunkSize = Math.ceil(data.length / thread_count);  
        const promises = [];
        
        for (let i = 0; i < thread_count; i++) {
            const chunk = data.slice(i * chunkSize, (i + 1) * chunkSize);
            promises.push(processWithWorker(chunk, options));
        }

        const results = await Promise.all(promises);

        results.forEach((workerResult) => {
            result.total_words += workerResult.total_words;

            Object.entries(workerResult.unique_words).forEach(([word, count]) => {
                result.unique_words[word] = (result.unique_words[word] || 0) + count;
            });

            if (workerResult.longest_word.length > result.longest_word.length) {
                result.longest_word = workerResult.longest_word;
            }
            if (workerResult.smallest_word.length < result.smallest_word.length || result.smallest_word === "") {
                result.smallest_word = workerResult.smallest_word;
            }
        });
        
        const sortedWords = Object.entries(result.unique_words)
            .map(([word, count]) => ({ word, count }))
            .sort((a, b) => b.count - a.count);

        result.top_n_most_repeated_words = sortedWords.slice(0, options.topN);

        result.unique_words_length = Object.keys(result.unique_words).length;
        const endTime = process.hrtime.bigint(); 
        const totTime = (Number(endTime-startTime) / 1e6).toFixed(2); 
        result.total_time = totTime+'ms';
        await fs.promises.mkdir(path.dirname(log_file_path), { recursive: true });
        await fs.promises.writeFile(log_file_path, JSON.stringify(result, null, 2));

        console.log("Log file saved successfully.");
        
        console.log("total time taken:",totTime,"ms");

    } catch (err) {
        console.error("Error reading or processing the file:", err);
    }
}

function processWithWorker(chunk, options) {
    return new Promise((resolve, reject) => {
        const worker = new Worker('./worker.js', {
            workerData: { chunk, options }
        });

        worker.on('message', (message) => {
            resolve(message);
        });

        worker.on('error', reject);
        
    });
}

const options = parseArgs();
readAndProcessFile(options);
