function showPopup(message) {
  var popup = document.getElementById("myPopup");
  popup.innerText = message;
  popup.classList.add("show");
  setTimeout(() => {
  document.getElementById("myPopup").classList.remove("show");
}, "3000")
}

function submitForm(){
  var articleForm = document.getElementById("create-article");
  setTimeout(() => {
  articleForm.submit();
}, "3000")

}

function submitNewArticle(){
    const text = tinymce.get("id_text").getContent();
    const title = document.getElementById("id_title").value;
    const category = document.getElementById("id_category").value;

    if(text!="" && title!="" && category!=""){
        showPopup("Спасибо, что поделились информацией! Ваша статья отправлена на модерацию!");
        submitForm();
    }
    else{
        document.getElementById("create-article").submit();
    }
}