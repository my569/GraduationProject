function showInfo(node){                                                                                                                    
	var paper_info = {};                                                                                                                    
	try {                                                                                                                                   
		home = 'ieeexplore.ieee.org';                                                                                                       
		paper_info['document_title_info'] = node.getElementsByTagName('h2')[0].innerText;                                                   
		paper_info['url_info'] = home + node.getElementsByTagName('h2')[0].getElementsByTagName('a')[0].getAttribute('href');               
		paper_info['authors_info'] = node.getElementsByClassName('author')[0].innerText;                                                    
		paper_info['publication_title_info'] = node.getElementsByClassName('description')[0].getElementsByTagName('a')[0].innerText;        
		publisher_node = node.getElementsByClassName('description')[0].getElementsByClassName('publisher-info-container')[0];               
		paper_info['publisher_year_info'] = publisher_node.getElementsByTagName('span')[0].innerText;                                       
		paper_info['publisher_kind_info'] = publisher_node.getElementsByTagName('span')[3].innerText;                                       
		paper_info['publisher_name_info'] = publisher_node.getElementsByTagName('span')[6].innerText;                                       
		paper_info['abstract_info'] = node.getElementsByClassName('js-displayer-content')[0].getElementsByTagName('span')[0].innerText;     
	}catch(err) {                                                                                                                           
		console.log('%c该节点获取信息有误（可能有部分信息缺失）','color:blue;font-size:15px');                                              
		console.log(node);                                                                                                                  
	}                                                                                                                                       
	console.log('文章标题:'		 + paper_info['document_title_info']);                                            
	console.log('作者:' 		 + paper_info['authors_info']);                                                   
	console.log('出版物标题：'	 + paper_info['source_info']);                                                    
	console.log('发布年份：'     + paper_info['publisher_year_info']);                                            
	console.log('出版物类型：'   + paper_info['publisher_kind_info']);                                            
	console.log('出版商：'       + paper_info['publisher_name_info']);                                            
	console.log('url：'          + paper_info['url_info']);                                                       
	console.log('\n摘要：'       + paper_info['abstract_info']);                                                                                                                                            
	return paper_info;                                                                                            
}                                                                                                                 
showInfo(document.getElementsByClassName('List-results-items')[0]);                                               
list = document.getElementsByClassName('List-results-items');                                                     
for (var i = 0; i < list.length; i++) {                                                                           
	console.log(i);                                                                                               
	console.log(list[i]);                                                                                         
    showInfo(list[i]);                                                                                            
}                                                                                                                 
paper_info = showInfo(list[1]);                                                                                   
return paper_info;                                                                                                
//去掉注释
//加上分号
//加上转义\
//加多行分割符\

function showInfo(node){                                                                                                      \
	try {                                                                                                                     \
		home = 'ieeexplore.ieee.org';                                                                                         \
		title_info = node.getElementsByTagName('h2')[0].innerText;                                                            \
		url_info = home + node.getElementsByTagName('h2')[0].getElementsByTagName('a')[0].getAttribute('href');               \
		author_info = node.getElementsByClassName('author')[0].innerText;                                                     \
		source_info = node.getElementsByClassName('description')[0].getElementsByTagName('a')[0].innerText;                   \
		publisher_node = node.getElementsByClassName('description')[0].getElementsByClassName('publisher-info-container')[0]; \
		publisher_year_info = publisher_node.getElementsByTagName('span')[0].innerText;                                       \
		publisher_kind_info = publisher_node.getElementsByTagName('span')[3].innerText;                                       \
		publisher_name_info = publisher_node.getElementsByTagName('span')[6].innerText;                                       \
		abstract_info = node.getElementsByClassName('js-displayer-content')[0].getElementsByTagName('span')[0].innerText;     \
	}                                                                                                                         \
	catch(err) {                                                                                                              \
		console.log('%c该节点获取信息有误（可能有部分信息缺失）','color:blue;font-size:15px');                                \
		console.log(node);                                                                                                    \
	}                                                                                                                         \
	console.log('标题:' + title_info +                                                                                        \
					'\\n作者:' + author_info +                                                                                 \
					'\\n文章具体来源：' + source_info +                                                                        \
					'\\n发布年份：' + publisher_year_info +                                                                    \
					'\\n出版物类型：' + publisher_kind_info +                                                                  \
					'\\n出版商：' + publisher_name_info +                                                                      \
					'\\nurl：' + url_info +                                                                                    \
					'\\n摘要：' + abstract_info                                                                                \
					);                                                                                                        \
}                                                                                                                             \
showInfo(document.getElementsByClassName('List-results-items')[0]);                                                           \
list = document.getElementsByClassName('List-results-items');                                                                 \
for (var i = 0; i < list.length; i++) {                                                                                       \
	console.log(i + '\\n');                                                                                                    \
	console.log(list[i]);                                                                                                     \
    showInfo(list[i]);                                                                                                        \
}
