const record=require('node-record-lpcm16');
const aikit=require('./aimakerskitutil');

const client_id='';
const client_key='';
const client_secret='';
const json_path='';

const proto_path='../data/gigagenieRPC.proto';

function initMic(){
        return record.start({
                sampleRateHertz: 16000,
                threshold: 0,
                verbose: false,
                recordProgram: 'arecord',
                silence: '10.0',
        })
};
let writeFlag=0;

//aikit.initialize(client_id,client_key,client_secret,proto_path);
aikit.initializeJson(json_path,proto_path);
const ktstt=aikit.getVoice2Text();
ktstt.on('error',(error)=>{
    console.log('Error:'+error);
});
ktstt.on('data',(data)=>{
    console.log('data:'+JSON.stringify(data));
});
ktstt.on('end',()=>{
        console.log('pcm end');
        record.stop();
	writeFlag=0;
	ktstt.end();
});
ktstt.write({reqOptions:{mode:0,lang:0}});
writeFlag=1;
const mic=initMic();
mic.on('data',(data)=>{
    if(writeFlag===1) ktstt.write({audioContent:data});
});
console.log('say something');
