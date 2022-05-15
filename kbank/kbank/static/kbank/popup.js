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
    showPopup("Спасибо! Что поделились знанием! Ваша статья отправлена на модерацию");
    submitForm();
}