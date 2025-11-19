const { parentPort, workerData } = require('worker_threads');



function countWordFrequency(wordsArray) {
    const frequency = {};
    wordsArray.forEach(word => {
        word = word.toLowerCase();
        frequency[word] = (frequency[word] || 0) + 1;
    });
    return frequency;
}

function processChunk(chunk, options) {
    const wordsArray = chunk;
    const filteredWords = wordsArray.filter(word => word.length > options.minLen);
    const wordFrequency = countWordFrequency(filteredWords);

    let result = {
        total_words: filteredWords.length,
        unique_words: wordFrequency,
        longest_word: '',
        smallest_word: '',
    };

    let frequencyArray = Object.entries(wordFrequency);
    frequencyArray.sort((a, b) => b[1] - a[1]);

    frequencyArray.forEach(([word, count], _) => {
        if (word.length > result.longest_word.length) {
            result.longest_word = word;
        }
        if (word.length < result.smallest_word.length || result.smallest_word === '') {
            result.smallest_word = word;
        }
    });

    return result;
}

const result = processChunk(workerData.chunk, workerData.options);
parentPort.postMessage(result);
