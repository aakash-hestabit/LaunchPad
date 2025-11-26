const demoRoute = (req,res,next)=>{
    try{
        throw new Error("this is demo routes error");
    }catch(e){
        res.status(500).json({error:e.message});
    }
}

export {demoRoute}