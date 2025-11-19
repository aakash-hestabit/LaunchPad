const express = require('express');
const app = express();

app.use(express.json());

app.get('/echo', (req,res)=>{
    const headers = req.headers;
    res.json({headers});
})
app.get('/slow', async(req,res)=>{
    const time = req.query.ms || 5000;
    await setTimeout(()=>{
        res.send(`This was a slow response after ${time/1000} seconds`);
    },time);
})
app.get('/cache', (req, res) => {
    
    res.setHeader('Cache-Control', 'public, max-age=3600, must-revalidate'); 
    res.setHeader('Expires', new Date(Date.now() + 3600 * 1000).toUTCString());
    res.json({
        message: 'Cache headers set for this response',
        cacheControl: 'public, max-age=3600, must-revalidate',
        expires: new Date(Date.now() + 3600 * 1000).toUTCString(),
    });
});

const port = 3000;
app.listen(port,()=>{
    console.log(`Server running on port ${port}`);
})
