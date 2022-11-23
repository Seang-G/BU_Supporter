const express = require('express'); // express 임포트
const app = express(); // app생성
const port = 5000;

app.get('/', function (req, res) {
  res.send('hello world!!');
});

app.listen(port, () => console.log(`${port}포트입니다.`));

const { MongoClient, ServerApiVersion } = require('mongodb');
// MongoDB 주소
const uri = "mongodb+srv://SeangG:0903@mycluster.cbbabsn.mongodb.net/?retryWrites=true&w=majority";
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true, serverApi: ServerApiVersion.v1 });

client.connect(err => {
  // db 및 컬랙션 선택
  const collection = client.db("myCluster").collection("test");

  // 모든 정보 가져오기
  var datas = collection.find();
  datas.forEach((err, doc)=>{
    if(err){
      console.log(err);
    } else {
      console.log(doc);
    }
  })
  // client.close();
});
// 몽구스 연결
// const mongoose = require('mongoose');
// mongoose
//   .connect('mongodb+srv://SeangG:0903@mycluster.cbbabsn.mongodb.net/?retryWrites=true&w=majority')
//   .then(() => {
//     console.log('MongoDB conected')
//     var mySchema = mongoose.Schema({
//       title: "string",
//       link: "string"
//     }, {versionKey : false});
//     const MyModel = mongoose.model("test", mySchema);

    // DB에 저장
    // const newInfo = new MyModel({title: "[학생생활상담센터] 집단상담 프로그램 안내", link: "https://community.bu.ac.kr/bbs/info/896/31822/artclView.do"});

    // newInfo.save((err, data)=>{
    //   if(err) console.log(err);
    //   else console.log("Saved!");
    // })

    // DB에서 불러오기
    // MyModel.find()
    //   .then((docs)=>{
    //     console.log(docs);
    //   })
    //   .catch((err)=>{
    //     console.log(err);
    //   })
  // })
  // .catch((err) => {
  //   console.log(err);
  // });