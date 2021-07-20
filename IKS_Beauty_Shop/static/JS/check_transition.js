
	//ページ移動確認
	function beforeUnload(event){
		event.preventDefault();
		event.returnValue = 'ページを移動します';
	}
		
	window.addEventListener('beforeunload', beforeUnload);

	function funcRem() {
		window.removeEventListener('beforeunload', beforeUnload);
	}