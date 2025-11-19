const fs = require('fs'); 
const path = require('path');

const startTime = process.hrtime.bigint();

const log_file_path = path.join(__dirname, '..', 'logs', 'day2_cli_output.json');
const result = {
    total_words: 0,
    unique_words_length: 0,
    unique_words: ["not_specified_in_arguments"],
    longest_word: "",
    smallest_word: "",
    top_n_most_repeated_words: []
};

function parseArgs() {
    const args = process.argv.slice(2); // first two indexes are skipped as these are only node and path to script file 

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

function splitWords(text) {
    let cleanedText = text.replace(/\./g, ' ');  // here using this regex we are removing all the punctuation(everything except word characters and white spaces )
    return cleanedText.trim().split(/\s+/);
}

function countWordFrequency(wordsArray) {
    const frequency = {};
    wordsArray.forEach(word => {
        word = word.toLowerCase();
        frequency[word] = (frequency[word] || 0) + 1;
    });
    return frequency;
}

async function wordstat() {
    const options = parseArgs();
    console.log("Options given: ", options);
    

    try {
        const data = await fs.promises.readFile(options.file, 'utf8');
        const wordsArray = splitWords(data);
        const minlen = options.minLen;
        const filteredWords = wordsArray.filter(word => word.length > minlen);

        console.log("Total words: ", filteredWords.length);
        result.total_words = filteredWords.length;

        const wordFrequency = countWordFrequency(filteredWords);

        if (options.unique) {
            console.log("Unique Words: ");
            const uniqueWords = Object.keys(wordFrequency);
            console.log("Total no of unique elements: ", uniqueWords.length);
            uniqueWords.forEach((word, _) => {
                console.log(word);
            });
            result.unique_words_length = uniqueWords.length;
            result.unique_words = uniqueWords;
        }

        const frequencyArray = Object.entries(wordFrequency);
        frequencyArray.sort((a, b) => b[1] - a[1]);

        let largestWord = "";
        let smallestWord = frequencyArray[0][0];
        let N = options.topN;

        frequencyArray.forEach(([word, count], _) => {
            if (N > 0) {
                result.top_n_most_repeated_words.push({word:word,count:count});
                console.log(`${word}: ${count}`);
                N -= 1;
            }

            if (word.length > largestWord.length) {
                largestWord = word;
            }
            if (word.length < smallestWord.length) {
                smallestWord = word;
            }
        });

        result.longest_word = largestWord;
        result.smallest_word = smallestWord;

        console.log("Smallest word: ", smallestWord);
        console.log("Largest word: ", largestWord);
        const endTime = process.hrtime.bigint(); 
        const totTime = (Number(endTime-startTime) / 1e6).toFixed(2); 
        result.total_time = totTime+'ms'
        await fs.promises.mkdir(path.dirname(log_file_path), { recursive: true });

        await fs.promises.writeFile(log_file_path, JSON.stringify(result, null, 2));
        console.log("Log file saved successfully.");
        
        console.log("total time taken:",totTime,"ms");

    } catch (err) {
        console.error("Error processing the file:", err);
    }
    
}

wordstat();
