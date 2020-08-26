const fetch = require("node-fetch")

const link = "https://forums.spacebattles.com/threads/compulsion-worm-prototype.821228/reader/page-"
list_of_content = []
for (var i=1;i<10;++i){
    list_of_content.push(`${link}${i}`)
}

const all_of_them = (links) => {
    const content = []
    links.forEach(element => {
        content.push(fetch(element))      
    });
    return Promise.all(content)
}

all_of_them(list_of_content)
.then(content => {
    debugger;
    console.log(content)
})
.catch(e => console.log(e))

