function showInfo(node){                                                                                                    
	var paper_info = {};                                                                                                                           
	try {                                                                                                                                          
		home = 'https://dl.acm.org';  
		paper_info['document_title'] = node.querySelector('.issue-item__title .hlFld-Title').innerText;
		paper_info['url'] = home + node.getElementsByClassName('hlFld-Title')[0].getElementsByTagName('a')[0].getAttribute('href');                           
		paper_info['description'] = []
		node.querySelectorAll('.issue-item__detail .dot-separator span').forEach((x) => paper_info['description'].push(x.innerText));
		link = node.querySelector('.issue-item__detail a').href;
		paper_info['publication_title'] = node.querySelector('.issue-item__detail a').getAttribute('title');                    
		paper_info['abstract'] = node.querySelector('.issue-item__abstract').innerText;          
	}catch(err) {                                                                                                                                  
		console.log('%c该节点获取信息有误（可能有部分信息缺失）', err ,'color:blue;font-size:15px');
		console.log(err);
		console.log(node);                                                                                                                         
	}                                                                                                                                              
	console.log('文章标题:'		 + paper_info['document_title']);                                                                                        
	console.log('出版物标题：'	 + paper_info['publication_title']);                                                                            
	console.log('文章说明：'          + paper_info['description']);                                                                                
	console.log('url：'          + paper_info['url']);                                                                                             
	console.log('摘要：'       + paper_info['abstract']);
	return paper_info;                                                                                                                             
}
function getInfoList(){                                                                                                                            
	infoList = [];                                                                                                                                 
	list = document.getElementsByClassName('search__item');                                                                                  
	for (var i = 0; i < list.length; i++) {                                                                                                        
		console.log(i);                                                                                                                            
		console.log(list[i]);                                                                                                                      
		infoList.push(showInfo(list[i]));                                                                                                          
	}                                                                                                                                              
	return infoList;                                                                                                                               
}     
getInfoList()                                                                      
//去掉注释
//加上分号
//加上转义\
//加多行分割符\

"\
function showInfo(node){\
	var paper_info = {};\
	try {\
		home = 'https://dl.acm.org';\
		paper_info['document_title'] = node.querySelector('.issue-item__title .hlFld-Title').innerText;\
		paper_info['url'] = home + node.getElementsByClassName('hlFld-Title')[0].getElementsByTagName('a')[0].getAttribute('href');\
		paper_info['description'] = [];\
		node.querySelectorAll('.issue-item__detail .dot-separator span').forEach((x) => paper_info['description'].push(x.innerText));\
		link = node.querySelector('.issue-item__detail a').href;\
		paper_info['publication_title'] = node.querySelector('.issue-item__detail a').getAttribute('title');\
		paper_info['abstract'] = node.querySelector('.issue-item__abstract').innerText;        \
	}catch(err) {                                                                   \
		console.log('%c该节点获取信息有误（可能有部分信息缺失）', err ,'color:blue;font-size:15px');\
		console.log(err);\
		console.log(node);                                                                 \
	}                                                                                      \
	console.log('文章标题:'		 + paper_info['document_title']);                            \
	console.log('出版物标题：'	 + paper_info['publication_title']);                       \
	console.log('文章说明：'          + paper_info['description']);                        \
	console.log('url：'          + paper_info['url']);                                     \
	console.log('摘要：'       + paper_info['abstract']);     \
	return paper_info;                                                                     \
}\
function getInfoList(){                                                                    \
	infoList = [];                                                                         \
	list = document.getElementsByClassName('search__item');                                \
	for (var i = 0; i < list.length; i++) {                                                \
		console.log(i);                                                                    \
		console.log(list[i]);                                                              \
		infoList.push(showInfo(list[i]));                                                  \
	}                                                                                      \
	return infoList;                                                                       \
}return getInfoList();"