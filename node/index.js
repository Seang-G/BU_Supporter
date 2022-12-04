const express = require('express'); // express 임포트
const app = express(); // app생성
const port = 5000;

app.get('/', function (req, res) {
  // res.sendFile(__dirname+"/templates/index.html");
  
});

app.listen(port, () => console.log(`${port}포트입니다.`));

const { MongoClient, ServerApiVersion } = require('mongodb');
// MongoDB 주소
const uri = "mongodb+srv://SeangG:0903@mycluster.cbbabsn.mongodb.net/?retryWrites=true&w=majority";
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true, serverApi: ServerApiVersion.v1 });

client.connect(err => {
  // db 및 컬랙션 선택
  const collection = client.db("test").collection("도서관");
  client.db("test").listCollections().forEach(data=>{
    console.log(data["name"])
  })
  // 모든 정보 가져오기
  let datas = collection.find()
  // datas.forEach(data=>console.log(data))
});
