
	//チェックボックスで時間帯ON・OFF切り替え
	var is_check_sunday = document.getElementById('id_is_holiday_sunday');
	var sunday = document.getElementsByClassName('sunday');

	function view_check(){
		if( is_check_sunday.checked ){
			for (let i = 0; i < sunday.length; i++) {
				sunday[i].style.display = 'none';
			}
		}else{
			for (let i = 0; i < sunday.length; i++) {
				sunday[i].style.display = 'block';
			}
		}
	}
	window.addEventListener('load', view_check);
	is_check_sunday.onchange = view_check;