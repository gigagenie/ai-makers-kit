const crypto=require('crypto');
const dateFormat=require('dateformat');
const grpc=require('grpc');
const fs=require('fs');
function getTimeStamp(){
	return dateFormat(new Date(),'yyyymmddHHmmssL');
};
function createSignature(id,timestamp,secret){
    return crypto.createHmac('sha256',secret).update(id+':'+timestamp).digest('hex');
};
function generateMetadata(params,callback){
	const metadata=new grpc.Metadata();
	const timeStamp=getTimeStamp();
	metadata.add('x-auth-clientkey',client_key);
	metadata.add('x-auth-timestamp',timeStamp);
	const signature=createSignature(client_id,timeStamp,client_secret);
	metadata.add('x-auth-signature',signature);;
	callback(null,metadata);
};
let client_id=null;
let client_key=null;
let client_secret=null;
let sslCred=null;
let authCred=null;
let credentials=null;
let proto=null;
let client=null;
const initialize=(inClientId,inClientKey,inClientSecret,inCertPath,inProtoPath)=>{
	client_id=inClientId;
	client_key=inClientKey;
	client_secret=inClientSecret;
	sslCred=grpc.credentials.createSsl( fs.readFileSync(inCertPath));
	authCred=grpc.credentials.createFromMetadataGenerator(generateMetadata);
	credentials=grpc.credentials.combineChannelCredentials(sslCred,authCred);
	proto=grpc.load(inProtoPath).kt.gigagenie.ai.speech;
	client=new proto.Gigagenie('gate.gigagenie.ai:4080',credentials);
};
const initializeJson=(inJsonFile,inCertPath,inProtoPath)=>{
	const readFromFile=fs.readFileSync(inJsonFile);
	const jsonData=JSON.parse(readFromFile.toString());
	client_id=jsonData.clientId;
	client_key=jsonData.clientKey;
	client_secret=jsonData.clientSecret;
	sslCred=grpc.credentials.createSsl( fs.readFileSync(inCertPath));
	authCred=grpc.credentials.createFromMetadataGenerator(generateMetadata);
	credentials=grpc.credentials.combineChannelCredentials(sslCred,authCred);
	proto=grpc.load(inProtoPath).kt.gigagenie.ai.speech;
	client=new proto.Gigagenie('gate.gigagenie.ai:4080',credentials);
};
const getVoice2Text=()=>{
	return client.getVoice2Text();
};
const getText2VoiceUrl=(inRequest,callback)=>{
	client.getText2VoiceUrl(inRequest,callback);
};
const getText2VoiceStream=(inRequest)=>{
	return client.getText2VoiceStream(inRequest);
};
const queryByText=(inRequest,callback)=>{
	client.queryByText(inRequest,callback);
};
const queryByVoice=(callback)=>{
	return client.queryByVoice({},callback);
};
module.exports={
	initialize:initialize,
	initializeJson:initializeJson,
	getVoice2Text:getVoice2Text,
	getText2VoiceUrl:getText2VoiceUrl,
	getText2VoiceStream:getText2VoiceStream,
	queryByText:queryByText,
	queryByVoice:queryByVoice
};
