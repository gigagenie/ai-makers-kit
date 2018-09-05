const request = require('request');
const youtubedl=require('youtube-dl');
const Cvlc=require('cvlc');
let player=new Cvlc();
const yturl= 'https://www.youtube.com/watch?v=NwhCsMepR3U';
const ytoptions=['--format=250'];

function getYoutubeSearchList(inQuery){
	const queryText=inQuery;
	return new Promise((resolve,reject)=>{
		console.log('QueryText:'+queryText);
		const searchurl='https://www.youtube.com/results?search_query=';
		const queryUrl=encodeURI(searchurl+queryText);
		request(queryUrl,(err,res,body)=>{
			let splitByWatch=body.split('href=\"\/watch?');
			let isFirst=true;
			let urlList=[];
			splitByWatch.forEach((splitText)=>{
				if(isFirst===true) isFirst=false;
				else {
					let splitByQuot=splitText.split('"');
					urlList.push(splitByQuot[0]);
				}
			});
			resolve(urlList);
		});
	});
};
function getPlayRealUrl(inUrl){
	const url=inUrl;
	return new Promise((resolve,reject)=>{
		youtubedl.getInfo(url,ytoptions,function(err,info){
			console.log('title:'+info.title);
			console.log('url:'+info.url);
			resolve({title:info.title,url:info.url});
		});
	});
};
const youtubePlayBaseUrl='https://www.youtube.com/watch?';
async function playYoutubeByText(inQuery){
	let urls=await getYoutubeSearchList(inQuery);
	let targetUrl=youtubePlayBaseUrl+urls[0];
	console.log('yt url:'+targetUrl);
	let realPlayUrl=await getPlayRealUrl(targetUrl);
	console.log('title:'+realPlayUrl.title+' url:'+realPlayUrl.url);
	player.play(realPlayUrl.url,()=>{
		console.log('Music Played');
	});
};
playYoutubeByText('싸이');
