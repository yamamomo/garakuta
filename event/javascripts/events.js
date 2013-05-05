
$(function(){
  $("#form1").validate({
    rules : {
      title: {
        required: true,
        minlength: 2 
       },
      content: {
        required: true,
        minlength: 3
      }
    },
    messages:{
      title: {
       required: "タイトルを記入してください",
      },
      content: {
       required: "内容を記入してください",
      }
    }
  });

});

function del_kakunin(){
	if(confirm("本当に削除しますか？")){
		return true;
	}else{
		return false;
	}
};

function setEmptyStart(EP) {
 	if (EP.value == ""){ 　
 	document.form1.start_month.value = "";
 	document.form1.start_day.value = "";
 	document.form1.start_jikan.value = "";
 	document.form1.start_min.value = "";}
 	else{}
};

function setEmptyEnd(EP) {
        if (EP.value == ""){ 　
        document.form1.end_month.value = "";
        document.form1.end_day.value = "";
        document.form1.end_jikan.value = "";
        document.form1.end_min.value = "";}
        else{}
}; 
