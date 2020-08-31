const cheerio = require("cheerio")
const fetch = require("node-fetch")
const link = "https://forums.spacebattles.com/threads/compulsion-worm-prototype.821228/reader/"




const page_futures = (story_link) =>{
    futures = []
    //get single return, parse for page numbers
    fetch(story_link)
        .then((response) => {
            response.text()      
        })
        .then(data => {
            //create container to store html
            //parse info from container using cheerio
            let docs = cheerio.load(data)
            console.log(docs)
        }) 
        .catch(error => console.log(error))
} 


page_futures(link)

const fireWalkWithMe = new Promise((resolve, reject) => {
    //tbfleshedoutinamomentplswait
})






